import requests
import json
# Replace with your API key and endpoint from Azure
API_KEY = '6e42b5ece252438c89ae74eb71162319'
ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
LOCATION = 'southeastasia'  # e.g., 'westeurope', 'eastus', etc.


# Dictionary of common regional Indian languages and their codes
INDIAN_LANGUAGES = {
    '1': ('Hindi', 'hi'),
    '2': ('Bengali', 'bn'),
    '3': ('Gujarati', 'gu'),
    '4': ('Kannada', 'kn'),
    '5': ('Malayalam', 'ml'),
    '6': ('Marathi', 'mr'),
    '7': ('Punjabi', 'pa'),
    '8': ('Tamil', 'ta'),
    '9': ('Telugu', 'te'),
    '10': ('Urdu', 'ur'),
    '11': ('Assamese', 'as'),
    '12': ('Odia', 'or'),
    '13': ('Konkani', 'kok'),
    '14': ('Maithili', 'mai'),
    '15': ('Sindhi', 'sd'),
    '16': ('Nepali', 'ne'),
    '17': ('Sanskrit', 'sa'),
    # Add more languages if needed
}

# Function to display available languages
def display_languages():
    print("Please choose a language:")
    for key, (name, _) in INDIAN_LANGUAGES.items():
        print(f"{key}: {name}")

# Function to call the Microsoft Translator API
def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    target_language_param = f'&to={target_language}'
    constructed_url = ENDPOINT + path + target_language_param

    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Ocp-Apim-Subscription-Region': LOCATION,
        'Content-type': 'application/json'
    }

    body = [{'text': text}]

    # Make the request to the API
    response = requests.post(constructed_url, headers=headers, json=body)

    # Parse the JSON response
    if response.status_code == 200:
        translation = response.json()
        translated_text = translation[0]['translations'][0]['text']
        return translated_text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Main program
def main():
    display_languages()
    choice = input("Enter the number of your choice: ")

    if choice in INDIAN_LANGUAGES:
        language_name, language_code = INDIAN_LANGUAGES[choice]
        text_to_translate = input(f"Enter the text to translate into {language_name}: ")
        translated_text = translate_text(text_to_translate, language_code)
        print(f"Translated text in {language_name}: {translated_text}")
    else:
        print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
