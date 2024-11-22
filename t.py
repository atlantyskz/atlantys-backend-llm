import requests
import json

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-4o-mini-2024-07-18",
    "messages": [
        {
            "role": "user",
            "content": "What's in this image?"
        },
        {
            "role": "user",
            "content": "Hi"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response from the API
print(response.status_code)
print(response.json())
