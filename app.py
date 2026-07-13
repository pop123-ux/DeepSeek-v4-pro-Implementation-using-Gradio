"""Gradio chat UI backed by DeepSeek's OpenAI-compatible API.

Runs locally with `python app.py`. Set `DEEPSEEK_API_KEY` in the environment
before launching (see .env.example).
"""

from __future__ import annotations

import os
from typing import Iterator

import gradio as gr
from openai import OpenAI

DEFAULT_MODEL       = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
DEFAULT_BASE_URL    = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEFAULT_SYSTEM_PROMPT = "You are a helpful, concise AI assistant."


def get_client() -> OpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY is not set. Export it in your shell or add it "
            "to a .env file — see .env.example."
        )
    return OpenAI(api_key=api_key, base_url=DEFAULT_BASE_URL)


client = get_client()


def stream_chat(
    message: str,
    history: list[dict],
    system_prompt: str,
    temperature: float,
    max_tokens: int,
) -> Iterator[str]:
    """Stream a DeepSeek chat completion for the given conversation."""
    messages = [{"role": "system", "content": system_prompt or DEFAULT_SYSTEM_PROMPT}]
    # Gradio's `type="messages"` hands us a list of {role, content} dicts.
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        partial = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                partial += delta
                yield partial
    except Exception as exc:
        yield f"**API error:** `{exc}`"


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="DeepSeek Chat") as demo:
        gr.Markdown(
            f"# 💬 DeepSeek Chat\n"
            f"Streaming chat UI over the **`{DEFAULT_MODEL}`** model via DeepSeek's "
            f"OpenAI-compatible API."
        )
        with gr.Accordion("Settings", open=False):
            system_prompt = gr.Textbox(
                label="System prompt",
                value=DEFAULT_SYSTEM_PROMPT,
                lines=2,
            )
            temperature = gr.Slider(0.0, 2.0, value=0.7, step=0.1, label="Temperature")
            max_tokens  = gr.Slider(64, 4096, value=1024, step=64, label="Max tokens")

        gr.ChatInterface(
            fn=stream_chat,
            additional_inputs=[system_prompt, temperature, max_tokens],
            examples=[
                ["Explain transformers in one paragraph.",              DEFAULT_SYSTEM_PROMPT, 0.7, 1024],
                ["Write a Python function that reverses a string in place.", DEFAULT_SYSTEM_PROMPT, 0.7, 1024],
                ["What are three underrated data structures?",         DEFAULT_SYSTEM_PROMPT, 0.7, 1024],
            ],
        )
    return demo


if __name__ == "__main__":
    build_ui().launch(
        server_name="0.0.0.0",
        share=False,
        theme=gr.themes.Soft(),
    )
