import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(question, context, model="llama3"):
    prompt = f"""Context:
{context}

Question:
{question}

Answer in table format if applicable."""

    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Ollama Error: {response.status_code} - {response.text}"
