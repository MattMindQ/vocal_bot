import logging
from typing import List  # NOQA: UP035

from openai import OpenAI
import streamlit as st


def create_gpt_completion(ai_model: str, messages: List[dict],API_O) -> dict:
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key= API_O,
    )
    completion = client.chat.completions.create(
        model=ai_model,
        messages=messages,
        stream=True,
        temperature=0,
    )
    logging.info(f"{completion=}")
    return completion
