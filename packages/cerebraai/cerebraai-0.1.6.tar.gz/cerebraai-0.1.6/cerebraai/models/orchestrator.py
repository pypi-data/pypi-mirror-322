# Written by Juan Pablo Gutiérrez
# 03/01/2025

from sentence_transformers import SentenceTransformer
from cerebraai.algorithms.analysis import get_best_model
from cerebraai.models.llm import LLM, LLMResponse

class Orchestrator:

    llms: list[LLM]
    """
    A class that represents an AI Orchestrator. It will balance prompting to different LLMs based on the user's prompt.
    """

    def __init__(self, llms: list[LLM], text_model: SentenceTransformer):
        self.llms = llms
        self.text_model = text_model

    def execute(self, prompt: str) -> LLMResponse:
        llm = get_best_model(self.text_model, prompt, self.llms)["llm"]
        return llm.execute(prompt)
