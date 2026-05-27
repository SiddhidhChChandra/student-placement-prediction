import streamlit as st
import pickle
import numpy as np
import os

# Find the exact path of this folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model.pk')

# 1. Load the trained model using the absolute path
model = pickle.load(open(model_path, 'rb'))

# 2. Set up the web page UI
st.title("🎓 Student Placement Predictor")
st.write("Enter your academic metrics to evaluate corporate placement eligibility.")

# 3. Create input boxes for the user
cgpa = st.number_input("Enter your CGPA", min_value=0.0, max_value=10.0, step=0.1)

# Added 'help' parameter here to guide laymen users
iq = st.number_input(
    "Enter your IQ Level", 
    min_value=0, 
    max_value=200, 
    step=1,
    help="Average human IQ is 100. Most people (about 68%) score between 85 and 115."
)

# 4. Predict button with corporate-grade evaluation logic
if st.button("Predict Placement Status"):
    
    # CASE 1: STRICT REGULATORY CRITERIA (RED)
    if cgpa < 5.0:
        st.error("❌ EVALUATION CRITERIA: NOT PLACED. Profile fails to meet the minimum regulatory CGPA threshold (5.0) required to unlock corporate eligibility filters.")
        
    elif iq < 70:
        st.error("❌ EVALUATION CRITERIA: NOT PLACED. Cognitive assessment performance sits below the baseline organizational requirement for technical roles.")
        
    # CASE 2: STATISTICAL ANOMALY / DISCREPANCY DETECTED (BLUE)
    elif cgpa >= 8.5 and iq < 90:
        st.info("ℹ️ EVALUATION STATUS: AUDIT REQUIRED. Profile data demonstrates statistical inconsistency (High CGPA relative to lower cognitive assessment score). Credential verification recommended.")
        
    # CASE 3: BORDERLINE/MARGINAL COHORT (YELLOW)
    elif (cgpa < 6.5 and iq < 100) or (cgpa < 7.5 and iq < 85):
        st.warning("⚠️ EVALUATION STATUS: CONDITIONAL / MAYBE. Profile features fall within the marginal corporate hiring variance. Placement probability is highly dependent on specific interview performance.")
        
    # CASE 4: STANDARD EVALUATION DRIVEN BY MACHINE LEARNING MODEL
    else:
        input_data = np.array([[cgpa, iq]])
        prediction = model.predict(input_data)
        
        # Display the result based on the model weights
        if prediction == 1:
            st.success("👑 EVALUATION STATUS: CONFIRMED PLACEMENT. Predictive modeling indicates high alignment with historical selection datasets for target corporate cohorts.")
        else:
            st.error("❌ EVALUATION STATUS: RISK IDENTIFIED. Statistical projection indicates a lower probability of placement matching current historical training data trends.")
