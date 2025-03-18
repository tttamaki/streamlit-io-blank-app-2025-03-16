import subprocess
import tempfile
import os
import streamlit as st
import urllib.parse

def run_data_flow_diagram(input_file_path, output_format):
    """data-flow-diagramを実行し、指定されたフォーマットのファイルを生成する"""
    output_file_path = input_file_path.replace(".txt", f".{output_format}")
    command = [
        "data-flow-diagram",
        "-o", output_file_path,
        "-f", output_format,
        "--no-graph-title",
        input_file_path
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    return process, output_file_path

def generate_dfd():
    dfd_text = st.session_state.get("dfd_text", "").strip()
    if dfd_text:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as input_file:
            input_file.write(dfd_text.encode("utf-8"))
            input_file_path = input_file.name
        
        # 選択されたフォーマットの生成
        process, output_file_path = run_data_flow_diagram(input_file_path, st.session_state.output_format)
        
        # PDFの生成
        process_pdf, pdf_file_path = run_data_flow_diagram(input_file_path, "pdf")
        
        if process.returncode == 0 and process_pdf.returncode == 0:
            st.session_state.generated = True
            st.session_state.generated_file = output_file_path
            st.session_state.generated_pdf_file = pdf_file_path
            st.session_state.generated_url = f"{st.session_state.BASE_URL}?text={urllib.parse.quote(dfd_text)}"
            st.session_state.error_message = ""
        else:
            st.session_state.generated = False
            st.session_state.error_message = process.stderr if process.returncode != 0 else process_pdf.stderr

def initialize_dfd_text():
    """URLパラメータからDFDテキストを初期化する"""
    query_params = st.query_params
    if "dfd_text" not in st.session_state:
        dfd_text = query_params.get("text", "")
        if dfd_text:
            dfd_text = urllib.parse.unquote(dfd_text)
            st.session_state.dfd_text = dfd_text
            st.success("DFD text loaded from URL.")
        else:
            st.session_state.dfd_text = ""

def main():
    st.title("DFD Generator with Streamlit")
    
    st.session_state.BASE_URL = st.secrets["BASE_URL"] if "BASE_URL" in st.secrets else "https://this.app.url/"
    
    initialize_dfd_text()
    
    st.selectbox("Select output format:", ["svg", "png", "jpg"], index=0, key="output_format")
    
    st.text_area("Enter DFD text (see [syntax document](https://github.com/pbauermeister/dfd/blob/main/doc/README.md)):", st.session_state.dfd_text, key="dfd_text", on_change=generate_dfd)
    
    if "generated" not in st.session_state and st.query_params.get("text", ""):
        generate_dfd()
    
    st.button("Generate DFD", on_click=generate_dfd)
    
    if "error_message" in st.session_state and st.session_state.error_message:
        st.error("Error generating DFD:")
        st.text(st.session_state.error_message)
    
    if st.session_state.get("generated", False):
        st.success("DFD generated successfully!")
        st.image(st.session_state.generated_file)
        
        with open(st.session_state.generated_pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name="dfd.pdf")
        
        st.text_input("Copy the generated DFD URL:", st.session_state.generated_url, help="Copy this URL manually")
        st.code(st.session_state.generated_url, language="text")

if __name__ == "__main__":
    main()