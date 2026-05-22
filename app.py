import os
import json
import time
import streamlit as st
import ollama

st.set_page_config(page_title="Ops Automation Center",  layout="centered")

st.title(" Inbound Lead Triage Automation")
st.markdown("##### Internal tool for structuring and qualifying incoming sales emails.")
st.markdown("---")

# 1. ENVIRONMENT CONFIGURATION
st.markdown("### 1. Environment Configuration")
config_mode = st.radio(
    "Choose Environment Mode:",
    ["Mock Mode (No Setup Required)", "Local Llama (Via Ollama)"]
)

# 2. INPUT AREA
st.markdown("### 2. Paste Incoming Lead Email")
default_email = (
    "Hey sales team! I'm John, manager at a local Sports Bar in Winnipeg. "
    "We have 22 TVs and we are looking for a way to automate our commercial breaks "
    "before the next season starts. Can someone call me?"
)
email_text = st.text_area("Email Content:", value=default_email, height=150)

# 3. PROCESS PIPELINE
if st.button("Run AI Triage Check", type="primary"):
    
    # ---- SCENARIO 1: MOCK MODE ----
    if "Mock Mode" in config_mode:
        with st.spinner("[MOCK MODE] Simulating AI analysis..."):
            time.sleep(1.2)
            mock_json_response = {
                "business_name": "Local Sports Bar",
                "city": "Winnipeg",
                "tv_count": 22,
                "category": "High Priority"
            }
            st.success("Analysis Complete (Mock Mode)!")
            st.warning("**Attention Sales:** This is a High Priority Lead!")
            st.json(mock_json_response)
            
    # ---- SCENARIO 2: LOCAL LLAMA (OLLAMA) ----
    else:
        try:
            with st.spinner("Local Llama is analyzing the email and structuring data..."):
                
                system_prompt = (
                    "You are an automated operations assistant for a B2B tech company.\n"
                    "Analyze the inbound email from a business lead and extract the following data in strict JSON format:\n"
                    "- business_name (string)\n"
                    "- city (string)\n"
                    "- tv_count (integer, or null if not mentioned)\n"
                    "- category (if the venue has more than 10 TVs or has a sports focus, "
                    "classify as 'High Priority', otherwise 'Standard')\n"
                    "Return ONLY a clean JSON object. Do not include markdown code block formatting."
                )

                # direct call to local Ollama server
                response = ollama.chat(
                    model="llama3.1:8b",
                    format="json",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": email_text}
                    ]
                )

                raw_content = response['message']['content'].strip()
                extracted_data = json.loads(raw_content)
                
                st.success("Local Analysis Complete!")
                if extracted_data.get("category") == "High Priority":
                    st.warning("**Attention Sales:** This is a High Priority Lead!")
                else:
                    st.info("**Standard Lead:** Added to the regular queue.")
                
                st.markdown("### Structured Payload (Ready for HubSpot CRM)")
                st.json(extracted_data)
                
        except Exception as e:
            st.error(
                f"Could not connect to local Llama. Make sure Ollama app is open on your Mac! "
                f"Error details: {str(e)}"
            )