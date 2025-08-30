import requests
import os

class RxNormAPI:
    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    def __init__(self, api_key=None):
        # RxNorm API typically doesn't require an API key for basic searches,
        # but some advanced features or higher rate limits might. 
        # Including it for consistency with other APIs.
        self.api_key = api_key or os.getenv("RXNORM_API_KEY")

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        if params is None:
            params = {}
        
        # Add API key if it exists and is needed (though often not for RxNorm)
        if self.api_key:
            params['apiKey'] = self.api_key # This is a placeholder, check RxNav docs for actual param name

        print(f"Making request to: {url} with params: {params}")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling RxNorm API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return None

    def get_rxcui_by_name(self, drug_name):
        """
        Searches for an RxCUI (RxNorm Concept Unique Identifier) by drug name.
        """
        endpoint = "rxcui"
        params = {"name": drug_name}
        result = self._make_request(endpoint, params)
        if result and "idGroup" in result and "rxnormId" in result["idGroup"]:
            return result["idGroup"]["rxnormId"][0]
        return None

    def get_drug_properties(self, rxcui):
        """
        Gets properties for a given RxCUI.
        """
        endpoint = f"rxcui/{rxcui}/properties"
        result = self._make_request(endpoint)
        if result and "propConceptGroup" in result and "propConcept" in result["propConceptGroup"]:
            properties = {prop["propName"]: prop["propValue"] for prop in result["propConceptGroup"]["propConcept"]}
            return properties
        return None

    def get_related_concepts(self, rxcui, rela_source="ALL", rela="ALL"):
        """
        Gets related concepts for a given RxCUI.
        Useful for finding alternatives or related drug forms.
        """
        endpoint = f"rxcui/{rxcui}/related"
        params = {"relaSource": rela_source, "rela": rela}
        result = self._make_request(endpoint, params)
        if result and "resultSet" in result and "conceptGroup" in result["resultSet"]:
            return result["resultSet"]["conceptGroup"]
        return None

if __name__ == "__main__":
    # Example Usage:
    # from dotenv import load_dotenv
    # load_dotenv()

    rxnorm = RxNormAPI()

    # Example 1: Get RxCUI for Aspirin
    drug_name = "Aspirin"
    rxcui = rxnorm.get_rxcui_by_name(drug_name)
    if rxcui:
        print(f"\nRxCUI for {drug_name}: {rxcui}")

        # Example 2: Get properties of Aspirin
        properties = rxnorm.get_drug_properties(rxcui)
        if properties:
            print(f"Properties of {drug_name}:")
            for key, value in properties.items():
                print(f"  {key}: {value}")

        # Example 3: Get related concepts (e.g., alternatives or different forms)
        related_concepts = rxnorm.get_related_concepts(rxcui, rela="has_tradename")
        if related_concepts:
            print(f"\nRelated concepts for {drug_name}:")
            for group in related_concepts:
                print(f"  Concept Type: {group['conceptType']}")
                for concept in group['concept']:
                    print(f"    {concept['name']} (RxCUI: {concept['rxcui']})")
    else:
        print(f"Could not find RxCUI for {drug_name}")