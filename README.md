# AI-Powered Inbound Contact Triage

A functional internal-tool prototype built with Python and Streamlit to process, classify, prioritize, and route incoming website inquiries to Sales or Technical Support.

The application combines a locally hosted LLM, rule-based business logic, and an outbound HTTP webhook.

> **Project scope:** This is a personal portfolio project developed and tested locally. It has not been deployed or used in a production Sales, Support, or CRM environment.

## Features

* **Contact form:** Collects customer information and an unstructured message through a Streamlit interface.
* **AI-assisted extraction:** Uses a locally hosted Llama 3.1 model through Ollama to extract information such as the customer’s city and number of TVs.
* **Rule-based routing:** Classifies inquiries as Standard Sales, High-Priority Sales, or Urgent Technical Support.
* **HTTP webhook:** Sends the processed contact information as a structured JSON payload to a configurable endpoint.
* **Live processing queue:** Displays recently processed contacts and their assigned classifications.

## Application Workflow

```text
Website inquiry
       |
       v
Streamlit form
       |
       v
Llama 3.1 data extraction
       |
       v
Rule-based classification
       |
       v
Structured JSON payload
       |
       v
HTTP webhook
       |
       v
Live processing queue
```
## Example

The following example shows how the application processes a simulated inbound website inquiry.

### Incoming Contact

```text
Name: Jordan Lee
Email: jordan@example.com

Message:
Hi, I manage a sports bar in Winnipeg with 18 TVs.
We are interested in learning more about the product and would like to schedule a demo.
```

### Extracted Information

The local Llama model analyzes the unstructured message and extracts the relevant operational data:

```text
City: Winnipeg
Number of TVs: 18
Request type: Sales inquiry
```

### Routing Decision

The application combines the extracted information with predefined business rules:

```text
Assigned department: Sales
Priority: High
Classification: High-Priority Sales
```

Because the contact represents a venue with a larger number of TVs, the inquiry is prioritized for the Sales team.

### Webhook Payload

The application converts the processed information into a structured JSON payload and sends it to the configured HTTP endpoint.

During development, the request was tested and inspected using Webhook.site.

```json
{
  "name": "Jordan Lee",
  "email": "jordan@example.com",
  "city": "Winnipeg",
  "tv_count": 18,
  "department": "Sales",
  "priority": "High",
  "classification": "High-Priority Sales",
  "message": "Hi, I manage a sports bar in Winnipeg with 18 TVs. We are interested in learning more about the product and would like to schedule a demo."
}
```

### Live Queue

After the webhook is sent, the processed contact appears in the application’s live history table.

```text
Jordan Lee | Winnipeg | 18 TVs | Sales | High-Priority Sales
```

> This example uses simulated contact information. The exact model output may vary, and the JSON field names should match the implementation in the application.

## Webhook Testing

The outbound HTTP webhook was tested using [Webhook.site](https://webhook.site).

Webhook.site provided a temporary endpoint that allowed the received HTTP request and JSON payload to be inspected and validated.

This project is not currently connected to Zapier, n8n, Salesforce, HubSpot, or another production CRM.

## Technologies

* Python
* Streamlit
* Ollama
* Llama 3.1
* HTTP webhooks
* JSON
* Rule-based workflow automation

## Prerequisites

Before running the project, install:

* Python 3.10 or later
* Git
* [Ollama](https://ollama.com)

## Installation

Clone the repository:

```bash
git clone https://github.com/PKpacheco/triage-inbound-lead-with-ai.git
cd triage-inbound-lead-with-ai
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS or Linux

```bash
source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Local LLM Setup

Pull the Llama 3.1 model through Ollama:

```bash
ollama pull llama3.1:8b
```

Make sure Ollama is running before starting the Streamlit application.

## Running the Application

Run:

```bash
streamlit run src/app.py
```

Streamlit will display the local application address in the terminal.

## Testing the Webhook

1. Open [Webhook.site](https://webhook.site).
2. Copy the unique URL generated for the session.
3. Paste the URL into the webhook field in the Streamlit application.
4. Submit a test inquiry.
5. Return to Webhook.site.
6. Inspect the received HTTP request and JSON payload.


## Current Limitations

* The application runs locally.
* Ollama must be installed and running locally.
* The project uses simulated contact information.
* It is not connected to a production CRM.
* The routing rules were created for demonstration purposes.
* Processing history is not stored permanently.
* The project has not been tested for production scalability, security, or reliability.

## Possible Improvements

* Add schema validation for LLM-generated output.
* Add automated tests for classification and routing rules.
* Add retry and error-handling logic for webhook failures.
* Store the processing history in a database.
* Add authentication and user roles.
* Connect the application to a CRM sandbox.
* Add human review for uncertain classifications.
* Generate suggested responses for common Sales and Support inquiries.
