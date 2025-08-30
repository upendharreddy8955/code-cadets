from .ner_model import NERModel
from .ibm_granite_nlp import IBMLanguageModel
from .ner_model import NERModel
import os

class NLPIntegrator:
    def __init__(self):
        self.ner_model = None
        self.ibm_nlp_model = None
        
        try:
            self.ner_model = NERModel()
            print("NERModel initialized successfully.")
        except ValueError as e:
            print(f"Warning: Could not initialize NERModel: {e}")
        
        try:
            self.ibm_nlp_model = IBMLanguageModel()
            print("IBMLanguageModel initialized successfully.")
        except ValueError as e:
            print(f"Warning: Could not initialize IBMLanguageModel: {e}")

    def analyze_prescription(self, prescription_text):
        """
        Analyzes a prescription text using both NER and IBM Granite NLP.
        Returns extracted entities and interaction analysis.
        """
        extracted_entities = []
        interaction_analysis = None

        if self.ner_model:
            print("Performing Named Entity Recognition...")
            extracted_entities = self.ner_model.extract_entities(prescription_text)
        else:
            print("NERModel not available. Skipping entity extraction.")

        if self.ibm_nlp_model:
            print("Performing IBM Granite NLP interaction analysis...")
            interaction_analysis = self.ibm_nlp_model.analyze_text(prescription_text)
        else:
            print("IBMLanguageModel not available. Skipping interaction analysis.")

        return {
            "extracted_entities": extracted_entities,
            "interaction_analysis": interaction_analysis
        }

if __name__ == "__main__":
    # Example Usage:
    # Ensure environment variables (HUGGING_FACE_API_KEY, IBM_GRANITE_API_KEY, IBM_GRANITE_API_URL) are set.
    # from dotenv import load_dotenv
    # load_dotenv()

    try:
        integrator = NLPIntegrator()
        test_prescription = "Patient is prescribed 20mg of Lipitor daily and 5mg of Amlodipine. Also taking St. John's Wort."
        analysis_results = integrator.analyze_prescription(test_prescription)

        print("\n--- Integrated Analysis Results ---")
        print("Extracted Entities:")
        for entity in analysis_results["extracted_entities"]:
            print(entity)
        
        print("\nInteraction Analysis:")
        print(analysis_results["interaction_analysis"])

    except Exception as e:
        print(f"An error occurred during integration: {e}")