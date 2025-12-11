from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
      print("POR FAVOR, INSIRA A CHAVE DE API DO GOOGLE_API_KEY NO ARQUIVO '.env'")

LLM_TICKET = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash-lite",
      api_key = GEMINI_API_KEY,
      temperature = 0
)
LLM = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash",
      api_key = GEMINI_API_KEY
)



TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY is None:
      print("POR FAVOR, INSIRA A CHAVE DE API DO TAVILY_API_KEY NO ARQUIVO '.env'")

