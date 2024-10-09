from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Please provide a concise and comprehensive summary of the article provided below. 
The summary should capture the main points, key arguments, and significant details of the article while omitting any unnecessary information or minor details. 
Ensure that the summary is clear and easy to understand, accurately reflecting the essence of the article.

Article Text:
{article_text}
Summary: """

prompt_template = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3")
chain = prompt_template | model

class Summarizer:
    def __init__(self):
        self.chain = chain

    def summarize(self, article_text):
        response = self.chain.invoke({"article_text": article_text})
        print("Response:", response)
        return response

summarizer_instance = Summarizer()