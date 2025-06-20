import streamlit as st
import os

def course_sidebar(base_dir="user_data"):
    st.sidebar.title("Your Courses")
    os.makedirs(base_dir, exist_ok=True)
    courses = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    # Add new course section
    with st.sidebar:
        new_course = st.text_input("Add new course")
        if st.button("Create Course") and new_course:
            course_path = os.path.join(base_dir, new_course)
            os.makedirs(os.path.join(course_path, "content"), exist_ok=True)
            os.makedirs(os.path.join(course_path, "past_exams"), exist_ok=True)
            os.makedirs(os.path.join(course_path, "generated_exams"), exist_ok=True)
            st.rerun()

    selected_course = None
    for course in courses:
        with st.sidebar.expander(course):
            st.write("Content files:")
            content_dir = os.path.join(base_dir, course, "content")
            files = os.listdir(content_dir) if os.path.exists(content_dir) else []
            for f in files:
                st.write(f"- {f}")
            st.write("Past exams:")
            exams_dir = os.path.join(base_dir, course, "past_exams")
            exams = os.listdir(exams_dir) if os.path.exists(exams_dir) else []
            for f in exams:
                st.write(f"- {f}")
            if st.button(f"Select {course}"):
                st.session_state["selected_course"] = course

    # Return the selected course path
    selected_course = st.session_state.get("selected_course")
    if selected_course:
        return os.path.join(base_dir, selected_course)
    return None