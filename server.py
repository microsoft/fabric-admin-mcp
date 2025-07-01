from fastmcp import FastMCP
import sys, os
from common import logger
from src.capacity import fabric_capacity_tools
from dotenv import load_dotenv

# import later to allow for environment variables to be set from command line
mcp = FastMCP("fabric-admin-mcp-server")
load_dotenv()

def register_tools(mcp: FastMCP) -> None:
    """
    Ensure all available MCP tools are registered with the MCP server.
    Args:
        mcp (FastMCP): The MCP server instance to register tools with 
    """
    fabric_capacity_tools.register_tools(mcp)

def main() -> None:
    logger.info("Starting Fabric Admin MCP server")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"PID: {os.getpid()}")    
    
    logger.error(f"Client: {os.getenv('AZURE_CLIENT_ID')}")

    register_tools(mcp)
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp/")
    
if __name__ == "__main__":
    main()