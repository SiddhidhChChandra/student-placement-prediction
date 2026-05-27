import streamlit as st
import pickle
import numpy as np

# 1. Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# 2. Set up the web page UI
st.title("🎓 Student Placement Predictor")
st.write("Enter your academic metrics to predict placement probability.")

# 3. Create input boxes for the user
cgpa = st.number_input("Enter your CGPA", min_value=0.0, max_value=10.0, step=0.1)
iq = st.number_input("Enter your IQ Level", min_value=0, max_value=200, step=1)

# 4. Predict button
if st.button("Predict Placement Status"):
    # Reshape input to match model format
    input_data = np.array([[cgpa, iq]])
    prediction = model.predict(input_data)
    
    # Display the result
    if prediction[0] == 1:
        st.success("🎉 High probability of being PLACED!")
    else:
        st.error("⚠️ Higher risk of being NOT PLACED. Keep working hard!")
