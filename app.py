import streamlit as st
import os
from groq import Groq
from pypdf import PdfReader

# 1. UI Setup
st.set_page_config(page_title="Super Fast AI PDF Assistant", layout="wide")
st.title("🚀 Super-Fast AI PDF Assistant (made by SAGAR)")

# 🔒 Secrets se Groq Key lena
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ API Key nahi mili! Kripya Streamlit Secrets me GROQ_API_KEY set karein.")
    st.stop()

# File uploader
uploaded_files = st.file_uploader("Apni PDF files upload karein", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    full_context = ""
    
    with st.spinner("PDFs ko instant read kiya ja raha hai..."):
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            for page_num, page in enumerate(reader.pages):
                full_context += f"\n--- [Document: {uploaded_file.name} | Page Number: {page_num + 1}] ---\n"
                full_context += page.extract_text()

    st.success("🎉 Sabhi PDFs padh li gayi hain! Ab aap niche sawal pooch sakte hain.")

    # 1. Detailed Summary Section
    if st.button("📝 PDF ka detailed Summary points me chahiye?"):
        with st.spinner("Groq AI summary bana raha hai..."):
            # Update: 2026 ka sabse stable aur current free model
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": f"Niche diye gaye PDF data ka ek clear aur detailed summary points me Hindi me likhein:\n\n{full_context[:30000]}"}
                ],
            )
            st.write("### 📋 PDF Summary:")
            st.write(response.choices.message.content)

    # 2. Chat Section with Page Citation
    st.write("---")
    st.subheader("💬 AI se Sawal Poochein (With Page Numbers)")
    user_query = st.text_input("PDF ke baare me koi bhi sawal likhein:")
    
    if user_query:
        with st.spinner("AI jawab dhoond raha hai..."):
            system_instruction = (
                "Aap ek professional AI assistant hain. Diye gaye context (PDF text) ko achhe se padhein. "
                "User ke sawal ka bilkul sateek aur clear jawab Hindi me dein. Apne jawab me strictly "
                "batayein ki yeh jankari kis Page Number aur kis Document se li gayi hai. "
                "Agar jawab data me nahi hai, to keh dein ki 'Mujhe iska jawab document me nahi mila'."
            )
            
            # Update: 2026 ka sabse stable aur current free model
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Context:\n{full_context[:35000]}\n\nSawal: {user_query}"}
                ],
                temperature=0.3
            )
            st.write("### 🤖 AI ka Jawab:")
            st.write(response.choices.message.content)
