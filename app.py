import streamlit as st
import numpy as np
import joblib

# 1. Load the improved model
# Ensure 'improved_fraud_model.pkl' is in the same folder
try:
    model = joblib.load('improved_fraud_model.pkl')
except:
    st.error("Model file not found! Please run your training script first to generate 'improved_fraud_model.pkl'.")

# Page Configuration
st.set_page_config(page_title="FraudGuard Pro AI", page_icon="🛡️", layout="wide")

st.title("🛡️ FraudGuard Pro: Forensic Transaction Analysis")
st.markdown("""
**Hybrid Security System:** This application combines **Random Forest Machine Learning** with 
**Deterministic Business Rules** to catch logical inconsistencies and behavioral fraud patterns.
""")

# --- 2. USER INPUT SECTION ---
st.subheader("Transaction Metadata")
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        type_option = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT"])
        amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=100.0, format="%.2f")
    
    with col2:
        old_balance_org = st.number_input("Sender: Starting Balance", min_value=0.0, format="%.2f")
        new_balance_org = st.number_input("Sender: Ending Balance", min_value=0.0, format="%.2f")
        
    with col3:
        old_balance_dest = st.number_input("Receiver: Starting Balance", min_value=0.0, format="%.2f")
        new_balance_dest = st.number_input("Receiver: Ending Balance", min_value=0.0, format="%.2f")

# --- 3. THE "PERFECT CATCH" LOGIC ---
if st.button("Run Forensic Analysis"):
    # A. Feature Engineering (Calculating the math discrepancies)
    type_val = 0 if type_option == 'TRANSFER' else 1
    error_orig = new_balance_org + amount - old_balance_org
    error_dest = old_balance_dest + amount - new_balance_dest
    
    # B. Hard Rule Checks (The "Interviewer Trap")
    # These rules override the AI if a physical impossibility occurs
    is_impossible = False
    reasons = []

    # Rule A: Spending money that doesn't exist
    if amount > old_balance_org:
        is_impossible = True
        reasons.append("Insufficient Funds: The transaction amount exceeds the available source balance.")
    
    # Rule B: Ghost Money / Destination Mismatch (The fix for Case 3)
    # Checks if the receiver balance increased by exactly the amount sent
    if abs(error_dest) > (amount * 0.01) and amount > 0:
        is_impossible = True
        reasons.append(f"Destination Integrity Failure: A discrepancy of ${abs(error_dest):.2f} was detected at the receiver's end.")

    # C. Machine Learning Prediction
    # Features must be in the exact order: [type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, errorBalanceOrig, errorBalanceDest]
    features = np.array([[type_val, amount, old_balance_org, new_balance_org, 
                          old_balance_dest, new_balance_dest, error_orig, error_dest]])
    
    ml_prediction = model.predict(features)[0]
    ml_risk_score = model.predict_proba(features)[0][1] * 100 # Probability of class 1 (Fraud)

    # --- 4. DISPLAY RESULTS ---
    st.divider()
    
    # Threshold: Flag as fraud if Hard Rules are triggered OR ML risk is high (>50%)
    if is_impossible or ml_prediction == 1 or ml_risk_score > 50:
        st.error(f"🚨 HIGH RISK DETECTED: {max(ml_risk_score, 95.0 if is_impossible else 0):.1f}% Risk Score")
        
        st.subheader("Forensic Breakdown")
        if is_impossible:
            for reason in reasons:
                st.write(f"❌ **Integrity Rule Violated:** {reason}")
        
        if ml_prediction == 1:
            st.write("🔍 **ML Pattern Match:** Transaction matches behavioral signatures of known financial theft.")
            
        with st.expander("View Technical Details"):
            st.write(f"**Origin Math Error:** ${error_orig:.2f}")
            st.write(f"**Destination Math Error:** ${error_dest:.2f}")
            st.write(f"**Raw ML Probability:** {ml_risk_score:.2f}%")
    else:
        st.success(f"✅ TRANSACTION VERIFIED: Risk Score {ml_risk_score:.1f}%")
        st.write("**Analysis:** This transaction passes all integrity checks and follows verified historical behavior.")