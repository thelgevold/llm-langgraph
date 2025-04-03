from typing_extensions import TypedDict
import json

class Article:
    title: str
    description: str
    link: str
    content: str
    summary: str
    tool_call_raw: object
    tool_argument: list[str]
    tool_name: str
    tool_result: str
    
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link

    def parse_tool_call(self):
        start_index = self.tool_call_raw.find("{")
        end_index = self.tool_call_raw.rfind("}") + 1
        json_str = self.tool_call_raw[start_index:end_index]

        data = json.loads(json_str)
        
        self.tool_name = data.get("name")
        categories = data.get("arguments", {}).get("article_categories")
        self.tool_argument = {"article_categories": categories}

    
class GraphState(TypedDict):
    data: str
    filter: list[str]
    articles: list[Article]
