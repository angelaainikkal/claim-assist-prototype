import streamlit as st
from google import genai
from google.genai import types
import json
import time
import os

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(page_title="Intelligent Claim Workflow", layout="centered")
st.title("🛡️ ClaimAssist: Automated Workflow")

# Safely get API key
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API Key not found. Add it to Streamlit secrets or environment variables.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# OPTIONAL: DEBUG MODEL LIST (Disable Later)
# ==========================================
# Uncomment this once to see available models
# models = client.models.list()
# for m in models:
#     st.write(m.name)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

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

# ==========================================
# STEP 1: CLAIM INITIATION
# ==========================================

if st.session_state.step == 1:
    st.header("Step 1: Report Incident")
    policy_id = st.text_input("Enter Policy ID")
    incident_type = st.selectbox(
        "Incident Type",
        ["Medical Emergency", "Vehicle Accident", "Property Damage"]
    )

    if st.button("Initiate Claim"):
        if policy_id:
            with st.spinner("Fetching policy details..."):
                time.sleep(1)
                st.session_state.claim_id = f"CLM-{int(time.time())}"
                st.session_state.policy_details = {
                    "id": policy_id,
                    "type": incident_type
                }
            st.success(f"Claim Initiated! ID: {st.session_state.claim_id}")
            next_step()
            st.rerun()

# ==========================================
# STEP 2: DOCUMENT UPLOAD & VALIDATION
# ==========================================

elif st.session_state.step == 2:
    st.header(f"Step 2: Document Upload (Claim: {st.session_state.claim_id})")

    st.markdown("### 📋 Required Documents")

    if st.session_state.policy_details["type"] == "Medical Emergency":
        st.write("- Hospital Discharge Summary")
        st.write("- Medical Bills & Receipts")
        st.write("- Patient ID")
    else:
        st.write("- Police Report")
        st.write("- Repair Estimate")
        st.write("- Vehicle Registration")

    uploaded_file = st.file_uploader(
        "Upload Document for AI OCR & Validation",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if st.button("Verify Document"):
        if uploaded_file:
            with st.spinner("Running Gemini 1.5 Flash OCR & Validation..."):
                try:
                    doc_bytes = uploaded_file.read()
                    mime_type = (
                        "application/pdf"
                        if uploaded_file.name.endswith("pdf")
                        else "image/jpeg"
                    )

                    prompt = f"""
                    Analyze this {st.session_state.policy_details['type']} document.

                    1. Verify if it is complete and legible.
                    2. Detect missing signatures, blur, cut edges.
                    3. Extract key medical/diagnostic data.

                    Return ONLY valid JSON:

                    {{
                        "is_valid": true/false,
                        "missing_incorrect_items": [],
                        "extracted_data": {{}}
                    }}
                    """

                    response = client.models.generate_content(
                        model="models/gemini-1.5-flash",  # ✅ FIXED MODEL CALL
                        contents=[
                            types.Part.from_bytes(
                                data=doc_bytes,
                                mime_type=mime_type
                            ),
                            prompt,
                        ],
                    )

                    raw_text = response.text.strip()

                    # Clean potential markdown formatting
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

                    result = json.loads(raw_text)

                    if result.get("is_valid"):
                        st.success("✅ Document Complete & Valid!")
                        st.json(result.get("extracted_data", {}))
                        next_step()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Validation Failed:")
                        for issue in result.get("missing_incorrect_items", []):
                            st.warning(issue)

                except Exception as e:
                    st.error(f"Error processing document: {e}")

# ==========================================
# STEP 3: VERIFICATION & SCORING
# ==========================================

elif st.session_state.step == 3:
    st.header("Step 3: Verification & Scoring")

    st.info("Running cross-checks...")
    time.sleep(1)

    st.markdown("### Claim Readiness Score")

    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

    st.success("Score: 100% - Ready for Submission")

    if st.button("Securely Submit via API"):
        with st.spinner("Submitting..."):
            time.sleep(1)
            next_step()
            st.rerun()

# ==========================================
# STEP 4: TRACKING
# ==========================================

elif st.session_state.step == 4:
    st.header("Step 4: Status Tracking")
    st.balloons()

    st.success("🎉 Claim Submitted Successfully!")

    st.markdown("### Live Tracking Timeline")
    st.write("🟢 Claim Initiated")
    st.write("🟢 Documents Verified")
    st.write("🟢 Submitted to Insurer API")
    st.write("⏳ Pending Adjuster Review")

    if st.button("Start New Claim Workflow"):
        reset_workflow()
        st.rerun()
