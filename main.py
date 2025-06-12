from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from google import genai

# Loads environment files
load_dotenv()

# Choosing our LLM
# llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm = genai.Client()

# To use our llm, we need a API key, which we will add into our .env file

# After doing that, I am making a simple request to test
# response = llm.invoke("What is the meaning of life?")
model = "gemini-2.0-flash"
response = llm.models.generate_content(model=model, contents="What is the meaning of life?")

# print(response)
print(response.text)