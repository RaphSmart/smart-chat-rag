from llama_cpp import Llama
from pathlib import Path


class LocalLLM:
    def __init__(
        self,
        model_path: Path,
        context_size: int = 2048,
        threads: int = 4
    ):
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=context_size,
            n_threads=threads,
            verbose=False
        )

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        output = self.llm(prompt, max_tokens=max_tokens)
        return output["choices"][0]["text"]
