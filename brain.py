import requests

def ask_llama(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
    )

    data = response.json()

    return data["response"]