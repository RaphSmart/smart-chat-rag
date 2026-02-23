from llama_cpp import Llama
from pathlib import Path
import urllib.request

MODEL_URL = "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "phi-2.gguf"


def download_model():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_PATH.exists():
        print("Downloading Phi-2 model... (first run only)")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded.")


class LocalLLM:

    def __init__(self, model_path=None):

        download_model()

        self.llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=2048,
            verbose=False
        )

    def generate(self, prompt):

        output = self.llm(
            prompt,
            max_tokens=300,
            temperature=0.7
        )

        return output["choices"][0]["text"]