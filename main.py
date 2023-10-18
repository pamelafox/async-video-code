import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(".env")

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=f"https://{os.environ['OPENAI_RESOURCE_NAME']}.openai.azure.com/openai/deployments/{os.environ['OPENAI_DEPLOYMENT_NAME']}",
    default_query={
        "api-version": "2023-03-15-preview",
    },
    default_headers={"api-key": os.environ["OPENAI_API_KEY"]},
)


async def generate_response(creature, location):
    print(f"Generating response for {creature} in {location}...")
    response = await client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "You are a tired parent trying to get your child to sleep."},
            {"role": "user", "content": f"Make up a short story about a {creature} who lives in {location}."},
        ],
        temperature=0.5,
        max_tokens=400,
    )
    print(f"Got response for {creature} in {location}!")
    return response


async def main():
    responses = await asyncio.gather(
        generate_response("unicorn", "ponyland"),
        generate_response("dragon", "castle"),
        generate_response("mermaid", "ocean"),
    )
    for response in responses:
        print(response.choices[0].message.content)


asyncio.run(main())
