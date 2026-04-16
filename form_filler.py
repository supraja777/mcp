import asyncio

class JobFormFiller:
    def __init__(self, session):
        self.session = session

    async def fill(self, data: dict):
        script = f"""
        const data = {data};

        function setField(selector, value) {{
            const el = document.querySelector(selector);
            if (!el) return false;

            el.focus();
            el.value = value;

            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));

            return true;
        }}

        function delay(ms) {{
            return new Promise(res => setTimeout(res, ms));
        }}

        async function run() {{
            await delay(1000);

            setField('[name="first_name"]', data.firstName);
            await delay(500);

            setField('[name="last_name"]', data.lastName);
            await delay(500);

            setField('[name="email"]', data.email);
            await delay(500);

            setField('[name="phone"]', data.phone);
            await delay(500);

            setField('[name="country"]', data.country);
        }}

        run();
        """

        return await self.session.call_tool(
            "puppeteer_evaluate",
            arguments={"script": script}
        )