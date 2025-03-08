# Generative AI - Audit Tools

A Streamlit-based web application that uses Google's Generative AI (Gemini) to analyze SOP and Work Instruction documents in PDF format.

## Features

- PDF document upload (multiple files supported)
- Automated analysis of documents using Gemini AI
- Extraction of key information including:
  1. Process & Activities
  2. Controls
  3. Risks
  4. Documents and Data
  5. Process Dependencies
  6. Supporting Applications
  7. ICOFR

## Prerequisites

- Python 3.9 or higher
- Google Cloud API key for Gemini
- Docker (for containerization)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd genai-audit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

1. Set up your Google Cloud API key
2. Run the Streamlit application:
```bash
streamlit run app.py
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t gcr.io/[YOUR-PROJECT-ID]/genai-audit .
```

2. Run locally with Docker:
```bash
docker run -p 8080:8080 gcr.io/[YOUR-PROJECT-ID]/genai-audit
```

## Google Cloud Run Deployment

1. Push the image to Google Container Registry:
```bash
docker push gcr.io/[YOUR-PROJECT-ID]/genai-audit
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy genai-audit --image gcr.io/[YOUR-PROJECT-ID]/genai-audit --platform managed
```

## Environment Variables

- `PORT`: Default is 8080 (set in Dockerfile)
- Google Cloud API key should be configured in your deployment environment

## Project Structure

```
genai-audit/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
```

## Usage

1. Access the web interface
2. Upload PDF documents using the sidebar
3. Customize the analysis prompt if needed
4. Click "Process LLM" to generate analysis
5. Download results in Markdown format

## Security Notes

- Ensure proper security measures when handling sensitive documents
- Store API keys securely in production environments
- Configure appropriate authentication for Cloud Run deployment
