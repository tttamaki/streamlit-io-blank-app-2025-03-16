import subprocess
import tempfile
import os
import streamlit as st
import urllib.parse

# Streamlitアプリのタイトル
st.title("DFD Generator with Streamlit")

# secretsからBASE_URLを取得（デフォルト値あり）
BASE_URL = st.secrets["BASE_URL"] if "BASE_URL" in st.secrets else "https://this.app.url/"

# URLパラメータからDFDのテキストを取得（指定がない場合は空の文字列）
query_params = st.query_params

dfd_text = query_params.get("text", "")
if dfd_text:
    dfd_text = urllib.parse.unquote(dfd_text)
    st.success("DFD text loaded from URL.")

# 画像出力フォーマットの選択（PDFは毎回作成するため選択肢から除外）
output_format = st.selectbox("Select output format:", ["svg", "png", "jpg"], index=0, key="output_format")

def generate_dfd():
    if st.session_state.dfd_text.strip():
        # 一時ファイルを作成してDFDのテキストを保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as input_file:
            input_file.write(st.session_state.dfd_text.encode("utf-8"))
            input_file_path = input_file.name
        
        # 選択されたフォーマットとPDFの2つを生成
        output_file_path = input_file_path.replace(".txt", f".{st.session_state.output_format}")
        pdf_file_path = input_file_path.replace(".txt", ".pdf")
        
        # `data-flow-diagram` コマンドを実行（選択されたフォーマット）
        command = [
            "data-flow-diagram",
            "-o", output_file_path,
            "-f", st.session_state.output_format,
            "--no-graph-title",
            input_file_path
        ]
        process = subprocess.run(command, capture_output=True, text=True)
        
        # `data-flow-diagram` コマンドを実行（PDFフォーマット）
        command_pdf = [
            "data-flow-diagram",
            "-o", pdf_file_path,
            "-f", "pdf",
            "--no-graph-title",
            input_file_path
        ]
        process_pdf = subprocess.run(command_pdf, capture_output=True, text=True)
        
        if process.returncode == 0 and process_pdf.returncode == 0:
            st.session_state.generated = True
            st.session_state.generated_file = output_file_path
            st.session_state.generated_pdf_file = pdf_file_path
            st.session_state.generated_url = f"{BASE_URL}?text={urllib.parse.quote(st.session_state.dfd_text)}"
            st.session_state.error_message = ""
        else:
            st.session_state.generated = False
            st.session_state.error_message = process.stderr if process.returncode != 0 else process_pdf.stderr


# ユーザー入力欄
dfd_text = st.text_area("Enter DFD text (see [syntax document](https://github.com/pbauermeister/dfd/blob/main/doc/README.md)):", dfd_text, key="dfd_text", on_change=generate_dfd)

# ボタンを押してDFDを生成
st.button("Generate DFD", on_click=generate_dfd)


# エラー表示をテキストエリアの下に移動
if "error_message" in st.session_state and st.session_state.error_message:
    st.error("Error generating DFD:")
    st.text(st.session_state.error_message)

# 生成結果をボタンの下に表示
if st.session_state.get("generated", False):
    st.success("DFD generated successfully!")
    
    # PDFダウンロードボタンを常に表示
    with open(st.session_state.generated_pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="dfd.pdf")

    # 生成画像を表示
    st.image(st.session_state.generated_file)   
    
    # URLをコピーできるボタンを追加
    st.text_input("Copy the generated DFD URL:", st.session_state.generated_url, help="Copy this URL manually")
    st.code(st.session_state.generated_url, language="text")