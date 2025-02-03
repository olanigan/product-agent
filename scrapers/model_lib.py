import os
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp')
OLLAMA_MODEL = OllamaModel('deepseek-r1:7b')
GROQ_MODEL = GroqModel('llama3-groq-8b-8192-tool-use-preview')
OPENAI_MODEL = OpenAIModel('gpt-4o-mini', openai_client=client)