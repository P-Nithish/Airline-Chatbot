import asyncio
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from .chroma_setup import get_chroma_client

load_dotenv()
GROQ_API_KEY = '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'

prompt = PromptTemplate.from_template("""
You are an airline policy assistant. Using only the provided policy context, provide a clear and concise answer.
If the context doesn’t contain the answer, say: "Sorry, I couldn’t find information related to that."

Context:
{context}

User question:
{question}

Answer:
""")

class PolicyRAGAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY
        )
        self.vectordb = get_chroma_client()

    async def query(self, question: str):
        results = await asyncio.to_thread(self.vectordb.similarity_search, question, 2)
        print("DEBUG: Retrieved docs:", [r.page_content for r in results])
        if not results:
            return {"answer": "No relevant policy found."}

        context = "\n\n".join([r.page_content for r in results])

        final_prompt = prompt.format(context=context, question=question)
        response = await asyncio.to_thread(self.llm.invoke, final_prompt)
        sources = [r.metadata.get("source", "") for r in results]
        return {"answer": response.content, "sources": list(set(sources))}
