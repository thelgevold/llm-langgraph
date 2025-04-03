from state import Article

class NewsResult:
    article_summary: str
    categories: list[str]
    original_link: str
    categories: str  

    def __init__(self, article: Article):
        self.article_summary = article.summary.content
        self.categories = article.tool_result
        self.original_link = article.link