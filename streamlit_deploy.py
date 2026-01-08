import streamlit as st
import requests

st.set_page_config(page_title="Bank Churn Prediction", page_icon="🏦", layout="centered")

# Cloud deployment banner
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; color: white; text-align: center;'>
    <h1>🏦 Bank Churn Prediction</h1>
    <h3>MLOps Project - Fully Deployed on Cloud</h3>
    <p><strong>API:</strong> Azure Container Apps</p>
    <p><strong>Frontend:</strong> Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# Your Azure URL (hardcoded for deployment)
AZURE_API_URL = "https://bank-churn.blackground-50ed117d.francecentral.azurecontainerapps.io"

st.markdown(f"""
### 🌐 Cloud Deployment Status
**API Endpoint:** `{AZURE_API_URL}`  
**Status:** ✅ Production Ready  
**Region:** France Central (Azure)
""")

# Test connection automatically
with st.spinner("Checking cloud API connection..."):
    try:
        response = requests.get(f"{AZURE_API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('model_loaded'):
                st.success("✅ **Azure API Connected & Model Loaded**")
            else:
                st.warning("⚠️ API Connected but Model Not Loaded")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ Cannot connect to Azure API")

st.divider()

# Customer Input
st.subheader("👤 Enter Customer Details")

col1, col2 = st.columns(2)

with col1:
    credit_score = st.slider("Credit Score", 300, 850, 650)
    age = st.slider("Age", 18, 100, 42)
    tenure = st.slider("Tenure (years)", 0, 10, 5)
    balance = st.number_input("Balance ($)", 0.0, 1000000.0, 50000.0, step=1000.0)

with col2:
    num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
    estimated_salary = st.number_input("Estimated Salary ($)", 0.0, 1000000.0, 75000.0, step=1000.0)
    has_credit_card = st.radio("Has Credit Card", ["No", "Yes"])
    is_active = st.radio("Is Active Member", ["No", "Yes"])
    geography = st.selectbox("Country", ["France", "Germany", "Spain"])

# Convert values
has_credit_card = 1 if has_credit_card == "Yes" else 0
is_active = 1 if is_active == "Yes" else 0
geography_germany = 1 if geography == "Germany" else 0
geography_spain = 1 if geography == "Spain" else 0

# Predict Button
if st.button("🔮 Predict Churn (Azure Cloud)", type="primary", use_container_width=True):
    # Prepare data
    customer_data = {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": float(balance),
        "NumOfProducts": num_products,
        "HasCrCard": has_credit_card,
        "IsActiveMember": is_active,
        "EstimatedSalary": float(estimated_salary),
        "Geography_Germany": geography_germany,
        "Geography_Spain": geography_spain
    }
    
    st.info(f"🌐 **Sending request to Azure API...**")
    
    try:
        with st.spinner("Calling Azure Cloud API..."):
            response = requests.post(f"{AZURE_API_URL}/predict", 
                                   json=customer_data, 
                                   timeout=15)
            
        if response.status_code == 200:
            result = response.json()
            
            st.success("✅ **Prediction Received from Azure Cloud**")
            st.divider()
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                probability = result['churn_probability'] * 100
                st.metric("Churn Probability", f"{probability:.1f}%")
            
            with col2:
                prediction_text = "🚨 Will CHURN" if result['prediction'] == 1 else "✅ Will STAY"
                st.metric("Prediction", prediction_text)
            
            with col3:
                risk_level = result['risk_level']
                if risk_level == "High":
                    st.error(f"🔴 {risk_level} Risk")
                elif risk_level == "Medium":
                    st.warning(f"🟡 {risk_level} Risk")
                else:
                    st.success(f"🟢 {risk_level} Risk")
            
            # Recommendation
            st.divider()
            st.subheader("🎯 Recommended Action")
            if risk_level == "High":
                st.error("**Immediate Action:** Contact customer with retention offer")
            elif risk_level == "Medium":
                st.warning("**Monitor:** Send satisfaction survey")
            else:
                st.success("**Maintain:** Continue relationship management")
                
        else:
            st.error(f"❌ API Error {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ Error connecting to Azure: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>MLOps Pipeline: Bank Churn Prediction</strong></p>
    <p>🌐 **Backend:** Azure Container Apps | 🎨 **Frontend:** Streamlit Cloud</p>
    <p>🔗 **API:** https://bank-churn.blackground-50ed117d.francecentral.azurecontainerapps.io</p>
    <p>📊 **Model:** Random Forest Classifier | 🚀 **Status:** Production</p>
</div>
""", unsafe_allow_html=True)