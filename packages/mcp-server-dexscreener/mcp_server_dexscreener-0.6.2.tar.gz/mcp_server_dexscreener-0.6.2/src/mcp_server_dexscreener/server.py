import json
from typing import Dict, List, TypeVar, Generic, Optional
from urllib.parse import urljoin, urlencode
import httpx
from mcp import ErrorData, McpError, stdio_server
from mcp.server import Server
from mcp.server.websocket import websocket_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from typing import Annotated, Tuple
from pydantic import BaseModel, Field, AnyUrl

T = TypeVar('T')

BASE_URL = "https://api.dexscreener.com"

class DexScreenerError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Status {status_code}: {message}")

class RateLimiter:
    """
    A simple rate limiter placeholder. 
    In a real implementation, you'd add actual rate limiting logic.
    """
    async def wait_for_slot(self):
        # Implement actual rate limiting if needed
        pass

class DexScreenerClient:
    def __init__(self, 
                 token_rate_limiter: RateLimiter = RateLimiter(),
                 dex_rate_limiter: RateLimiter = RateLimiter()):
        self.token_rate_limiter = token_rate_limiter
        self.dex_rate_limiter = dex_rate_limiter
        self.client = httpx.AsyncClient()

    async def fetch(
        self, 
        endpoint: str, 
        rate_limiter: RateLimiter,
        params: Optional[Dict[str, str]] = None
    ) -> T:
        """
        Fetch data from DexScreener API with rate limiting
        
        :param endpoint: API endpoint
        :param rate_limiter: Rate limiter to use
        :param params: Optional query parameters
        :return: Parsed JSON response
        """
        await rate_limiter.wait_for_slot()

        # Construct full URL
        url = urljoin(BASE_URL, endpoint)
        
        # Add query parameters if provided
        if params:
            url = f"{url}?{urlencode(params)}"

        try:
            response = await self.client.get(url)
            
            # Raise an exception for bad HTTP responses
            response.raise_for_status()
            
            # Return parsed JSON
            return response.json()
        
        except httpx.HTTPError as error:
            # Convert network errors to DexScreenerError
            raise DexScreenerError(
                500, 
                f"Network error: {str(error)}"
            )

    # Token Profile Endpoints
    async def get_latest_token_profiles(self) -> List[Dict]:
        return await self.fetch(
            '/token-profiles/latest/v1', 
            self.token_rate_limiter
        )

    # Token Boost Endpoints
    async def get_latest_boosted_tokens(self) -> List[Dict]:
        return await self.fetch(
            '/token-boosts/latest/v1', 
            self.token_rate_limiter
        )

    async def get_top_boosted_tokens(self) -> List[Dict]:
        return await self.fetch(
            '/token-boosts/top/v1', 
            self.token_rate_limiter
        )

    # Orders Endpoint
    async def get_token_orders(
        self, 
        chain_id: str, 
        token_address: str
    ) -> List[Dict]:
        return await self.fetch(
            f'/orders/v1/{chain_id}/{token_address}', 
            self.token_rate_limiter
        )

    # DEX Pairs Endpoints
    async def get_pairs_by_chain_and_address(
        self, 
        chain_id: str, 
        pair_id: str
    ) -> Dict:
        return await self.fetch(
            f'/latest/dex/pairs/{chain_id}/{pair_id}', 
            self.dex_rate_limiter
        )

    async def get_pairs_by_token_addresses(
        self, 
        token_addresses: str
    ) -> Dict:
        return await self.fetch(
            f'/latest/dex/tokens/{token_addresses}', 
            self.dex_rate_limiter
        )

    async def search_pairs(
        self, 
        query: str
    ) -> Dict:
        return await self.fetch(
            '/latest/dex/search', 
            self.dex_rate_limiter,
            params={'q': query}
        )

    async def search_blockchain_tokens(
        self, 
        chain_name: str
    ) -> Dict:
        return await self.fetch(
            '/latest/dex/search', 
            self.dex_rate_limiter,
            params={'q': chain_name}
        )

    async def close(self):
        """
        Close the HTTP client when done
        """
        await self.client.aclose()

class SearchBlockchainTokens(BaseModel):
    """Parameters for searching blockchain tokens."""

    chain_name: Annotated[str, Field(description="Name of the blockchain to search for tokens")]

class SearchPairsByTokenAddresses(BaseModel):
    """Parameters for searching pairs by token addresses."""

    token_addresses: Annotated[str, Field(description="Comma-separated list of token addresses")]

async def serve() -> None:
    """Run the dexscreener MCP server.

    Args:
        custom_user_agent: Optional custom User-Agent string to use for requests
        ignore_robots_txt: Whether to ignore robots.txt restrictions
    """
    server = Server("mcp-dexscreener")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="search_blockchain_tokens",
                description="""Gets the tokens on a given blockchain.""",
                inputSchema=SearchBlockchainTokens.model_json_schema(),
            ),
            Tool(
                name="search_pairs_by_token_addresses",
                description="""Gets the pairs on a given blockchain.""",
                inputSchema=SearchPairsByTokenAddresses.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="search_blockchain_tokens",
                description="Search for tokens on a given blockchain",
                arguments=[
                    PromptArgument(
                        name="chain_name", description="Name of the blockchain to search for tokens", required=True
                    )
                ],
            ),
            Prompt(
                name="search_pairs_by_token_addresses",
                description="Search for pairs by token addresses",
                arguments=[
                    PromptArgument(name="token_addresses", description="Comma-separated list of token addresses", required=True)
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        client = DexScreenerClient()
        result = None
        try:
            if name == "search_blockchain_tokens":
                args = SearchBlockchainTokens(**arguments)
                chain_name = str(args.chain_name)
                if not chain_name:
                    raise McpError(INVALID_PARAMS, "Chain name is required")
                result = await client.search_blockchain_tokens(chain_name)

            elif name == "search_pairs_by_token_addresses":
                args = SearchPairsByTokenAddresses(**arguments)
                token_addresses = str(args.token_addresses)
                if not token_addresses:
                    raise McpError(INVALID_PARAMS, "Token addresses are required")
                result = await client.get_pairs_by_token_addresses(token_addresses)

            else:
                raise McpError(INVALID_PARAMS, f"Invalid tool name: {name}")

            json_output = json.dumps(result, indent=2)
            return [TextContent(type="text", text=json_output)]

        except McpError as e:
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Error processing tool {name}: {str(e)}"))

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)