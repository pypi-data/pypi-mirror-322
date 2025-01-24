import streamlit as st
from streamlit_chunked_upload import uploader

def main():
    st.title("Streamlit Chunked Upload Example")
    
    # Basic usage
    st.subheader("Basic Usage")
    file1 = uploader(
        "Basic uploader",
        key="basic_uploader",
    )
    if file1:
        st.write(f"Uploaded: {file1.name} ({file1.size / (1024*1024):.2f} MB)")
    
    # Advanced usage with custom chunk size
    st.subheader("Advanced Usage", divider=True)
    file2 = uploader(
        "Advanced uploader with custom chunk size",
        key="advanced_uploader",
        chunk_size=31,  # 31MB chunks
        uploader_msg="Drop your large files here",
    )
    if file2:
        st.write(f"Uploaded: {file2.name} ({file2.size / (1024*1024):.2f} MB)")
        st.download_button(
            "Download file",
            data=file2,
            file_name=file2.name,
            type="primary",
            key="advanced_download"
        )
    
    # Comparison with standard uploader
    st.subheader("Standard Uploader", divider=True)
    file3 = st.file_uploader("Standard Streamlit uploader")
    if file3:
        st.write(f"Uploaded: {file3.name} ({file3.size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
