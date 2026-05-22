# AI Powered Inbound Lead Triage Automation

### Problem 
In fast-growing B2B tech and smart-hardware startups, sales operations often face a major bottleneck: manually screening hundreds of inbound emails from business owners to qualify if they have the right profile (e.g., venue size, number of displays) before booking a sales demo.

### Solution
A lightweight Streamlit app for internal business operations. It intercepts incoming unstructured customer emails, uses local **Llama 3.1** (via [Ollama](https://ollama.com)) with strict JSON output to structure the text, automatically scores the lead's priority based on business criteria, and prepares the payload for CRM integration (HubSpot/Salesforce). A mock mode is included so you can demo the workflow without running a model.

### 🏗️ Why this Architecture?
Built adhering to the YAGNI principle (*You Aren't Gonna Need It*). In rapid-growth environments, business qualification rules change weekly. Instead of engineering heavy infrastructure, this prompt-driven micro-tool delivers immediate business value to internal operations teams with minimal maintenance and high flexibility.


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
streamlit run app.py
```

4. (Optional) For **Local Llama** mode, install [Ollama](https://ollama.com), keep it running, and pull the model:

```bash
ollama pull llama3.1:8b
```