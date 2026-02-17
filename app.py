import streamlit as st
import random

# Page configuration
st.set_page_config(page_title="Random Name Picker", page_icon="🎯")

# --- CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State ---
# This ensures data persists while the app is open
if 'names_list' not in st.session_state:
    st.session_state.names_list = []
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 Random Name Picker")
st.write("Enter a list of names, choose how many to pick, and watch them move to your history!")

# --- Sidebar: Management ---
with st.sidebar:
    st.header("📋 List Management")
    
    # Input area for names
    input_text = st.text_area("Paste names here (one per line):", height=200)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Load/Update"):
            # Split by newline, strip whitespace, and ignore empty lines
            new_names = [n.strip() for n in input_text.split('\n') if n.strip()]
            if new_names:
                st.session_state.names_list = new_names
                st.success(f"Loaded {len(new_names)} names!")
            else:
                st.warning("Please enter some names first.")

    with col2:
        # The requested Delete All button
        if st.button("🗑️ Delete All"):
            st.session_state.names_list = []
            st.session_state.history = []
            st.rerun()

    st.divider()
    st.info(f"Names remaining: **{len(st.session_state.names_list)}**")

# --- Main App Logic ---
if st.session_state.names_list:
    # 1. Ask how many names to pick
    max_pick = len(st.session_state.names_list)
    num_to_pick = st.number_input(
        "How many names do you want to pick?", 
        min_value=1, 
        max_value=max_pick, 
        value=1 if max_pick >= 1 else 0
    )
    
    # 2. Pick Button
    if st.button("🎲 Pick Randomly"):
        # Select random samples
        selected = random.sample(st.session_state.names_list, num_to_pick)
        
        # Display results
        st.subheader("Results:")
        cols = st.columns(min(len(selected), 3)) # Display in up to 3 columns
        for idx, name in enumerate(selected):
            cols[idx % 3].success(f"**{name}**")
            
        # 3. Update the lists (Remove from main, add to history)
        for name in selected:
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)
        
        # Small delay/refresh hint is built into Streamlit's reactive nature
else:
    st.warning("No names available. Please add some names in the sidebar to begin!")

# --- History Section ---
st.divider()
show_history = st.toggle("Show Picked History")

if show_history:
    if st.session_state.history:
        st.write("### 📜 Picked History")
        # Reverse list so the newest picks are at the top
        for h_name in reversed(st.session_state.history):
            st.text(f"• {h_name}")
    else:
        st.caption("History is currently empty.")
