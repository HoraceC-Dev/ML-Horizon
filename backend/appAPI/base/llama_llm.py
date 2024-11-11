from langchain_ollama.llms import OllamaLLM


def llm_llama3b():
    return OllamaLLM(model="llama3.2:latest", temperature=0.0, top_k=20, top_p= 0.6)