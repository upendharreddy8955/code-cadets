# AI Medical Prescription Verification Leveraging IBM Granite and Hugging Face Models

This project aims to analyze drug interactions, identify correct drug dosages, and provide safe alternative medication options based on age and drug details. It integrates multiple datasets and leverages advanced NLP models and APIs for accurate drug information extraction and interaction understanding. The system is built with a FastAPI backend and a Streamlit frontend for easy user interaction.

## Features

- **Drug Interaction Analysis**: Identify potential adverse drug interactions.
- **Dosage Verification**: Ensure correct drug dosages based on patient and drug details.
- **Alternative Medication Suggestions**: Provide safe alternative medication options.
- **NLP-powered Information Extraction**: Utilize Hugging Face and IBM Granite models for extracting drug names, dosages, and understanding interaction context.
- **API Integration**: Seamlessly integrate with RxNorm for drug mapping and other relevant APIs.
- **User-friendly Interface**: A Streamlit frontend for easy interaction and visualization.

## Project Flow

### Milestone 1: Data Acquisition and Integration
- Activity 1.1: Dataset Download
- Activity 1.2: Dataset mapping and Preparation

### Milestone 2: NLP Model Integration for Drug Extraction and Interaction Understanding
- Activity 2.1: Named Entity Recognition (NER) using Hugging Face models.
- Activity 2.2: IBM Granite NLP for Interaction Context.
- Activity 2.3: Integration of both models.

### Milestone 3: Dosage Verification and Alternative Recommendations
- Activity 3.1: RxNorm API Usage for drug mapping and dosage information.
- Activity 3.2: Alternative Safe Drug Suggestions based on age and drug details.

### Milestone 4: Backend and Frontend Development
- Activity 4.1: FastAPI Backend for API endpoints and business logic.
- Activity 4.2: Streamlit Frontend for user interaction and data visualization.

## Installation Guide

### Prerequisites
- Python 3.8+
- Hugging Face API Key (for `samant/medical-ner` model)
- IBM Granite NLP API Key and URL
- RxNorm API Keys

### Setup Steps

1. **Clone the repository (if applicable)**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (A `requirements.txt` file will be created in a later step.)

### 5. Set up API Keys
   Create a `.env` file in the root directory of the project and add your API keys:
   ```
   HUGGING_FACE_API_KEY=your_hugging_face_api_key
   IBM_GRANITE_API_KEY=your_ibm_granite_api_key
   IBM_GRANITE_API_URL=your_ibm_granite_api_url
   RXNORM_API_KEY=your_rxnorm_api_key
   ```

**Note**: The `nlp_models` directory contains scripts for NLP functionalities, including Named Entity Recognition (NER) using Hugging Face models and IBM Granite NLP. The `api_clients` directory contains scripts for interacting with external APIs like RxNorm. Ensure your `HUGGING_FACE_API_KEY`, `IBM_GRANITE_API_KEY`, `IBM_GRANITE_API_URL`, and `RXNORM_API_KEY` are correctly set in the `.env` file for the models and APIs to function properly.

## Usage

### 1. Download Datasets

To download the necessary datasets, run the `download_datasets.py` script:

```bash
python scripts/download_datasets.py
```

**Note**: You will need to update the `datasets` list in `scripts/download_datasets.py` with the actual URLs of the datasets you intend to use.

### 2. Prepare Datasets

After downloading, prepare the datasets by running the `prepare_datasets.py` script:

```bash
python scripts/prepare_datasets.py
```

**Note**: You will need to update the `datasets_to_process` list in `scripts/prepare_datasets.py` with the names of the downloaded files you wish to process.

### 3. Run the FastAPI Backend

To run the FastAPI backend, navigate to the `backend` directory and execute:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API documentation will be available at `http://localhost:8000/docs`.

### 4. Run the Streamlit Frontend

To run the Streamlit frontend, navigate to the `frontend` directory and execute:

```bash
cd frontend
streamlit run app.py
```

The Streamlit application will open in your web browser.

## Contributing

(Guidelines for contributing to the project will be added here.)

## License

(License information will be added here.)