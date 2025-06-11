# gemini_core.py

import vertexai
from vertexai.generative_models import GenerativeModel

def call_gemini(project_id: str, location: str, prompt: str) -> str:
    """
    A foundational function to send a prompt to the Gemini model in Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Cloud location (e.g., "us-central1").
        prompt: The text prompt to send to the model.

    Returns:
        The text response from the model.
    """
    # Initialize the Vertex AI SDK for your project and location
    vertexai.init(project=project_id, location=location)

    # Load the specific Gemini model you want to use
    # "gemini-1.5-pro-preview-0409" is a great, powerful choice for coding
    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    # The model.generate_content() method sends the prompt to the API
    try:
        response = model.generate_content(prompt)
        # Return the text part of the response
        return response.text
    except Exception as e:
        # Basic error handling
        print(f"An error occurred while calling the API: {e}")
        return ""

# This block allows us to test the function by running this file directly
if __name__ == '__main__':
    # --- IMPORTANT: CONFIGURE YOUR DETAILS HERE ---
    # 1. Get your Project ID from the Google Cloud Console or by running `gcloud config get-value project`
    my_project_id = "your-gcp-project-id"  # <--- CHANGE THIS

    # 2. This is a common location for Vertex AI, you can usually leave it as is.
    my_location = "us-central1"

    # 3. This is our test prompt for the model.
    my_test_prompt = "Write a simple Python function that returns the factorial of a number."
    
    # --- SCRIPT EXECUTION ---
    print("--- Testing Connection to Gemini API ---")
    
    if my_project_id == "your-gcp-project-id":
        print("\n!!! ERROR: Please update 'my_project_id' in the script with your real Google Cloud Project ID.")
    else:
        print(f"Project: {my_project_id}, Location: {my_location}")
        print(f"Sending prompt: '{my_test_prompt}'")
        print("\n...waiting for response...")

        # Call our function
        gemini_response = call_gemini(
            project_id=my_project_id,
            location=my_location,
            prompt=my_test_prompt
        )
        
        print("\n--- Gemini's Response ---")
        print(gemini_response)
        print("-------------------------\n")
        if gemini_response:
            print("Success! Your connection to the Gemini API is working.")
        else:
            print("Failed to get a response. Please check your Project ID, and ensure the Vertex AI API is enabled.")