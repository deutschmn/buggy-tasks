# Standard library imports

# Third-party imports
import streamlit as st
import pandas as pd

# Local application imports
from buggy_tasks.commands import process_command, registry
from buggy_tasks.io import load_todos, save_todos
from buggy_tasks.derive_tags import derive_tags_from_text
from buggy_tasks.priority import compute_priority

# Initialize session state variables
# This ensures we have defaults for all required state


def initialize_session_state():
    """Initialize the session state with default values if they don't exist"""
    if "todos" not in st.session_state:
        st.session_state.todos = []
    if "new_todo" not in st.session_state:
        st.session_state.new_todo = ""


# Call initialization function
initialize_session_state()


def add_todo():
    """
    Add a new todo item to the application.

    This function processes the text in st.session_state.new_todo:
    1. Applies any slash commands
    2. Derives tags using AI
    3. Calculates priority
    4. Adds the todo to the session state
    5. Saves the updated todo list
    """
    # Check if there is actually a todo to add
    if st.session_state.new_todo:
        # Step 1: Process any slash commands in the new todo
        processed_text = process_command(st.session_state.new_todo)

        # Step 2: Derive tags using AI
        tags = derive_tags_from_text(processed_text)

        # Step 3: Calculate priority score based on tags
        priority_score = compute_priority(tags)

        # Step 4: Create and add the new todo item
        todo_item = {
            "task": processed_text,
            "completed": False,
            "tags": tags,
            "priority": priority_score
        }
        # Insert at the beginning of the list (newest first)
        st.session_state.todos.insert(0, todo_item)

        # Step 5: Save and reset input
        save_todos(st.session_state.todos)
        st.session_state.new_todo = ""


def clear_todos():
    """Remove all todos from the session state and save the empty list"""
    # Reset the todos list
    st.session_state.todos = []
    # Make sure to persist the change to storage
    save_todos(st.session_state.todos)


def insert_command_example(example: str) -> None:
    """
    Set the new_todo input field to the given example command

    Args:
        example: The example command string to insert
    """
    st.session_state.new_todo = example


def display_todos_with_data_editor():
    """Display todos in an editable data table using Streamlit's data_editor"""
    # Transform todo dictionaries to a format suitable for display
    todo_display_data = []
    for todo_item in st.session_state.todos:
        # Create a display-friendly record for each todo
        display_record = {
            "Task": todo_item["task"],
            "Completed": todo_item["completed"],
            "Tags": ", ".join(todo_item["tags"]),
            "Priority": todo_item["priority"],
        }
        todo_display_data.append(display_record)

    # Create pandas DataFrame from the display data
    todo_df = pd.DataFrame(todo_display_data)

    # Add deletion functionality via checkbox column
    todo_df["Delete"] = False

    # Make sure the Delete column appears at the end
    column_order = todo_df.columns[:-1].tolist() + ["Delete"]
    todo_df = todo_df[column_order]

    # Use st.data_editor for an editable table
    edited_df = st.data_editor(
        todo_df,
        key="data_editor",
        hide_index=True,
        column_config={
            "Completed": st.column_config.CheckboxColumn("Completed"),
            "Tags": st.column_config.TextColumn("Tags"),
            "Priority": st.column_config.NumberColumn("Priority", disabled=True),
            "Delete": st.column_config.CheckboxColumn("Delete"),
        },
    )

    # Process any rows marked for deletion
    rows_marked_for_deletion = edited_df[edited_df["Delete"]].index
    # Check if any rows need to be deleted
    if not rows_marked_for_deletion.empty:
        # Filter out the todos that should be deleted using list comprehension
        indices_to_delete = [i - 1 for i in rows_marked_for_deletion if i - 1 >= 0]
        st.session_state.todos = [
            todo for i, todo in enumerate(st.session_state.todos) if i not in indices_to_delete
        ]
        # Persist changes to storage
        save_todos(st.session_state.todos)
        # Refresh the UI to reflect changes
        st.rerun()

    # Apply any edits made in the data editor to our todos list
    updated_todos_list = []
    # Process each row in the edited dataframe
    for idx, data_row in edited_df.iterrows():
        # Create a new todo item with the edited values
        updated_todo = {
            "task": data_row["Task"],
            "completed": data_row["Completed"],
            # Split comma-separated tags string back into a list, stripping whitespace
            "tags": [tag.strip() for tag in data_row["Tags"].split(",") if tag.strip()],
            "priority": data_row["Priority"],
        }
        # Add to our updated list
        updated_todos_list.append(updated_todo)

    st.session_state.todos = updated_todos_list
    save_todos(st.session_state.todos)


# Application title with emoji
st.title("✨ Buggy Tasks - To Do List ✨")

# Load saved todos from storage on application startup
if not st.session_state.todos:
    # If no todos in session state, load them from persistent storage
    st.session_state.todos = load_todos()

# Create a form for adding new todos with a modern UI
with st.form(key="add_todo_form", clear_on_submit=False):
    # Use columns for a nice layout: input field and button side by side
    input_col, button_col = st.columns([3, 1])

    # Input field in the first (wider) column
    with input_col:
        st.text_input(
            label="Add a new todo",
            key="new_todo",
            label_visibility="collapsed",  # Hide the label for cleaner UI
            placeholder="Type / to use commands or just enter a task",
        )

    # Submit button in the second (narrower) column
    with button_col:
        st.form_submit_button(
            label="Add ➕",
            on_click=add_todo,
            use_container_width=True
        )

# Expandable section to show available commands
with st.expander("Commands 🚀"):
    # Get all registered commands
    available_commands = registry.get_commands()

    # Display each command with its description and example
    for command in available_commands:
        # Use columns for better layout
        info_column, action_column = st.columns([3, 1])

        # Command info in the first column
        with info_column:
            st.markdown(f"**{command.name}**")
            st.markdown(f"*{command.description}*")
            st.markdown(f"`{command.example}`")

        # Quick action button in the second column
        with action_column:
            st.button(
                label="Try It",
                key=f"use_{command.name}",
                on_click=insert_command_example,
                args=(command.example,),
                use_container_width=True
            )

# Display todos section header with icon
st.subheader("📋 My Todos")

# Handle empty state vs. populated state
if not st.session_state.todos:
    # Show a friendly message when no todos exist
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <p><em>Your todo list is empty. Add your first task above!</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Display the interactive todo table
    display_todos_with_data_editor()

    # Add a button to clear all todos (with confirmation)
    col1, col2, col3 = st.columns([3, 3, 2])
    with col3:
        if st.button("Clear All Tasks", type="secondary", use_container_width=True):
            clear_todos()
            st.rerun()
