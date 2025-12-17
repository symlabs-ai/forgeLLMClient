"""
Async Chat Example - Non-blocking chat with AsyncChatAgent.

This example demonstrates async/await patterns for concurrent LLM calls.
"""
import asyncio
import os

from forge_llm.application.agents import AsyncChatAgent
from forge_llm.domain.entities import ProviderConfig


async def main() -> None:
    # Create async agent
    config = ProviderConfig(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY") or "",
        model="gpt-4o-mini",
    )
    agent = AsyncChatAgent(config)

    # Single async chat
    response = await agent.chat("What is 2 + 2?")
    print(f"Response: {response.content}")

    # Concurrent requests
    questions = [
        "What is the capital of Japan?",
        "What is the largest planet?",
        "What year did WW2 end?",
    ]

    # Run multiple requests concurrently
    tasks = [agent.chat(q) for q in questions]
    responses = await asyncio.gather(*tasks)

    for question, response in zip(questions, responses, strict=False):
        print(f"\nQ: {question}")
        print(f"A: {response.content}")


async def streaming_example() -> None:
    """Example of async streaming."""
    config = ProviderConfig(
        provider="anthropic",
        api_key=os.getenv("ANTHROPIC_API_KEY") or "",
        model="claude-3-haiku-20240307",
    )
    agent = AsyncChatAgent(config)

    print("\nStreaming response:")
    async for chunk in agent.stream_chat("Tell me a short joke"):
        print(chunk.content, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(streaming_example())
