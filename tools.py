from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the internet for information"
)

def prank(prank_string):
    return prank_string + "\nHaha... just joking :)"

prank_tool = Tool(
    name="prank",
    func=prank,
    description='Used to prank people.'
)