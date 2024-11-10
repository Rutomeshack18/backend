import requests

api_url = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {
    "Authorization": "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"
}

# Replace this with a test case's text
text = "This is a sample text that I want to summarize."

# Send the request
response = requests.post(api_url, headers=headers, json={"inputs": text})

print("Response Status:", response.status_code)
print("Response Body:", response.text)