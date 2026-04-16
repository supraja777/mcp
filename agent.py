import asyncio

class GoogleAgent:
    def __init__(self, session):
        self.session = session

    async def open_google(self):
        return await self.session.call_tool(
            "puppeteer_navigate",
            arguments={
                "url": "https://job-boards.greenhouse.io/embed/job_app?for=ispottv&jr_id=69e001bc14bf245fc7a6f4da&token=4685254005&utm_source=jobright"
            }
        )

    async def search(self, query: str):
        script = f"""
        const input = document.querySelector('textarea[name="q"]');
        input.value = "{query}";
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        document.querySelector('form').submit();
        """

        return await self.session.call_tool(
            "puppeteer_evaluate",
            arguments={"script": script}
        )
    
    async def fill_job_form(self, data: dict):
        script = f"""
        const data = {data};

        function findInput(keywords) {{
            const inputs = Array.from(document.querySelectorAll('input'));

            return inputs.find(input => {{
                const attrs = (
                    (input.name || "") + " " +
                    (input.id || "") + " " +
                    (input.placeholder || "") + " " +
                    (input.getAttribute("aria-label") || "")
                ).toLowerCase();

                return keywords.some(k => attrs.includes(k));
            }});
        }}

        function setValue(input, value) {{
            if (!input) return;

            input.focus();
            input.value = value;

            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}

        // Map fields → keywords
        setValue(findInput(["first name", "firstname", "first"]), data.firstName);
        setValue(findInput(["last name", "lastname", "last"]), data.lastName);
        setValue(findInput(["email", "e-mail"]), data.email);
        setValue(findInput(["phone", "mobile", "contact"]), data.phone);
        setValue(findInput(["country"]), data.country);
        """

        return await self.session.call_tool(
            "puppeteer_evaluate",
            arguments={"script": script}
        )

    async def run(self, query="hello world"):
        await self.open_google()
        await asyncio.sleep(2)
        await self.fill_job_form({
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "country": "United States"
        })
        # await self.search(query)
        await asyncio.sleep(100)