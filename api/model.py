from langchain_ollama import ChatOllama
from tools.category_tools import get_article_categories

model_llm_tools = None
model_llm = None
 
def init_llm_with_tool_calling(): 
    global model_llm_tools

    if model_llm_tools == None:
        model_llm_tools = ChatOllama(model="qwen2.5", base_url = "http://llm-with-tool-calling:11434")
        model_llm_tools = model_llm_tools.bind_tools([get_article_categories])

    return model_llm_tools

def init_llm(): 
    global model_llm

    if model_llm == None:
        model_llm = ChatOllama(model="llama3.2:1b", base_url = "http://llm-without-tool-calling:11434", num_ctx=3000)
       
    return model_llm



