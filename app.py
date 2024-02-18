import streamlit as st
import openai
from guesslang import Guess
import os
import shutil
import zipfile
import time
import base64

# Set your OpenAI GPT-3.5 API key
openai.api_key = "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"

def generate_code(prompt):
    try:
        with st.spinner("Generating code..."):
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                  "role": "system",
                  "content": 'generate pure code without any other introductory text' + prompt
                }
              ]
            )
            time.sleep(2)  # Simulate processing delay for spinner
            return response.choices[0].message["content"]
    except Exception as e:
        st.error("Error generating code: {}".format(str(e)))
        return None

def save_code_to_folder(code, language, filename, folder_name):
    folder_path = f"./{folder_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_extension = {
        "python": "py",
        "javascript": "js",
        "html": "html",
        "php": "php",
        "java": "java",
        "c++" : "cpp"
                # Add more file extensions for other languages as needed
    }
    if language in file_extension:
        file_name = f"{filename}.{file_extension[language]}"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as file:
            file.write(code)
        st.success(f"📄 Generated code saved to {file_path}")
    else:
        st.warning("❗ Unsupported language. Code not saved.")

def detect_language(code):
    guess = Guess()
    language = guess.language_name(code)
    return language.lower()

def main():
    st.title("Code Generation with GPT-3.5 Turbo")
    st.markdown("---")

    # Input prompt from the user
    prompt = st.text_area("✍️ Enter your prompt here:", height=150)

    if st.button("🚀 Generate Code", key="generate_button"):
        if prompt:
            with st.spinner("Generating code..."):
                code = generate_code(prompt)
                if code:
                    st.subheader("🎨 Processing Code:")
                    st.code(code, language='python')

                    # Allow user to specify folder name
                    folder_name = st.text_input("📁 Enter folder name:", value="generated_code")

                    # Detect language
                    language = detect_language(code)

                    if language:
                        st.info(f"🔍 Detected Language: {language}")
                        save_code_to_folder(code, language, "generated_code", folder_name)
                        # Zip the folder
                        shutil.make_archive(folder_name, 'zip', folder_name)
                        zip_file_path = f"{folder_name}.zip"
                        st.success(f"🎉 All generated files saved to {folder_name}.zip")

                        # Generate a download link for the zip file
                        with open(zip_file_path, "rb") as file:
                            zip_data = file.read()
                            zip_b64 = base64.b64encode(zip_data).decode("utf-8")
                            href = f'<a href="data:application/zip;base64,{zip_b64}" download="{zip_file_path}" class="btn btn-success">📥 Download Zip File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                    else:
                        st.warning("❗ Unable to determine language. Code not saved.")
        else:
            st.warning("⚠️ Please enter a prompt.")

if __name__ == "__main__":
    main()
