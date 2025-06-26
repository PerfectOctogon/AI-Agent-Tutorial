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

def save_to_file(string_to_save):
    file = open("output.txt", "w")
    file.write(string_to_save)
    file.close()

save_tool = Tool(
    name="save",
    func=save_to_file,
    description="Use to save findings to a file"
)

def prank(prank_string):
    return prank_string + "\nHaha... just joking :)"

prank_tool = Tool(
    name="prank",
    func=prank,
    description='Used to prank people.'
)