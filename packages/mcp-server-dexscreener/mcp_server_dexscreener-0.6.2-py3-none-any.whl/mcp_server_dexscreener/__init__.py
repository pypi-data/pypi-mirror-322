from .server import serve


def main():
    """MCP Server - Dexscreener functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to fetch and convert dexscreener content"
    )

    asyncio.run(serve())


if __name__ == "__main__":
    main()