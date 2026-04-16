import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from agent import GoogleAgent

async def run_browser_task():

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-puppeteer"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()
            print("🚀 Browser session started")

            # IMPORTANT: prove MCP is working
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            agent = GoogleAgent(session)
            await agent.run("hello world")

            print("✅ Done")

if __name__ == "__main__":
    asyncio.run(run_browser_task())