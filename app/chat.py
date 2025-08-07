import asyncio

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
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


def stream_chat_response(prompt: str, message_history: list[ModelMessage]):
    """Stream chat response from the LLM agent with the given prompt and message history.

    Args:
        prompt (str): The current user prompt to send to the agent
        message_history (list[ModelMessage]): Previous conversation messages for context

    Yields:
        str: Individual text chunks from the streaming LLM response
    """

    async def async_stream():
        try:
            async with agent.run_stream(
                prompt, message_history=message_history
            ) as result:
                response_text = ""
                async for text in result.stream_text(delta=True):
                    response_text += text
                    yield text
                st.session_state.chat_history = result.all_messages()
        except Exception as e:
            yield f"Error: {str(e)}"

    # Convert async generator to sync generator for Streamlit
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        async_gen = async_stream()
        while True:
            try:
                yield loop.run_until_complete(async_gen.__anext__())
            except StopAsyncIteration:
                break
    finally:
        loop.close()


def main():
    st.title("LLM Chat Assistant")
    st.caption("Powered by Pydantic AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you with?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(
                stream_chat_response(prompt, st.session_state.chat_history)
            )

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
