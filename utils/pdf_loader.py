import os
from utils.file_parser import extract_text_from_pdf

def load_course_texts(content_folder="data/content"):
    course_texts = []
    for root, _, files in os.walk(content_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                path = os.path.join(root, filename)
                course_texts.append(extract_text_from_pdf(path))
    return "\n\n".join(course_texts)

def load_past_exam_texts(past_exams_folder="data/past_exams"):
    exam_texts = []
    for root, _, files in os.walk(past_exams_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                path = os.path.join(root, filename)
                exam_texts.append(extract_text_from_pdf(path))
    return "\n\n".join(exam_texts)