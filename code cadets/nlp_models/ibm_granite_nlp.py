import requests
import json
import os

class IBMLanguageModel:
    def __init__(self, api_key=None, service_url=None):
        self.api_key = api_key or os.getenv("IBM_GRANITE_API_KEY")
        self.service_url = service_url or os.getenv("IBM_GRANITE_API_URL")

        if not self.api_key or not self.service_url:
            raise ValueError("IBM Granite API key and/or service URL not provided or found in environment variables.")

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.auth = ("apikey", self.api_key)

    def analyze_text(self, text, model_id="ibm/granite-13b-instruct-v1", parameters=None):
        """
        Analyzes text using the IBM Granite NLP model to understand interaction context.
        """
        if not text:
            return None

        # Default parameters for the model
        if parameters is None:
            parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "min_new_tokens": 50,
                "repetition_penalty": 1.2
            }

        # Construct the prompt for interaction context understanding
        # This is a basic example; a more sophisticated prompt might be needed
        prompt = f"Analyze the following medical text for drug interaction context and potential implications: {text}\n\nInteraction analysis:"

        data = {
            "model_id": model_id,
            "input": prompt,
            "parameters": parameters
        }

        print(f"Sending request to IBM Granite NLP for text: '{text[:50]}...' ")
        try:
            response = requests.post(self.service_url, headers=self.headers, auth=self.auth, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()
            # Assuming the response structure contains 'results' and 'generated_text'
            if "results" in result and len(result["results"]) > 0:
                return result["results"][0]["generated_text"]
            else:
                print("No results found in IBM Granite NLP response.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling IBM Granite NLP API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response from IBM Granite NLP: {e}")
            return None

if __name__ == "__main__":
    # Example Usage:
    # Ensure IBM_GRANITE_API_KEY and IBM_GRANITE_API_URL are set in your environment
    # from dotenv import load_dotenv
    # load_dotenv()

    try:
        ibm_nlp = IBMLanguageModel()
        text_to_analyze = "Patient is currently taking Warfarin and was prescribed Ibuprofen. Assess potential interaction."
        analysis = ibm_nlp.analyze_text(text_to_analyze)
        if analysis:
            print("\nIBM Granite NLP Analysis:")
            print(analysis)
        else:
            print("Could not get analysis from IBM Granite NLP.")
    except ValueError as e:
        print(f"Initialization Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")