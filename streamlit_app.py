import subprocess
import tempfile
import os
import streamlit as st
import urllib.parse

# Streamlitアプリのタイトル
st.title("DFD Generator with Streamlit")

# 現在のアプリのURLを取得（仮のURLを設定、実際にはデプロイ時に変更）
BASE_URL = os.getenv("BASE_URL", "https://this.app.url/")

# URLパラメータからDFDのテキストを取得（指定がない場合は空の文字列）
query_params = st.query_params

dfd_text = query_params.get("text", "")
if dfd_text:
    dfd_text = urllib.parse.unquote(dfd_text)
    st.success("DFD text loaded from URL.")

# ユーザー入力欄（DFDのテキストを受け取る）
dfd_text = st.text_area("Enter DFD text (see [syntax document](https://github.com/pbauermeister/dfd/blob/main/doc/README.md)):", dfd_text)

# 画像出力フォーマットの選択
output_format = st.selectbox("Select output format:", ["svg", "png", "pdf", "jpg"], index=0)

# ボタンを押すとDFD画像を生成
if st.button("Generate DFD"):
    if dfd_text.strip():
        # 一時ファイルを作成してDFDのテキストを保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as input_file:
            input_file.write(dfd_text.encode("utf-8"))
            input_file_path = input_file.name
        
        # 出力ファイル名を設定
        output_file_path = input_file_path.replace(".txt", f".{output_format}")
        
        # `data-flow-diagram` コマンドを実行
        command = [
            "data-flow-diagram",
            "-o", output_file_path,
            "-f", output_format,
            "--no-graph-title",
            input_file_path
        ]
        process = subprocess.run(command, capture_output=True, text=True)
        
        if process.returncode == 0:
            st.success("DFD generated successfully!")
            
            # 画像を表示
            if output_format in ["svg", "png", "jpg"]:
                st.image(output_file_path)
            elif output_format == "pdf":
                with open(output_file_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name=f"dfd.{output_format}")
            
            # テキストをエンコードしてURLを生成
            encoded_text = urllib.parse.quote(dfd_text)
            generated_url = f"{BASE_URL}?text={encoded_text}"
            
            # URLをコピーできるボタンを追加
            st.text_input("Copy the generated DFD URL:", generated_url, help="Copy this URL manually")
            st.code(generated_url, language="text", line_numbers=True, wrap_lines=True)
        else:
            st.error("Error generating DFD:")
            st.text(process.stderr)
    else:
        st.warning("Please enter valid DFD text.")