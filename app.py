import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.title("🤖 **PHASE 1: AI CRM - Excel Upload + Dynamic Fields**")
st.write("**Upload ANY Excel → Auto-detect columns → Ready for AI queries!**")

# File Upload
uploaded_file = st.file_uploader("📁 Upload Excel/CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Load Data
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        # PHASE 1: DYNAMIC ADAPTATION
        st.success(f"✅ **LOADED {len(df)} ROWS!**")
        st.write(f"**📊 COLUMNS DETECTED:** `{', '.join(df.columns.tolist())}`")
        
        # Show Sample Data
        st.subheader("**📋 SAMPLE DATA**")
        st.dataframe(df.head(5))
        
        # Show Column Info
        st.subheader("**🔧 AI READY FIELDS**")
        for col in df.columns:
            st.write(f"• **{col}** - {df[col].dtype} - Sample: `{df[col].iloc[0]}`")
        
        # Save for Next Phases
        if st.button("💾 **SAVE DATA**"):
            df.to_csv("crm_data.csv", index=False)
            st.success("✅ **Data saved as `crm_data.csv`**")
            
    except Exception as e:
        st.error(f"❌ **Error:** {e}")
else:
    st.info("👆 **Upload your Excel/CSV to start!**")
    st.write("**Works with ANY columns:** Name, Email, Sales, Status, etc.")