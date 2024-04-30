import streamlit as st
import requests
import streamlit.components.v1 as components
import os

def save_uploaded_file(uploaded_file, path):
    try:
        with open(os.path.join(path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        return False, str(e)

def main():
    st.title("Camera Control")
    st.write("Adjust camera settings")

    video_url = "http://localhost:5000/video_feed"
    html_string = f"<img src='{video_url}'/>"

    components.html(html_string, height=500)

    # 初期設定値
    bias_diff_on = st.number_input('Bias Diff ON', min_value=-10, max_value=100, value=30)
    bias_diff_off = st.number_input('Bias Diff OFF', min_value=-10, max_value=100, value=30)

    if st.button('Update Settings'):
        response = requests.post('http://localhost:5000/update_settings', json={
            'bias_diff_on': bias_diff_on,
            'bias_diff_off': bias_diff_off
        })

        if response.json()['success']:
            st.success("Settings updated successfully!")
        else:
            st.error("Failed to update settings.")

    st.write("Upload a CSV file to save it to a directory on your PC.")

    # ファイルアップローダーを作成
    uploaded_file = st.file_uploader("Choose a CSV file", type=['py'])

    # 保存先ディレクトリの入力
    path = st.text_input("Enter the path to save the file:")

    if st.button("Upload and Save"):
        if uploaded_file is not None and path:
            # ファイルを保存
            result, message = save_uploaded_file(uploaded_file, path)
            if result:
                st.success("File saved successfully!")
            else:
                st.error(f"Failed to save the file: {message}")
        else:
            st.warning("Please upload a file and specify a valid path.")

if __name__ == "__main__":
    main()