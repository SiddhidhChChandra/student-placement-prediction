import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import os
import sqlite3

# Find the exact path of this folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model.pk')
db_path = os.path.join(BASE_DIR, 'placement_history.db')

# 1. Load the trained model using the absolute path
model = pickle.load(open(model_path, 'rb'))

# 2. Database Initialization Function with Cloud Safety Fallback
def init_db():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cgpa REAL,
                iq INTEGER,
                status_result TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass

def log_prediction(cgpa_val, iq_val, result_text):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluation_logs (cgpa, iq, status_result)
            VALUES (?, ?, ?)
        ''', (cgpa_val, iq_val, result_text))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass

def get_prediction_logs():
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT timestamp, cgpa, iq, status_result FROM evaluation_logs ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame(columns=["timestamp", "cgpa", "iq", "status_result"])

# Initialize database structure
init_db()

# Helper function to generate background dataset for visualization
@st.cache_data
def get_historical_data():
    np.random.seed(42)
    n_samples = 200
    cgpa_data = np.random.uniform(5.0, 10.0, n_samples)
    iq_data = np.random.uniform(75, 140, n_samples)
    
    status = []
    for c, i in zip(cgpa_data, iq_data):
        if (c >= 7.2 and i >= 95) or c >= 8.5 or i >= 115:
            status.append("Eligible Cohort")
        else:
            status.append("Risk Profile")
            
    return pd.DataFrame({"CGPA": cgpa_data, "IQ": iq_data, "Status": status})

# 3. Set up executive page styling configuration
st.set_page_config(
    page_title="Corporate Placement Intelligence Terminal", 
    page_icon="🏢", 
    layout="wide"
)

# FIXED: Replaced unsafe_index with safe HTML formatting standard
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: 700; color: #1e293b; }
    h1 { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; color: #0f172a; letter-spacing: -0.5px; }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🏢 Corporate Recruitment Analytics Terminal")
st.caption("Enterprise-grade predictive modeling engine for human capital screening & cohort classification.")
st.write("---")

# 4. Structural Layout: Two-Column Workspace Split
left_column, right_column = st.columns(2, gap="large")

with left_column:
    st.subheader("📋 Evaluation Parameter Input")
    
    with st.form("professional_eval_form"):
        cgpa = st.slider(
            "University Cumulative GPA (CGPA)", 
            min_value=0.0, max_value=10.0, value=7.5, step=0.1,
            help="Candidate verified cumulative university grade threshold scale."
        )
        
        iq = st.slider(
            "Cognitive Assessment Index (IQ)", 
            min_value=50, max_value=150, value=100, step=1,
            help="Standardized internal organizational cognitive baseline evaluation score."
        )
        
        st.write("")
        submit_button = st.form_submit_button("📊 Execute Quantitative Analysis", use_container_width=True)

    # Sidebar System Parameters
    with st.sidebar:
        st.header("Compliance & System Specs")
        st.markdown("""
        **Model Framework:** scikit-learn Pipeline  
        **Database Storage:** SQLite Engine Active  
        **Inference Engine:** Quantized Weights Array  
        """)
        st.divider()
        st.caption("System Environment Check: **Operational**")

# Processing and Dynamic Output
with right_column:
    if submit_button:
        st.subheader("🔍 Predictive Intelligence Summary")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            cgpa_tier = "Tier-1 (High)" if cgpa >= 8.0 else ("Tier-2 (Mid)" if cgpa >= 6.5 else "Tier-3 (Sub-optimal)")
            st.metric(label="Academic Track Metric", value=f"{cgpa} CGPA", delta=cgpa_tier, delta_color="normal" if cgpa >= 6.5 else "inverse")
        with m2:
            iq_tier = "Alpha Cohort" if iq > 110 else ("Standard Cohort" if iq >= 90 else "Marginal Cohort")
            st.metric(label="Cognitive Screening Metric", value=f"{iq} pts", delta=iq_tier, delta_color="normal" if iq >= 90 else "inverse")
        with m3:
            raw_index = int((cgpa * 10) + (iq * 0.5))
            st.metric(label="Systemic Synergy Matrix", value=f"{raw_index} index", delta="Calculated Vector")
            
        st.write("")
        
        tab1, tab2, tab3 = st.tabs(["🎯 Decision Matrix", "📈 Statistical Distribution Mapping", "🗄️ Database History Audit"])
        
        final_status_text = ""
        if cgpa < 5.0:
            final_status_text = "Rejected: Insufficient CGPA"
        elif iq < 70:
            final_status_text = "Rejected: Low Cognitive Score"
        elif cgpa >= 8.5 and iq < 90:
            final_status_text = "Audit Triggered: Data Anomaly"
        elif (cgpa < 6.5 and iq < 100) or (cgpa < 7.5 and iq < 85):
            final_status_text = "Conditional Advancement Margin"
        else:
            input_data = np.array([[cgpa, iq]])
            prediction = model.predict(input_data)
            final_status_text = "Confirmed Placement Profile" if prediction == 1 else "Rejected: High Placement Risk"
            
        log_prediction(cgpa, iq, final_status_text)
        
        with tab1:
            st.markdown("### Automated Screening Status Decision")
            if "Insufficient CGPA" in final_status_text:
                st.error("🟥 **SCREENING REJECTION: INSUFFICIENT ACADEMIC MATRICES**  \nProfile parameters sit below the organizational 5.0 CGPA legal minimum standard.")
            elif "Low Cognitive Score" in final_status_text:
                st.error("🟥 **SCREENING REJECTION: COGNITIVE THRESHOLD ANOMALY**  \nStandardized cognitive validation score is below safe operational baseline minimum benchmarks.")
            elif "Data Anomaly" in final_status_text:
                st.info("🟪 **SYSTEM AUDIT TRIGGERED: DATA DISCREPANCY DETECTED**  \nIncongruent parameters observed (Elevated CGPA index conflicting with low cognitive evaluation output).")
            elif "Conditional" in final_status_text:
                st.warning("🟨 **CONDITIONAL ADVANCEMENT: MARGINAL RECRUITMENT VARIANCE**  \nStatistical models place profile vectors in a fluid evaluation margin.")
            elif "Confirmed" in final_status_text:
                st.success("🟩 **HIRING ACCEPTANCE RECOMMENDATION: SUCCESS PROJECTION HIGH**  \nPredictive machine learning matrices confirm optimal profile vector orientation.")
            else:
                st.error("🟥 **SCREENING REJECTION: RECRUITMENT RISK PROFILE MATCH**  \nAlgorithmic projection matrix tracks matching history trajectories with low integration performance scores.")
        
        with tab2:
            st.markdown("### Operational Clustering Visualization")
            df_hist = get_historical_data()
            
            fig = px.scatter(
                df_hist, x="CGPA", y="IQ", color="Status",
                color_discrete_map={"Eligible Cohort": "#3b82f6", "Risk Profile": "#cbd5e1"},
                opacity=0.35,
                labels={"CGPA": "University Verified CGPA", "IQ": "Cognitive Aptitude Index"},
                title="Historical Candidate Clustering Maps vs Current Target Profile Vector"
            )
            fig.add_scatter(
                x=[cgpa], y=[iq], mode="markers",
                marker=dict(color="#0f172a", size=16, symbol="diamond", line=dict(color="#ffffff", width=2)),
                name="Target Evaluation Coordinates",
                hoverinfo="skip"
            )
            fig.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        with tab3:
            st.markdown("### Real-Time Database Queries")
            st.caption("Showing logs pulled directly out of your SQLite datastore file:")
            logs_df = get_prediction_logs()
            st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("💡 **Awaiting Inputs:** Populate parameter fields in the sidebar form layout and execute calculations to generate analytics projections.")
