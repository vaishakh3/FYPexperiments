import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/octet-stream"
}

def query(filename):
    try:
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        
        # Check for successful response
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

output = query("sample2.flac")
print(output)
