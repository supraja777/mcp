import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent import GoogleAgent


async def run_browser_task():
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-puppeteer"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("🚀 Browser session started")

                # 🔍 List available tools
                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print("🛠 Tools detected:", tool_names)

                # ⚠️ Important debug check
                if "puppeteer_frames" not in tool_names:
                    print("⚠️ puppeteer_frames NOT available (will use fallback)")

                # 🤖 Run agent
                agent = GoogleAgent(session)
                await agent.run()

                print("✅ Done")

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        print(e)


if __name__ == "__main__":
    asyncio.run(run_browser_task())