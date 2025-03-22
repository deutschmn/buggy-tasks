import streamlit as st

from buggy_tasks.commands import process_command, registry
from buggy_tasks.io import load_todos, save_todos

# Initialize session state for todos if it doesn't exist
if "todos" not in st.session_state:
    st.session_state.todos = []
if "new_todo" not in st.session_state:
    st.session_state.new_todo = ""


def add_todo():
    if st.session_state.new_todo:
        # Process any slash commands in the new todo
        processed_todo = process_command(st.session_state.new_todo)
        st.session_state.todos.insert(0, {"task": processed_todo, "completed": False})
        save_todos(st.session_state.todos)
        st.session_state.new_todo = ""


def clear_todos():
    st.session_state.todos = []
    save_todos(st.session_state.todos)


def insert_command_example(example: str):
    st.session_state.new_todo = example


st.title("Buggy Tasks - To Do List")

# Load todos on startup
if not st.session_state.todos:
    st.session_state.todos = load_todos()

# Add new todo using a form
with st.form("add_todo_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input(
            "Add a new todo",
            key="new_todo",
            label_visibility="collapsed",
            placeholder="Type / to use commands",
        )
    with col2:
        st.form_submit_button("Add ➕", on_click=add_todo)

# Commands expander
with st.expander("Commands 🚀"):
    for cmd in registry.get_commands():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{cmd.name}**")
            st.markdown(f"*{cmd.description}*")
            st.markdown(f"`{cmd.example}`")
        with col2:
            st.button(
                "Use Example",
                key=f"use_{cmd.name}",
                on_click=insert_command_example,
                args=(cmd.example,),
            )

# Display todos
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.checkbox(todo["task"], key=f"todo_{i}", value=todo["completed"]):
            st.session_state.todos[i]["completed"] = not todo["completed"]
            save_todos(st.session_state.todos)
    with col2:
        if st.button("🗑️", key=f"delete_{i}", help="Delete todo"):
            st.session_state.todos.pop(i)
            save_todos(st.session_state.todos)
            st.rerun()

# Clear all todos button
if st.button("Clear All", type="secondary"):
    clear_todos()
    st.rerun()
