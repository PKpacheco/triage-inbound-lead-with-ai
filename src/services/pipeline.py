# Pipeline Service Layer
import time
import requests
import skills
import ai_agent

def execute_triage_pipeline(form_data: dict, config_mode: str, webhook_url: str) -> dict:
    """
    process the raw form data, run the business rules
    and dispatch the webhook in real time.
    """
    # 1. execute the helper functions (Skills)
    detected_tv_count = skills.tool_extract_tv_count(form_data["message"])
    detected_city = skills.tool_extract_city(form_data["address"])
    
    # 2. processing (Mock or real AI)
    if "Mock Mode" in config_mode:
        time.sleep(0.4)
        msg_lower = form_data["message"].lower()
        if "partnership" in msg_lower or "enterprise" in msg_lower:
            routing_queue = "Strategic Accounts"
            lead_category = "Enterprise Prospect"
            is_alert = False
        elif "offline" in msg_lower or "cancel" in msg_lower:
            routing_queue = "Customer Success (SLA Urgent)"
            lead_category = "Customer Churn Risk"
            is_alert = True
        else:
            is_high = detected_tv_count and detected_tv_count > 10
            routing_queue = "High Priority Sales" if is_high else "Standard Sales"
            lead_category = "High Priority" if is_high else "Standard"
            is_alert = bool(is_high)
        
        final_city = detected_city
        final_tv_count = detected_tv_count
    else:
        # calling the ai_agent
        llm_data = ai_agent.run_llama_triage(form_data, detected_tv_count)
        final_tv_count = llm_data.get("tv_count", detected_tv_count)
        final_city = llm_data.get("city", detected_city)
        
        msg_lower = form_data["message"].lower()
        if "partnership" in msg_lower:
            routing_queue = "Strategic Accounts"
            lead_category = "Enterprise Prospect"
            is_alert = False
        elif "offline" in msg_lower:
            routing_queue = "Customer Success (SLA Urgent)"
            lead_category = "Customer Churn Risk"
            is_alert = True
        else:
            is_high = final_tv_count and int(final_tv_count) > 10
            routing_queue = "High Priority Sales" if is_high else "Standard Sales"
            lead_category = "High Priority" if is_high else "Standard"
            is_alert = bool(is_high)

    # 3. build the final structured payload for the CRM
    crm_payload = {
        "contact": {
            "first_name": form_data["first_name"], 
            "last_name": form_data["last_name"], 
            "email": form_data["email"], 
            "phone": form_data["phone"]
        },
        "company": {
            "company_name": form_data["business_name"], 
            "city": final_city, 
            "hardware_count_tv": final_tv_count
        },
        "deal_routing": {
            "pipeline_stage": "Inbound Triage Completed", 
            "lead_score_category": lead_category, 
            "target_operational_queue": routing_queue, 
            "requires_immediate_sla": is_alert
        }
    }
    
    # 4. dispatch the real webhook
    try:
        requests.post(webhook_url, json=crm_payload, timeout=3)
    except:
        pass 
        
    return crm_payload