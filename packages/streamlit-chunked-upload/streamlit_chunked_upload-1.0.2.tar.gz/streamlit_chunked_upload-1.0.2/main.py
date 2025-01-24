import streamlit as st
from streamlit_chunked_upload import uploader

st.set_page_config(
    page_title="Streamlit Chunked Upload Demo",
    page_icon="📁",
    layout="wide"
)

st.title("Streamlit Chunked Upload Demo")

# Add description
st.markdown("""
This demo shows how to use the streamlit-chunked-upload component to handle large file uploads.
The component splits large files into chunks before uploading, making it more reliable for large files.
""")

col1, col2 = st.columns(2)

with col1:
    st.header("Chunked Uploader")
    st.caption("Handles large files by splitting them into chunks")
    
    # Chunked file uploader
    chunked_file = uploader(
        "Upload Large File",
        key="chunked_uploader",
        uploader_msg="Drag and drop or click to upload large files",
        chunk_size=31,  # 31MB chunks
    )
    
    if chunked_file is not None:
        st.success(f"File uploaded successfully: {chunked_file.name}")
        st.info(f"File size: {chunked_file.size / (1024*1024):.2f} MB")
        st.download_button(
            "Download uploaded file",
            data=chunked_file,
            file_name=chunked_file.name,
            type="primary",
            key="chunked_download"
        )

with col2:
    st.header("Standard Uploader")
    st.caption("Regular Streamlit file uploader for comparison")
    
    # Standard file uploader
    standard_file = st.file_uploader(
        "Upload File (Standard)",
        key="standard_uploader"
    )
    
    if standard_file is not None:
        st.success(f"File uploaded successfully: {standard_file.name}")
        st.info(f"File size: {standard_file.size / (1024*1024):.2f} MB")
        st.download_button(
            "Download uploaded file",
            data=standard_file,
            file_name=standard_file.name,
            type="primary",
            key="standard_download"
        )

# Add rerun counter to demonstrate state management
if "count" not in st.session_state:
    st.session_state.count = 0

st.sidebar.metric("Rerun Count", st.session_state.count)
st.session_state.count += 1 