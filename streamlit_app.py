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

# 画像出力フォーマットの選択
output_format = st.selectbox("Select output format:", ["svg", "png", "pdf", "jpg"], index=0, key="output_format")

def generate_dfd():
    if st.session_state.dfd_text.strip():
        # 一時ファイルを作成してDFDのテキストを保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as input_file:
            input_file.write(st.session_state.dfd_text.encode("utf-8"))
            input_file_path = input_file.name
        
        # 出力ファイル名を設定
        output_file_path = input_file_path.replace(".txt", f".{st.session_state.output_format}")
        
        # `data-flow-diagram` コマンドを実行
        command = [
            "data-flow-diagram",
            "-o", output_file_path,
            "-f", st.session_state.output_format,
            "--no-graph-title",
            input_file_path
        ]
        process = subprocess.run(command, capture_output=True, text=True)
        
        if process.returncode == 0:
            st.session_state.generated = True
            st.session_state.generated_file = output_file_path
            st.session_state.generated_url = f"{BASE_URL}?text={urllib.parse.quote(st.session_state.dfd_text)}"
        else:
            st.error("Error generating DFD:")
            st.text(process.stderr)

# ボタンを押してDFDを生成
st.button("Generate DFD", on_click=generate_dfd)

# ユーザー入力欄（テキストエリアをボタンの下に移動）
dfd_text = st.text_area("Enter DFD text (see [syntax document](https://github.com/pbauermeister/dfd/blob/main/doc/README.md)):", dfd_text, key="dfd_text", on_change=generate_dfd)

# 生成結果をボタンの下に表示
if st.session_state.get("generated", False):
    st.success("DFD generated successfully!")
    
    if st.session_state.output_format in ["svg", "png", "jpg"]:
        st.image(st.session_state.generated_file)
    elif st.session_state.output_format == "pdf":
        with open(st.session_state.generated_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"dfd.{st.session_state.output_format}")
    
    # URLをコピーできるボタンを追加
    st.text_input("Copy the generated DFD URL:", st.session_state.generated_url, help="Copy this URL manually")
    st.code(st.session_state.generated_url, language="text")
