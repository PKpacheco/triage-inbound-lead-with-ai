# Main Streamlit Interface

import time
import streamlit as st
from demo.scenarios.scenarios import SCENARIOS
from services.pipeline import execute_triage_pipeline

st.set_page_config(page_title="Ops Automation Center", layout="wide")
st.title("Internal Operations Hub")
st.markdown("##### Production-ready infrastructure built for Lead Triage and Workflow Automation.")
st.markdown("---")

# initialize the session state
if "ops_queue" not in st.session_state:
    st.session_state["ops_queue"] = []
if "business_name_input" not in st.session_state:
    st.session_state["first_name"] = "John"
    st.session_state["last_name"] = "Smith"
    st.session_state["email_address"] = "john@sportsbar.com"
    st.session_state["cell_number"] = "+1 204-555-0199"
    st.session_state["business_name_input"] = "Kobi Sports Venue"
    st.session_state["business_address"] = "22 St James St, Boston"
    st.session_state["message_text"] = "I am interested to understand more about the product."

# side menu - settings
st.sidebar.markdown("### System Settings")
config_mode = st.sidebar.radio("Choose Environment:", ["Mock Mode (Simulated Test)", "Local LLM (Real AI Connection)"])
st.sidebar.markdown("---")
st.sidebar.markdown("### Workflow Integration")
webhook_url = st.sidebar.text_input("Target Webhook URL:", value="https://example")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Step 1: Inbound Lead Triage Form")
    st.markdown("**Quick Demo Scenarios (Click to load):**")
    
    # dynamic rendering of the scenario buttons with for loop
    btn_cols = st.columns(3)
    for col, key in zip(btn_cols, SCENARIOS.keys()):
        with col:
            if st.button(SCENARIOS[key]["button_label"], use_container_width=True):
                for field in ["first_name", "last_name", "email_address", "cell_number", "address", "message"]:
                    # map the dictionary keys to the st.session_state keys
                    state_key = "business_name_input" if field == "business_name" else field
                    state_key = "message_text" if field == "message" else state_key
                    st.session_state[state_key] = SCENARIOS[key][field]

    st.markdown("---")
    
    # visual inputs for the form
    first_name = st.text_input("First Name", key="first_name")
    last_name = st.text_input("Last Name", key="last_name")
    email_address = st.text_input("Email Address", key="email_address")
    cell_number = st.text_input("Cell Number", key="cell_number")
    business_name_input = st.text_input("Business Name", key="business_name_input")
    business_address = st.text_input("Business Address", key="business_address")
    message_text = st.text_area("User Message", key="message_text", height=140)
    
    execute_pipeline = st.button("Run Automation Pipeline", type="primary", use_container_width=True)

with col_right:
    st.markdown("### Step 2: Live Processing & Telemetry")
    
    if execute_pipeline:
        st.markdown("**[System Log]** Extracting elements and triggering service pipeline...")
        
        # build the data package to send to the service file
        raw_form_data = {
            "first_name": first_name, "last_name": last_name, "email": email_address,
            "phone": cell_number, "business_name": business_name_input,
            "address": business_address, "message": message_text
        }
        
        # call the separated function
        with st.spinner("Processing pipeline telemetry..."):
            result_payload = execute_triage_pipeline(raw_form_data, config_mode, webhook_url)
        
        # save in the table of logs on the screen
        st.session_state["ops_queue"].append({
            "Timestamp": time.strftime("%H:%M:%S"),
            "Company": result_payload["company"]["company_name"],
            "City": result_payload["company"]["city"],
            "TVs": result_payload["company"]["hardware_count_tv"],
            "Routing Queue": result_payload["deal_routing"]["target_operational_queue"],
            "SLA Urgent": "YES" if result_payload["deal_routing"]["requires_immediate_sla"] else "Standard"
        })
        
        st.success("Pipeline Executed & Webhook Dispatched!")
        st.json(result_payload)
    else:
        st.info("Awaiting pipeline trigger event.")

# lower operational panel
st.markdown("---")
st.markdown("### Active Operations Monitoring Queue")
if st.session_state["ops_queue"]:
    st.table(st.session_state["ops_queue"])
    if st.button("Clear Queue History", type="secondary"):
        st.session_state["ops_queue"] = []
        st.rerun()
else:
    st.caption("No operations data in the active session log. Run the form pipeline above to stream data.")