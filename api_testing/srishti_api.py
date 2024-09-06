import requests
import json
import pygame

# Your Azure Translator API key and endpoint
api_key = '6e42b5ece252438c89ae74eb71162319'  # Replace this with your actual API key
endpoint = 'https://api.cognitive.microsofttranslator.com/translate'  # Add /translate to the endpoint

# Function to call Microsoft Translator API
def translate_text(text, target_language):
    # Specify the API URL with the parameters
    url = endpoint
    params = {
        'api-version': '3.0',
        'to': target_language
    }
    
    # Define the headers with API key and content type
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': 'centralindia',  # Replace with your region
        'Content-type': 'application/json'
    }
    
    # Create the request body with the text to translate
    body = [{'text': text}]
    
    # Make the request to the API
    response = requests.post(url, headers=headers, params=params, json=body)
    
    # Handle the response
    if response.status_code == 200:
        translated_text = response.json()[0]['translations'][0]['text']
        return translated_text
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage
translated = translate_text("Hello, World!", "hi")  # Translate to Hindi
print(translated)


# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Translator Integration")

# Load font
font = pygame.font.SysFont("arial", 24)

# Function to display text in Pygame window
def display_text(text, x, y):
    translated_text = translate_text(text, "hi")  # Translate to Hindi
    if translated_text:
        rendered_text = font.render(translated_text, True, (255, 255, 255))
        screen.blit(rendered_text, (x, y))
    else:
        rendered_text = font.render("Translation failed", True, (255, 0, 0))
        screen.blit(rendered_text, (x, y))

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black
    screen.fill((0, 0, 0))

    # Display translated text
    display_text("Hello, World!", 100, 100)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
