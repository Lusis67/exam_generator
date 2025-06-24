from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

openai_api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from ui.sidebar import course_sidebar

# Load credentials from YAML
with open("users.yaml") as file:
    config = yaml.safe_load(file)
st.write("DEBUG: Loaded YAML config")

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.write("DEBUG: Authenticator initialized")

login_result = authenticator.login('main')
st.write("DEBUG: login_result =", login_result)
# Defensive unpacking
if isinstance(login_result, tuple) and len(login_result) == 3:
    name, authentication_status, username = login_result
else:
    name = username = None
    authentication_status = login_result
st.write("DEBUG: authentication_status =", authentication_status)
st.write("DEBUG: authentication_status type =", type(authentication_status)) 
st.write("DEBUG: name =", name)
st.write("DEBUG: username =", username)

if authentication_status is True:
    st.success(f"Welcome, {name}!")
    st.sidebar.success(f"Logged in as {name} ({username})")
    course_path = course_sidebar()
    st.write("DEBUG: course_path =", course_path)

    if course_path:
        import os
        from utils.rag import build_vectorstore, retrieve_relevant_chunks
        from utils.pdf_loader import load_past_exam_texts
        from utils.pdf_writer import text_to_pdf
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from langchain_openai import ChatOpenAI

        chroma_db_path = os.path.join(course_path, "chroma_db")

        # Check if vectorstore exists
        if not os.path.exists(chroma_db_path):
            st.header("Upload Course Content PDFs")
            course_files = st.file_uploader("Course PDFs", type="pdf", accept_multiple_files=True)
            st.header("Upload Past Exam PDFs")
            exam_files = st.file_uploader("Past Exam PDFs", type="pdf", accept_multiple_files=True)
            if st.button("Save and Embed Documents"):
                # Save files
                if course_files:
                    for f in course_files:
                        with open(os.path.join(course_path, "content", f.name), "wb") as out:
                            out.write(f.read())
                if exam_files:
                    for f in exam_files:
                        with open(os.path.join(course_path, "past_exams", f.name), "wb") as out:
                            out.write(f.read())
                # Build vectorstore
                build_vectorstore(os.path.join(course_path, "content"), persist_directory=chroma_db_path)
                st.success("Documents embedded! You can now generate practice exams.")
                st.rerun()
            st.stop()
        else:
            st.success("Course documents already embedded. You can generate practice exams below.")

            num_questions = st.number_input("Number of Questions", min_value=1, max_value=5, value=3)
            custom_prompt = st.text_area(
                "Custom Prompt (optional)",
                placeholder="Type your custom instructions or prompt here. Leave blank to use the default."
            )
            if st.button("Generate Practice Exam"):
                query = f"{os.path.basename(course_path)} course summary"
                course_text = retrieve_relevant_chunks(query, k=5, persist_directory=chroma_db_path)
                exam_text = load_past_exam_texts(os.path.join(course_path, "past_exams"))

                # Generate exam
                llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
                prompt_template = PromptTemplate(
                    input_variables=["course_summary", "exam_examples"],
                    template=open("prompts/base_prompt.txt").read()
                )
                chain = LLMChain(llm=llm, prompt=prompt_template)
                exam_output = chain.run(course_summary=course_text, exam_examples=exam_text)

                # Write PDF to course's generated_exams folder
                pdf_path = os.path.join(course_path, "generated_exams", "practice_exam.pdf")
                text_to_pdf(
                    exam_output,
                    pdf_path,
                    title="Practice Exam",
                    subtitle=f"Sample Exam for {os.path.basename(course_path)}"
                )

                # Download link
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download Practice Exam PDF",
                        f,
                        file_name="practice_exam.pdf",
                        mime="application/pdf"
                    )
                st.markdown("---")
                st.subheader("We want to give you the best preparation possible!")
                st.write("Let us know how the practice exam could be improved.")

                # Star rating (0-5)
                rating = st.slider("How would you rate this practice exam?", 0, 5, 0)

                # Optional feedback text
                feedback = st.text_area("Additional feedback (optional):", placeholder="Type your suggestions here...")

                if st.button("Submit Feedback"):
                    import csv
                    feedback_path = os.path.join(course_path, "generated_exams", "feedback.csv")
                    with open(feedback_path, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([rating, feedback])
                    st.success("Thank you for your feedback!")
    else:
        st.info("Please select or create a course in the sidebar to continue.")
        st.write("DEBUG: No course selected")
elif authentication_status is False:
    st.error("Username/password is incorrect")
    st.write("DEBUG: Incorrect username/password")
elif authentication_status is None:
    st.warning("Please enter your username and password")
    st.write("DEBUG: Awaiting username/password")