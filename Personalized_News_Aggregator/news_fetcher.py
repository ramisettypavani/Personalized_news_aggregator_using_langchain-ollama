import requests
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, Tool
from langchain_ollama.llms import OllamaLLM
from summarizer import summarizer_instance

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines"
        self.llm = OllamaLLM(model="llama3")
        self.news_tool = self.create_news_tool()
        self.agent = self.create_agent()

    def fetch_news(self, query, sources):
        params = {
            'q': query,
            'sources': ','.join(sources),
            'apiKey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json().get('articles', [])

    def summarize_article(self, article_text):
        return summarizer_instance.summarize(article_text)

    def fetch_and_summarize(self, query, sources):
        articles = self.fetch_news(query, sources)
        summarized_articles = [
            {
                'title': article['title'],
                'summary': self.summarize_article(article.get('content', ''))
            }
            for article in articles[:5]
        ]
        return summarized_articles

    def create_news_tool(self):
        def fetch_tool(input_data):
            query = input_data.get("query", "")
            sources = input_data.get("sources", [])
            return self.fetch_news(query, sources)
        
        return Tool(
            name="NewsFetcher",
            func=fetch_tool,
            description="Fetches the top 5 news articles based on the query and sources."
        )

    def create_agent(self):
        template = '''You are a news agent. Your task is to fetch the top 5 news articles based on the user's preferences.
        You have access to the following tools:
        {tools}
        Thought: You should fetch the latest news.
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Begin!
        Thought: {agent_scratchpad}
        '''
        prompt = PromptTemplate.from_template(template)
        tools = [self.news_tool]
        return create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt,
            stop_sequence=True
        )
