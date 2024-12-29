from dotenv import load_dotenv

load_dotenv('../.env')

import os
from rag.utils import gptunnel_call
from langchain_core.language_models.llms import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.retrievers import ArxivRetriever
from langchain_mistralai import ChatMistralAI


class GPTunnelLLM(LLM):
    api_key: str
    model: str = "ministral-3b"  # the cheapest on gptunnel.ru, please use only this one

    def _call(self, prompt: str, stop=None):
        response = gptunnel_call(prompt, self.api_key, self.model)
        return response

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "GPTunnelChatModel"

    @property
    def _identifying_params(self):
        """Return a dictionary of identifying parameters."""
        return {"model_name": self.model}


class RAGPipeline:
    def __init__(self,
                 llm,
                 retriever
                 ):
        self.llm = llm
        self.retriever = retriever

        self.history = []

        self.prompt = ChatPromptTemplate.from_template(
            """You are an assistant who answers scientific questions using data from an articles' database.
            This data will be given to you each time, and it is called context.
            Answer the user's question based only on this context provided.
        
        Context: {context}
        
        Conversation history (include recent exchanges):
        {history}
        
        User's current question: {question}"""
        )

    @staticmethod
    def format_docs(docs):
        """Format retrieved documents for the LLM."""
        return "\n\n".join(doc.page_content for doc in docs)

    def build_chain(self):
        """Build the processing chain."""
        return (
                {
                    "context": {
                        "question": RunnablePassthrough()
                                    | (lambda x: x["question"])
                                    | self.retriever
                                    | self.format_docs
                    },
                    "question": RunnablePassthrough(),
                    "history": RunnablePassthrough(),
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
        )

    def handle_user_input(self, question: str) -> str:
        """Handles user input and manages conversation history."""
        # Build the chain
        chain = self.build_chain()

        # Append the user's question to the history
        user_input = f"User: {question}"
        formatted_history = "\n".join(self.history)

        # Invoke the chain and get the response
        response = chain.invoke({"question": question, "history": formatted_history})

        # Append both user input and assistant response to history
        assistant_response = f"Assistant: {response}"
        self.history.append(user_input)
        self.history.append(assistant_response)

        return response


# Example Usage
if __name__ == "__main__":
    # Initialize the retriever
    retriever = ArxivRetriever(
        top_k_results=3,
        get_full_documents=False,  # gives errors with MuPDF when True
        doc_content_chars_max=10000000000
    )

    mistral_llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0,
        max_retries=2,
        # other params...
    )

    assistant = RAGPipeline(llm=mistral_llm, retriever=retriever)

    # Example query
    question = "How does ImageBind model bind multiple modalities into a single embedding space? Tell me in detail."
    response = assistant.handle_user_input(question)
    print(response)
