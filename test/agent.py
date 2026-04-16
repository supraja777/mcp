import asyncio
import json
from extract_fields import extract_fields_from_response

class GoogleAgent:
    def __init__(self, session):
        self.session = session

    async def list_input_tags(self):
        
        script = """
        (() => {
            const results = [];

            const collect = (doc) => {
                return Array.from(doc.querySelectorAll('input, textarea, select'))
                    .map(el => ({
                        tag: el.tagName.toLowerCase(),
                        type: el.type || 'text',
                        name: el.name || '',
                        id: el.id || '',
                        placeholder: el.placeholder || ''
                    }));
            };

            // Main document
            results.push(...collect(document));

            // Try iframes (may fail silently due to CORS)
            const iframes = document.querySelectorAll('iframe');
            for (let frame of iframes) {
                try {
                    const doc = frame.contentDocument || frame.contentWindow.document;
                    if (doc) results.push(...collect(doc));
                } catch (e) {}
            }

            return JSON.stringify(results);
        })()
        """

        try:
            response = await self.session.call_tool(
                "puppeteer_evaluate",
                arguments={"script": script}
            )
            return extract_fields_from_response(response)

        except Exception as e:
            print("❌ Evaluate failed:", e)
            return []

    async def run(self):
        url = "https://job-boards.greenhouse.io/embed/job_app?for=ispottv&jr_id=69e001bc14bf245fc7a6f4da&token=4685254005&utm_source=jobright"

        print(f"🌍 Navigating to {url}...")

        try:
            await self.session.call_tool(
                "puppeteer_navigate",
                arguments={"url": url}
            )
        except Exception as e:
            print("❌ Navigation failed:", e)
            return

        # Wait for page load
        await asyncio.sleep(5)

        inputs = await self.list_input_tags()

        print(f"\n🎯 Found {len(inputs)} input fields:\n")

        for i in inputs:
            print(
                f"- [{i['tag']}] "
                f"Type: {i['type']} | "
                f"Name: {i['name']} | "
                f"ID: {i['id']} | "
                f"Placeholder: {i['placeholder']}"
            )