import streamlit as st

from buggy_af.io import load_todos, save_todos

# Initialize session state for todos if it doesn't exist
if "todos" not in st.session_state:
    st.session_state.todos = []

st.title("Buggy AF - TODO List")

# Load todos on startup
if not st.session_state.todos:
    st.session_state.todos = load_todos()

# Add new todo
new_todo = st.text_input("Add a new todo")
if st.button("Add") and new_todo:
    st.session_state.todos.append({"task": new_todo, "completed": False})
    save_todos(st.session_state.todos)
    st.text_input("Add a new todo", value="", key="clear_input")

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
