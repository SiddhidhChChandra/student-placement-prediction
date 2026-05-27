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
st.write("Enter your academic metrics to predict placement probability.")

# 3. Create input boxes for the user
cgpa = st.number_input("Enter your CGPA", min_value=0.0, max_value=10.0, step=0.1)
iq = st.number_input("Enter your IQ Level", min_value=0, max_value=200, step=1)

# 4. Predict button with logical boundary overrides
if st.button("Predict Placement Status"):
    
    # Rule 1: Strict Academic Criteria (CGPA below 5.0 is an automatic fallback)
    if cgpa < 5.0:
        st.error("❌ Placement Status: NOT PLACED. A minimum CGPA of 5.0 is generally required to clear company eligibility criteria.")
        
    # Rule 2: Extreme Below-Average IQ Criteria 
    elif iq < 75:
        st.error("⚠️ Placement Status: NOT PLACED. Your technical problem-solving metrics drop below the standard corporate assessment threshold.")
        
    # Rule 3: Low Profile Combination (Marginal CGPA + Below Average IQ)
    elif cgpa < 6.5 and iq < 95:
        st.warning("⚠️ Placement Status: HIGH RISK / NOT PLACED. The combination of a marginal CGPA and a below-average assessment score reduces probability.")
        
    # Rule 4: If inputs pass safety checks, fallback to the model predictions
    else:
        input_data = np.array([[cgpa, iq]])
        prediction = model.predict(input_data)
        
        # Display the result based on the model's math
        if prediction == 1:
            st.success("🎉 High probability of being PLACED!")
        else:
            st.error("⚠️ Higher risk of being NOT PLACED. Keep working hard!")
