from api_clients.rxnorm_api import RxNormAPI
import pandas as pd

class DrugSuggester:
    def __init__(self):
        self.rxnorm_api = RxNormAPI()
        # In a real application, you might load age-specific drug data here
        # For now, we'll use a placeholder or rely on RxNorm's related concepts.

    def suggest_alternatives(self, drug_name, patient_age=None):
        """
        Suggests alternative safe drug options based on the given drug name and patient age.
        This is a simplified example. A real-world system would require extensive medical knowledge bases.
        """
        print(f"Suggesting alternatives for {drug_name} (Age: {patient_age})...")
        rxcui = self.rxnorm_api.get_rxcui_by_name(drug_name)
        alternatives = []

        if rxcui:
            # Get related concepts that might be alternatives (e.g., different forms, similar drugs)
            # The 'rela' parameter can be tuned for more specific relationships
            related_concepts_groups = self.rxnorm_api.get_related_concepts(rxcui, rela="has_precise_ingredient")
            if related_concepts_groups:
                for group in related_concepts_groups:
                    if "concept" in group:
                        for concept in group["concept"]:
                            # Filter out the original drug itself
                            if concept["name"].lower() != drug_name.lower():
                                alternatives.append({
                                    "name": concept["name"],
                                    "rxcui": concept["rxcui"],
                                    "type": group["conceptType"]
                                })
            
            # Placeholder for age-based filtering/suggestions
            if patient_age:
                print(f"Applying age-based considerations for age {patient_age} (placeholder).")
                # In a real system, this would involve checking contraindications or preferred drugs for age groups.
                # For example, if drug is not suitable for children, filter it out if patient_age < 18.

        return alternatives

    def verify_dosage(self, drug_name, dosage, patient_age=None):
        """
        Verifies if a given dosage is within a safe range for a drug and patient age.
        This is a highly simplified placeholder and requires a comprehensive dosage database.
        """
        print(f"Verifying dosage for {drug_name} ({dosage}) for age {patient_age} (placeholder)...")
        # In a real system, this would involve:
        # 1. Looking up standard dosage ranges for the drug.
        # 2. Adjusting ranges based on patient factors like age, weight, kidney function.
        # 3. Comparing the given dosage to the safe range.
        
        # For demonstration, assume a generic safe range for 'Aspirin'
        if "aspirin" in drug_name.lower():
            if "mg" in dosage.lower():
                try:
                    value = float(dosage.lower().replace('mg', '').strip())
                    if 50 <= value <= 1000: # Example safe range for adult aspirin dose
                        return True, "Dosage appears to be within typical adult range."
                    else:
                        return False, "Dosage outside typical adult range. Consult a physician."
                except ValueError:
                    return False, "Could not parse dosage value."
        
        return True, "Dosage verification not implemented for this drug or general range assumed safe."

if __name__ == "__main__":
    # Example Usage:
    # from dotenv import load_dotenv
    # load_dotenv()

    suggester = DrugSuggester()

    # Example 1: Suggest alternatives for Aspirin
    drug = "Aspirin"
    age = 30
    alternatives = suggester.suggest_alternatives(drug, age)
    print(f"\nAlternatives for {drug} (Age: {age}):")
    if alternatives:
        for alt in alternatives:
            print(f"- {alt['name']} (RxCUI: {alt['rxcui']}, Type: {alt['type']})")
    else:
        print("No direct alternatives found or implemented.")

    # Example 2: Verify dosage
    drug_to_verify = "Aspirin"
    dosage_to_verify = "500mg"
    is_safe, message = suggester.verify_dosage(drug_to_verify, dosage_to_verify, age)
    print(f"\nDosage verification for {drug_to_verify} ({dosage_to_verify}): {is_safe} - {message}")

    drug_to_verify_2 = "Aspirin"
    dosage_to_verify_2 = "2000mg"
    is_safe_2, message_2 = suggester.verify_dosage(drug_to_verify_2, dosage_to_verify_2, age)
    print(f"Dosage verification for {drug_to_verify_2} ({dosage_to_verify_2}): {is_safe_2} - {message_2}")