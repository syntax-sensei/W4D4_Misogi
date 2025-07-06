import streamlit as st
import os
from extractor import extract_text
from chunker import chunk_text
from embedder import embed_and_store
from rag_pipeline import generate_response

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Admin credentials - load from environment variables
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  # Default fallback for development

st.set_page_config(page_title="HR Onboarding Assistant", layout="wide")

mode = st.sidebar.radio("Mode", ["Employee Chat", "Admin Upload"])

# Initialize session state for admin authentication
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

st.title("🤖 HR Knowledge Assistant")

if mode == "Admin Upload":
    st.subheader("🔐 Admin Authentication Required")
    
    # Admin authentication
    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("✅ Admin access granted!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
        
        st.info("💡 Contact your system administrator for the password.")
        st.stop()
    
    # Admin interface (only shown after authentication)
    if st.session_state.admin_authenticated:
        # Logout button
        if st.sidebar.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
        
        st.success("🔓 Admin access active")
        st.subheader("📁 Upload HR Policy Documents")
        
        # Show existing files in uploads folder
        existing_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(('.txt', '.pdf', '.docx'))]
        if existing_files:
            st.write("**Existing files in uploads folder:**")
            for file in existing_files:
                st.write(f"• {file}")
            
            if st.button("Process Existing Files"):
                with st.spinner("Processing existing files..."):
                    for file in existing_files:
                        path = os.path.join(UPLOAD_DIR, file)
                        text = extract_text(path)
                        chunks = chunk_text(text)
                        embed_and_store(chunks, file)
                        st.success(f"{file} embedded with {len(chunks)} chunks.")
        
        st.write("---")
        st.write("**Upload new files:**")
        files = st.file_uploader("Upload HR Docs", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        if st.button("Process & Embed New Files"):
            for file in files:
                path = os.path.join(UPLOAD_DIR, file.name)
                with open(path, "wb") as f:
                    f.write(file.read())
                text = extract_text(path)
                chunks = chunk_text(text)
                embed_and_store(chunks, file.name)
                st.success(f"{file.name} embedded with {len(chunks)} chunks.")
else:
    st.subheader("💬 Ask a question about HR policies")
    user_input = st.text_input("Your Question:")
    if st.button("Get Answer") and user_input:
        with st.spinner("Thinking..."):
            answer, refs = generate_response(user_input)
        st.markdown("**Answer:**")
        st.success(answer)
        st.markdown(f"**References:** {refs}")
