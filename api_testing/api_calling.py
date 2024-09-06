import requests
import json
# Replace with your API key and endpoint from Azure
API_KEY = '6e42b5ece252438c89ae74eb71162319'
ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
LOCATION = 'southeastasia'  # e.g., 'westeurope', 'eastus', etc.

# Function to call the Microsoft Translator API
def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    target_language_param = f'&to={target_language}'
    constructed_url = ENDPOINT + path + target_language_param

    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Ocp-Apim-Subscription-Region': LOCATION,  # Region of your resource
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    # Make the request to the API
    response = requests.post(constructed_url, headers=headers, json=body)

    # Parse the JSON response
    if response.status_code == 200:
        translation = response.json()
        translated_text = translation[0]['translations'][0]['text']
        return translated_text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
translated_text = translate_text("Hello, how are you?", "es")  # 'es' for Spanish
print(f"Translated text: {translated_text}")
