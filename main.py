from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, prank_tool, save_tool

# These tools are used for formatting AI outputs
# We can then use its output predictively
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Loads environment files
load_dotenv()

# This is the output format we want from our LLMs'
class ResearchResponse(BaseModel):
    topic: str # Topic of the research
    summary: str # Small summary of the conducted research
    sources: list[str] # List of all the sources used
    tools_used: list[str] # Tools that were used in the research

# Choosing our LLM
llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# To use our llm, we need a API key, which we will add into our .env file

# After doing that, I am making a simple request to test
# response = llm.invoke("What is the meaning of life?")
# model = "gemini-2.0-flash"
# response = llm.models.generate_content(model=model, contents="What is the meaning of life?")

# print(response)
# print(response.text)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an agentic research assistant that will help generate a research paper.
            Answer the user query and use necessary tools provided.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, prank_tool, save_tool]
llm = llm.bind_tools(tools)
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = input("What would you like to research? ")

raw_response = agent_executor.invoke({"query": query})

# print(raw_response)

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print(e)
