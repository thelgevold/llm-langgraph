from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from model import init_llm_with_tool_calling, init_llm
from tools.rss_tools import get_rss_links, get_rss_feed
from tools.url_tools import load_links
from state import GraphState
from tools.category_tools import get_article_categories
from dtos.news_context import NewsContext
from dtos.news_result import NewsResult

tools = [get_article_categories]
tools_names = {t.name: t for t in tools}

def generate_summary(state: GraphState):
    model = init_llm()

    articles = state["articles"]

    for article in articles:
        content = f"""
        Generate a two paragraph summary of the following text: {article.content}
        """

        request = [HumanMessage(content=content)]
        summary = model.invoke(request)
        article.summary = summary
        
    return {"articles": articles}

def get_categories(state: GraphState):
    model = init_llm_with_tool_calling()

    articles = state["articles"]

    for article in articles:
        content= f"""You are an assistant who will use the tool called get_article_categories. Determine the categories that best describe this text: {article.summary}
        Use only categories from the following list: Real Estate, Politics, Sports, Immigration, Food, Entertainment, Business, Crime, Weather, Technology, Medicine, Science or Other. 
        You may select more than one category per text"""
        
        request = [SystemMessage(content=content)]
        categories = model.invoke(request)
        article.tool_call_raw = categories.content
        
    return {"tool": content}

def execute_tools(state: GraphState):
    articles = state["articles"]
    
    for article in articles:
        article.parse_tool_call()

        article.tool_result = tools_names[article.tool_name].invoke(article.tool_argument) 
              
    return {"articles": articles}

def start_agent(news_ctx: NewsContext): 
    graph_builder=StateGraph(GraphState)
    graph_builder.add_node("get_rss_feed", get_rss_feed)
    graph_builder.add_node("get_rss_links", get_rss_links)
    graph_builder.add_node("load_links", load_links)
    graph_builder.add_node("generate_summary", generate_summary)
    graph_builder.add_node("execute_tools", execute_tools)
    graph_builder.add_node("get_categories", get_categories)

    graph_builder.add_edge(START, "get_rss_feed")  
    graph_builder.add_edge("get_rss_feed", "get_rss_links" )
    graph_builder.add_edge("get_rss_links", "load_links")
    graph_builder.add_edge("load_links", "generate_summary")
    graph_builder.add_edge("generate_summary", "get_categories")
    graph_builder.add_edge("get_categories", "execute_tools")
    graph_builder.add_edge("execute_tools", END)
    
    graph=graph_builder.compile()

    print(graph.get_graph().draw_ascii())

    result = graph.invoke({"data": news_ctx.rss_feed})

    return [NewsResult(r) for r in result["articles"]]
