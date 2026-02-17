import streamlit as st
import random
import json
import os

# --- File Handling Logic ---
DB_FILE = "data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"names_list": [], "history": []}

def save_data():
    data = {
        "names_list": st.session_state.names_list,
        "history": st.session_state.history
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- Initialize Session State ---
# Load from file if session state is empty
if 'initialized' not in st.session_state:
    saved_data = load_data()
    st.session_state.names_list = saved_data["names_list"]
    st.session_state.history = saved_data["history"]
    st.session_state.initialized = True

# --- Page Layout & Styling ---
st.set_page_config(page_title="Daily Name Picker", page_icon="📅")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 Daily Random Picker")

# --- Sidebar ---
with st.sidebar:
    st.header("📋 Management")
    input_text = st.text_area("Add new names (one per line):", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Names"):
            new_entries = [n.strip() for n in input_text.split('\n') if n.strip()]
            st.session_state.names_list.extend(new_entries)
            save_data() # Save to disk
            st.rerun()

    with col2:
        if st.button("🗑️ Reset All"):
            st.session_state.names_list = []
            st.session_state.history = []
            save_data() # Save empty state to disk
            st.rerun()

    st.divider()
    st.metric("Names Left", len(st.session_state.names_list))

# --- Main Logic ---
if st.session_state.names_list:
    num_to_pick = st.number_input("How many names today?", min_value=1, max_value=len(st.session_state.names_list), value=1)
    
    if st.button("🎲 Pick Today's Names"):
        selected = random.sample(st.session_state.names_list, num_to_pick)
        
        st.subheader("Selected for today:")
        for name in selected:
            st.success(f"⭐ **{name}**")
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)
        
        save_data() # Save the updated lists to disk
else:
    st.info("The list is empty! Please add names in the sidebar.")

# --- History ---
st.divider()
if st.checkbox("Show Picked History"):
    if st.session_state.history:
        # Show newest at the top
        for h_name in reversed(st.session_state.history):
            st.text(f"• {h_name}")
    else:
        st.caption("No history recorded yet.")
