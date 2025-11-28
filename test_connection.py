import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

async def main():
    kernel = Kernel()

    kernel.add_service(
        AzureChatCompletion(
            service_id="azure-openai",
            endpoint="https://esthe-midqe1pi-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview",
            deployment_name="gpt-4o",
            api_key="3nRbzEXwpnhNJRSdwfzW4wyt77U7mcnd8374DTEYSQOxNIF1H74yJQQJ99BKACHYHv6XJ3w3AAAAACOGJJhL"
        )
    )

    response = await kernel.invoke_prompt("Say hello to Esther in a friendly tone!")
    print("AI Response:", response)

asyncio.run(main())
