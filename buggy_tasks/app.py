import streamlit as st
import pandas as pd

from buggy_tasks.commands import process_command, registry
from buggy_tasks.io import load_todos, save_todos
from buggy_tasks.derive_tags import derive_tags_from_text

# Initialize session state for todos if it doesn't exist
if "todos" not in st.session_state:
    st.session_state.todos = []
if "new_todo" not in st.session_state:
    st.session_state.new_todo = ""


def add_todo():
    if st.session_state.new_todo:
        # Process any slash commands in the new todo
        processed_todo = process_command(st.session_state.new_todo)
        # Automatically derive tags using Mistral AI
        derived_tags = derive_tags_from_text(processed_todo)
        st.session_state.todos.insert(
            0, {"task": processed_todo, "completed": False, "tags": derived_tags})
        save_todos(st.session_state.todos)
        st.session_state.new_todo = ""


def clear_todos():
    st.session_state.todos = []
    save_todos(st.session_state.todos)


def insert_command_example(example: str):
    st.session_state.new_todo = example


def display_todos_with_data_editor():
    # Prepare data for the table
    data = [
        {
            "Task": todo["task"],
            "Completed": todo["completed"],
            "Tags": ", ".join(todo["tags"]),
        }
        for todo in st.session_state.todos
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Add a checkbox column for deletion
    df["Delete"] = False

    # Ensure Delete is the last column
    df = df[df.columns[:-1].tolist() + ["Delete"]]

    # Use st.data_editor for an editable table
    edited_df = st.data_editor(
        df,
        key="data_editor",
        hide_index=True,
        column_config={
            "Completed": st.column_config.CheckboxColumn("Completed"),
            "Tags": st.column_config.TextColumn("Tags"),
            "Delete": st.column_config.CheckboxColumn("Delete"),
        },
    )

    # Handle deletions
    rows_to_delete = edited_df[edited_df["Delete"]].index
    if not rows_to_delete.empty:
        st.session_state.todos = [
            todo for i, todo in enumerate(st.session_state.todos) if i not in rows_to_delete
        ]
        save_todos(st.session_state.todos)
        st.rerun()

    # Update session state with edited data
    updated_todos = []
    for i, row in edited_df.iterrows():
        updated_todos.append({
            "task": row["Task"],
            "completed": row["Completed"],
            "tags": [tag.strip() for tag in row["Tags"].split(",") if tag.strip()],
        })

    st.session_state.todos = updated_todos
    save_todos(st.session_state.todos)


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
st.subheader("My Todos")


if not st.session_state.todos:
    st.write("*No todos yet!*")
else:
    display_todos_with_data_editor()

    # Clear all todos button
    if st.button("Clear All", type="secondary"):
        clear_todos()
        st.rerun()
