class GenerationAgent:
    def __init__(self, kernel):
        self.kernel = kernel

    async def generate_variants(self, segment, retrieved_content):
        prompt = f"""
You are a marketing assistant.

Use ONLY the content below and include citations:
{retrieved_content}

Create 3 personalized message variants for the segment: {segment}.
"""

        result = await self.kernel.run(prompt, service_id="azure-gpt")
        return str(result)
