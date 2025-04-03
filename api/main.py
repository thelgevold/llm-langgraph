from fastapi import FastAPI
from dtos.news_context import NewsContext

app = FastAPI()

from news_agent import start_agent

@app.post('/api/news')
async def get_news(news_context: NewsContext):
    response = start_agent(news_context)
    return response
