import json
import ollama

def run_llama_triage(inbound_payload, detected_tv_count):
    system_prompt = (
        "You are an automated operations assistant routing data.\n"
        "Analyze the text and extract fields into a clean JSON structure.\n"
        "If no TVs are mentioned in the text, you must return null for tv_count.\n"
        "Return ONLY raw JSON, no extra text conversational phrases."
    )

    response = ollama.chat(
        model="llama3",
        format="json",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(inbound_payload)}
        ]
    )

    raw_content = response['message']['content'].strip()
    return json.loads(raw_content)