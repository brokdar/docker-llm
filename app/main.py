import asyncio

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", "app.env"], env_file_encoding="utf-8"
    )

    model_name: str = "ai/smollm2:latest"
    base_url: str | None = None
    api_key: str | None = None


settings = Settings()


model = OpenAIModel(
    model_name=settings.model_name,
    provider=OpenAIProvider(base_url=settings.base_url, api_key=settings.api_key),
)

agent = Agent(
    model, system_prompt="You are a helpful assistant. Be concise and friendly."
)


async def main():
    result = await agent.run("What is the capital of France?")
    print(result.output)

    async with agent.run_stream("What is the capital of the UK?") as response:
        print(await response.get_output())


if __name__ == "__main__":
    asyncio.run(main())
