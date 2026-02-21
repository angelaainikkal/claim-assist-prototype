import streamlit as st
from google import genai
from google.genai import types
import json
import time

# 1. Initialize Session State for the Workflow
if "step" not in st.session_state:
    st.session_state.step = 1
if "claim_id" not in st.session_state:
    st.session_state.claim_id = None
if "policy_details" not in st.session_state:
    st.session_state.policy_details = {}

def next_step():
    st.session_state.step += 1

def reset_workflow():
    st.session_state.step = 1
    st.session_state.claim_id = None

st.set_page_config(page_title="Intelligent Claim Workflow", layout="centered")
st.title("🛡️ ClaimAssist: Automated Workflow")

# ==========================================
# FLOW: Start & Claim Initiation
# ==========================================
if st.session_state.step == 1:
    st.header("Step 1: Report Incident")
    policy_id = st.text_input("Enter Policy ID")
    incident_type = st.selectbox("Incident Type", ["Medical Emergency", "Vehicle Accident", "Property Damage"])
    
    if st.button("Initiate Claim"):
        if policy_id:
            with st.spinner("Auto-fetching policy details and notifying TPA..."):
                time.sleep(1) # Simulating API/DB call
                # Generate Claim ID
                st.session_state.claim_id = f"CLM-{int(time.time())}"
                st.session_state.policy_details = {"id": policy_id, "type": incident_type}
            st.success(f"Claim Initiated! ID: {st.session_state.claim_id}")
            next_step()
            st.rerun()

# ==========================================
# FLOW: Checklist, Upload & Validation Loop
# ==========================================
elif st.session_state.step == 2:
    st.header(f"Step 2: Document Upload (Claim: {st.session_state.claim_id})")
    
    # Generate Dynamic Checklist
    st.markdown("### 📋 Required Documents")
    if st.session_state.policy_details["type"] == "Medical Emergency":
         st.write("- [ ] Hospital Discharge Summary\n- [ ] Medical Bills & Receipts\n- [ ] Patient ID")
    else:
         st.write("- [ ] Police Report\n- [ ] Repair Estimate\n- [ ] Vehicle Registration")
         
    # Guided Document Upload + OCR
    uploaded_file = st.file_uploader("Upload Document for Guided OCR", type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button("Verify Document"):
        if uploaded_file:
            with st.spinner("Running Gemini 1.5 Flash OCR & Validation..."):
                try:
                    client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY"))
                    doc_bytes = uploaded_file.read()
                    mime_type = "application/pdf" if uploaded_file.name.endswith('pdf') else "image/jpeg"
                    
                    # Prompt designed for the "Decision Diamond" in your flowchart
                    prompt = f"""
                    Analyze this {st.session_state.policy_details['type']} document.
                    1. Verify if it is a complete, legible document.
                    2. Check for missing signatures, blurry text, or cut-off edges.
                    3. Extract key diagnostic data, carefully mapping ailments to standard ICD-11 codes where applicable.
                    
                    Return EXACTLY this JSON format:
                    {{
                        "is_valid": true/false,
                        "missing_incorrect_items": ["list specific issues here, leave empty if valid"],
                        "extracted_data": {{"key": "value"}}
                    }}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=[types.Part.from_bytes(data=doc_bytes, mime_type=mime_type), prompt]
                    )
                    
                    result = json.loads(response.text.replace('```json', '').replace('```', '').strip())
                    
                    # Decision: Documents Complete & Valid?
                    if result.get("is_valid"):
                        st.success("✅ Document Complete & Valid!")
                        st.json(result.get("extracted_data", {}))
                        next_step()
                        time.sleep(2)
                        st.rerun()
                    else:
                        # Path: Detect Missing / Incorrect Items (Loops back to upload)
                        st.error("❌ Validation Failed. Please correct the following issues and re-upload:")
                        for issue in result.get("missing_incorrect_items", []):
                            st.warning(f"⚠️ {issue}")
                            
                except Exception as e:
                    st.error(f"Error processing document: {e}")

# ==========================================
# FLOW: Verification, Scoring & Submission
# ==========================================
elif st.session_state.step == 3:
    st.header("Step 3: Verification & Scoring")
    
    # Cross-Document Verification
    st.info("Running cross-checks against policy constraints...")
    time.sleep(1)
    
    # Claim Readiness Score
    st.markdown("### Claim Readiness Score")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
        
    st.success("Score: 100% - Ready for Submission")
    
    # Secure Submission via API
    if st.button("Securely Submit via API"):
        with st.spinner("Submitting to TPA Gateway..."):
            time.sleep(1) # Simulating API post
            next_step()
            st.rerun()

# ==========================================
# FLOW: Real-Time Tracking & End
# ==========================================
elif st.session_state.step == 4:
    st.header("Step 4: Status Tracking")
    st.balloons()
    st.success("🎉 Claim Submitted Successfully!")
    
    # Real-Time Status Tracking & Alerts
    st.markdown("### Live Tracking Timeline")
    st.write("🟢 **Claim Initiated**")
    st.write("🟢 **Documents Verified & Scored**")
    st.write("🟢 **Submitted to Insurer API**")
    st.write("⏳ *Pending Adjuster Review*")
    
    if st.button("Start New Claim Workflow"):
        reset_workflow()
        st.rerun()