from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from datetime import date

class agent_ollama:
    def __init__(self):
        self.model = "llama3.2"
        self.llm = ChatOllama(model="llama3.2", temperature=0.1)
        self.sysprompt = """Eres un agente de WebRTC por lo que todas tus respuestas con concisas y cortas, sin uso de emojis.
             Tu objetivo es usar las herramientas que tienes disponibles para responder las preguntas que te hagan"""
        self.tools = [self.get_systemtime]

    @tool
    def get_systemtime():
        """
        Returns today's system date
        """
        return date.today()
    
    @tool
    def search_theweb():
        """
        Returns a TavilySearchResults object in order to search the web
        """
        return TavilySearchResults()