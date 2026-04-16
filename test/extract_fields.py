import json


def extract_fields_from_response(response):
    """
    Extract and clean input fields from MCP puppeteer_evaluate response
    """

    try:
        print("Actual response is ", response)
        raw_text = response.content[0].text.strip()

        print("RAW RESPONSE:", raw_text)  # debug (you can remove later)

        # 🧠 Remove MCP wrappers if present
        if "Execution result:" in raw_text:
            raw_text = raw_text.split("Execution result:")[1]

        if "Console output:" in raw_text:
            raw_text = raw_text.split("Console output:")[0]

        raw_text = raw_text.strip()

        # 🔥 Handle double-encoded JSON
        data = json.loads(raw_text)

        # If still string → decode again
        if isinstance(data, str):
            data = json.loads(data)

        # ✅ Clean: remove fields with empty IDs
        data = [field for field in data if field.get("id")]

        return data

    except Exception as e:
        print("❌ Parsing failed")
        print("CLEANED RAW:", raw_text if 'raw_text' in locals() else "N/A")
        print("ERROR:", e)
        return []