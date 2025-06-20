import sys
print(sys.path)

from utils.rag import build_vectorstore, retrieve_relevant_chunks
from utils.pdf_loader import load_course_texts, load_past_exam_texts
from utils.file_parser import extract_text_from_pdf
from utils.pdf_writer import text_to_pdf
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load your API key from .env
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

prompt_template = PromptTemplate(
    input_variables=["course_summary", "exam_examples"],
    template=open("prompts/base_prompt.txt").read()
)

chain = LLMChain(llm=llm, prompt=prompt_template)


# Build the vectorstore once (do this only when your content changes)
if not os.path.exists("chroma_db"):
    print("Building vectorstore...")
    build_vectorstore("data/content", persist_directory="chroma_db")

# When generating an exam, retrieve relevant course content
query = "university course summary"  # or a more specific topic if you want
course_text = retrieve_relevant_chunks(query, k=5, persist_directory="chroma_db")

# Past exams as before
exam_text = load_past_exam_texts("data/past_exams")

# Generate exam
exam_output = chain.run(course_summary=course_text, exam_examples=exam_text)

# Save result as PDF
text_to_pdf(
    exam_output,
    "outputs/generated_exam.pdf",
    title="Practice Exam",
    subtitle="Sample Exam for [Course Name]",
    details=[
        "Instructions: Answer all questions.",
        "Time Allowed: 2 hours",
        "This is a practice exam. No university branding is present."
    ]
)

print("✅ Practice exam generated.")