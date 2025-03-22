import streamlit as st

from buggy_af.io import load_todos, save_todos

# Initialize session state for todos if it doesn't exist
if "todos" not in st.session_state:
    st.session_state.todos = []
if "new_todo" not in st.session_state:
    st.session_state.new_todo = ""


def add_todo():
    if st.session_state.new_todo:
        st.session_state.todos.append(
            {"task": st.session_state.new_todo, "completed": False}
        )
        save_todos(st.session_state.todos)
        st.session_state.new_todo = ""


st.title("Buggy AF - TODO List")

# Load todos on startup
if not st.session_state.todos:
    st.session_state.todos = load_todos()

# Add new todo using a form
with st.form("add_todo_form"):
    st.text_input("Add a new todo", key="new_todo")
    st.form_submit_button("Add", on_click=add_todo)

# Display todos
st.subheader("Your TODOs")
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.checkbox(todo["task"], key=f"todo_{i}", value=todo["completed"]):
            st.session_state.todos[i]["completed"] = not todo["completed"]
            save_todos(st.session_state.todos)
    with col2:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.todos.pop(i)
            save_todos(st.session_state.todos)
            st.rerun()
