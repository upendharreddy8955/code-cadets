import streamlit as st
import requests
import os

# FastAPI backend URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Medical Prescription Verification", layout="wide")

st.title("💊 AI Medical Prescription Verification System")
st.markdown("---")

# --- Sidebar for Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Prescription Verification", "Dosage Verification", "Alternative Suggestions"])

# --- Prescription Verification Page ---
if page == "Prescription Verification":
    st.header("📝 Prescription Verification")
    st.write("Analyze your prescription text to extract entities and understand potential drug interactions.")

    prescription_text = st.text_area("Enter Prescription Text:", height=150, help="e.g., Take 10mg of Amoxicillin twice a day for 7 days. Also, take 500mg of Paracetamol as needed.")
    patient_age_pv = st.number_input("Patient Age (optional, for context):", min_value=0, max_value=120, value=None, format="%d", help="Enter patient's age for more accurate interaction analysis.")

    if st.button("Analyze Prescription"): 
        if prescription_text:
            with st.spinner("Analyzing prescription..."):
                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/verify_prescription",
                        json={
                            "prescription_text": prescription_text,
                            "patient_age": patient_age_pv
                        }
                    )
                    response.raise_for_status() # Raise an exception for HTTP errors
                    result = response.json()

                    st.subheader("Analysis Results:")
                    st.json(result)

                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the FastAPI backend. Please ensure it is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred during the request: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter prescription text to analyze.")

# --- Dosage Verification Page ---
elif page == "Dosage Verification":
    st.header("⚖️ Dosage Verification")
    st.write("Verify if a specific drug dosage is within a safe range based on patient age.")

    drug_name_dv = st.text_input("Drug Name:", help="e.g., Amoxicillin")
    dosage_dv = st.text_input("Dosage:", help="e.g., 10mg, 500mg")
    patient_age_dv = st.number_input("Patient Age:", min_value=0, max_value=120, help="Enter patient's age for dosage verification.")

    if st.button("Verify Dosage"): 
        if drug_name_dv and dosage_dv and patient_age_dv is not None:
            with st.spinner("Verifying dosage..."):
                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/verify_dosage",
                        json={
                            "drug_name": drug_name_dv,
                            "dosage": dosage_dv,
                            "patient_age": patient_age_dv
                        }
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.subheader("Dosage Verification Results:")
                    st.json(result)

                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the FastAPI backend. Please ensure it is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred during the request: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please fill in all fields for dosage verification.")

# --- Alternative Suggestions Page ---
elif page == "Alternative Suggestions":
    st.header("🔄 Alternative Medication Suggestions")
    st.write("Find alternative safe drug options for a given medication, considering patient age.")

    drug_name_as = st.text_input("Drug Name for Alternatives:", help="e.g., Ibuprofen")
    patient_age_as = st.number_input("Patient Age:", min_value=0, max_value=120, help="Enter patient's age for alternative suggestions.")

    if st.button("Suggest Alternatives"): 
        if drug_name_as and patient_age_as is not None:
            with st.spinner("Searching for alternatives..."):
                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/suggest_alternatives",
                        json={
                            "drug_name": drug_name_as,
                            "patient_age": patient_age_as
                        }
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.subheader("Alternative Suggestions:")
                    st.json(result)

                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the FastAPI backend. Please ensure it is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred during the request: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter the drug name and patient age for alternative suggestions.")


st.markdown("--- ")
st.info("Note: This system is for informational purposes only and should not replace professional medical advice.")