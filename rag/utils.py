import requests


def gptunnel_call(prompt: str, api_key: str, model="ministral-3b"):
    url = "https://gptunnel.ru/v1/chat/completions"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]
