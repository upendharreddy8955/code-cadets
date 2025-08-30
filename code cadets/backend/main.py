from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

# Import custom modules
from nlp_models.nlp_integrator import NLPIntegrator
from scripts.drug_suggestions import DrugSuggester

app = FastAPI(
    title="AI Medical Prescription Verification API",
    description="API for analyzing drug interactions, verifying dosages, and suggesting alternatives.",
    version="1.0.0"
)

# Initialize NLP and Drug Suggester components
try:
    nlp_integrator = NLPIntegrator()
except ValueError as e:
    print(f"Failed to initialize NLPIntegrator: {e}. Some functionalities might be limited.")
    nlp_integrator = None

try:
    drug_suggester = DrugSuggester()
except Exception as e:
    print(f"Failed to initialize DrugSuggester: {e}. Some functionalities might be limited.")
    drug_suggester = None

class PrescriptionRequest(BaseModel):
    prescription_text: str
    patient_age: int = None

class DosageVerificationRequest(BaseModel):
    drug_name: str
    dosage: str
    patient_age: int = None

class AlternativeSuggestionRequest(BaseModel):
    drug_name: str
    patient_age: int = None

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the AI Medical Prescription Verification API"}

@app.post("/verify_prescription", tags=["Prescription Verification"])
async def verify_prescription(request: PrescriptionRequest):
    """
    Analyzes a given prescription text for drug interactions and extracts entities.
    """
    if not nlp_integrator:
        raise HTTPException(status_code=503, detail="NLP services are not available.")
    
    analysis_results = nlp_integrator.analyze_prescription(request.prescription_text)
    return {
        "prescription_text": request.prescription_text,
        "extracted_entities": analysis_results["extracted_entities"],
        "interaction_analysis": analysis_results["interaction_analysis"]
    }

@app.post("/verify_dosage", tags=["Dosage Verification"])
async def verify_dosage(request: DosageVerificationRequest):
    """
    Verifies if a given drug dosage is within a safe range.
    """
    if not drug_suggester:
        raise HTTPException(status_code=503, detail="Drug suggestion services are not available.")

    is_safe, message = drug_suggester.verify_dosage(
        request.drug_name, request.dosage, request.patient_age
    )
    return {
        "drug_name": request.drug_name,
        "dosage": request.dosage,
        "patient_age": request.patient_age,
        "is_safe": is_safe,
        "message": message
    }

@app.post("/suggest_alternatives", tags=["Alternative Suggestions"])
async def suggest_alternatives(request: AlternativeSuggestionRequest):
    """
    Suggests alternative safe drug options for a given drug.
    """
    if not drug_suggester:
        raise HTTPException(status_code=503, detail="Drug suggestion services are not available.")

    alternatives = drug_suggester.suggest_alternatives(
        request.drug_name, request.patient_age
    )
    return {
        "original_drug": request.drug_name,
        "patient_age": request.patient_age,
        "suggested_alternatives": alternatives
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)