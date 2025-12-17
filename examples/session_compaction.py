"""
Session Compaction Example - Manage long conversations with context compaction.

This example demonstrates different strategies for managing conversation context
when it exceeds the model's token limit.
"""
import os

from forge_llm import ChatAgent, ChatSession, TruncateCompactor
from forge_llm.application.session import SummarizeCompactor


def truncate_strategy() -> None:
    """Use truncation to manage context - removes oldest messages."""
    agent = ChatAgent(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
    )

    # TruncateCompactor removes oldest messages to fit context window
    session = ChatSession(
        system_prompt="You are a helpful assistant.",
        max_tokens=4000,
        compactor=TruncateCompactor(),
    )

    # Have a long conversation
    topics = [
        "Tell me about Python",
        "How about JavaScript?",
        "What is Rust?",
        "Compare them all",
    ]

    for topic in topics:
        response = agent.chat(topic, session=session)
        print(f"Q: {topic}")
        print(f"A: {response.content[:100]}...")
        print(f"   Tokens: {response.token_usage.total_tokens}")
        print()


def summarize_strategy() -> None:
    """Use LLM summarization to compress older context."""
    agent = ChatAgent(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
    )

    # SummarizeCompactor uses the LLM to summarize old messages
    compactor = SummarizeCompactor(
        agent=agent,
        summary_tokens=200,  # Target summary length
        keep_recent=4,  # Keep last 4 messages intact
    )

    session = ChatSession(
        system_prompt="You are a helpful assistant. Remember our conversation.",
        max_tokens=2000,  # Lower limit to trigger compaction sooner
        compactor=compactor,
    )

    # Long conversation
    messages = [
        "My name is Alice and I work as a data scientist.",
        "I'm interested in machine learning, especially NLP.",
        "I've been working with transformers for 2 years.",
        "What projects would you recommend for someone with my background?",
        "Can you summarize what you know about me?",
    ]

    for msg in messages:
        response = agent.chat(msg, session=session)
        print(f"User: {msg}")
        print(f"Assistant: {response.content[:200]}...")
        print(f"Session messages: {len(session.messages)}")
        print()


def ollama_local_session() -> None:
    """Use Ollama for local LLM with session management."""
    agent = ChatAgent(
        provider="ollama",
        model="llama3",
        base_url="http://localhost:11434",  # Default Ollama URL
    )

    session = ChatSession(
        system_prompt="You are a helpful coding assistant.",
        max_tokens=4000,
        compactor=TruncateCompactor(),
    )

    # Chat with local model
    response = agent.chat("Write a Python function to reverse a string", session=session)
    print(response.content)


if __name__ == "__main__":
    truncate_strategy()
    # summarize_strategy()
    # ollama_local_session()
