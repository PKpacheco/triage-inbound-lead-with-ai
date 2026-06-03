# Internal Operations Hub

This project is an internal tool built with Python and Streamlit. It automatically organizes and routes incoming website contacts to the correct internal department (Sales or Support).

## What This App Does

* **Reads the Form:** Ingests the customer's contact information and raw text message.
* **Cleans the Data:** Extracts the customer's city and counts how many TVs they have (using Python and a local LLM via Ollama/Llama).
* **Routes the Lead:** Categorizes contacts into Standard Sales, High-Priority Sales, or Urgent Technical Support.
* **Dispatches a Webhook:** Sends the clean, structured JSON data to an external URL (like Zapier or n8n) to update the CRM.
* **Displays a Live Queue:** Keeps track of processed contacts in a real-time history table at the bottom of the page.

---

## How to Run the Project

### Prerequisites
* Python installed
* Ollama running locally

### Step-by-Step Setup
1. Clone or download this repository to your computer.
2. Open your terminal in the project folder and create a virtual environment:
   ```bash
   python -m venv venv


### Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run src/app.py
```

4. For **Local Llama** mode, install [Ollama](https://ollama.com), keep it running, and pull the model:

```bash
ollama pull llama3.1:8b
```