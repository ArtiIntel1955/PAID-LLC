import requests
import json

# Test the local Ollama API
def test_ollama():
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3.2:3b",
        "prompt": "Can you explain operating income optimization strategies for Fortune 500 retailers?",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            print("Success! Response received:")
            print(result.get('response', 'No response text found'))
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_ollama()