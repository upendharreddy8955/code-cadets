from transformers import pipeline
import os

class NERModel:
    def __init__(self, model_name="samant/medical-ner", api_key=None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("HUGGING_FACE_API_KEY")
        if not self.api_key:
            raise ValueError("Hugging Face API key not provided or found in environment variables.")
        
        # Initialize the Hugging Face pipeline for NER
        # For local inference, you might download the model first.
        # For API-based inference, you'd typically use requests to call the API endpoint.
        # This example assumes a local pipeline for simplicity, but notes API usage.
        try:
            self.nlp = pipeline("ner", model=self.model_name, token=self.api_key)
        except Exception as e:
            print(f"Error initializing NER pipeline: {e}")
            print("Attempting to initialize without token (might fail for private models or rate limits).")
            self.nlp = pipeline("ner", model=self.model_name)

    def extract_entities(self, text):
        """
        Extracts named entities (e.g., drug names, dosages) from the given text.
        """
        if not hasattr(self, 'nlp'):
            print("NER pipeline not initialized. Cannot extract entities.")
            return []
        
        print(f"Extracting entities from text: '{text}'")
        entities = self.nlp(text)
        extracted_data = []
        for entity in entities:
            extracted_data.append({
                "entity": entity["entity"],
                "score": entity["score"],
                "word": entity["word"],
                "start": entity["start"],
                "end": entity["end"]
            })
        return extracted_data

if __name__ == "__main__":
    # Example Usage:
    # Ensure HUGGING_FACE_API_KEY is set in your environment or passed directly
    # For testing, you might need to install python-dotenv and load it:
    # from dotenv import load_dotenv
    # load_dotenv()

    try:
        ner_extractor = NERModel()
        text = "Patient was prescribed 10mg of Aspirin daily and 500mg of Paracetamol twice a day."
        extracted_entities = ner_extractor.extract_entities(text)
        print("\nExtracted Entities:")
        for entity in extracted_entities:
            print(entity)
    except ValueError as e:
        print(f"Initialization Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")