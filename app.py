import streamlit as st
import random
import json
import os
from collections import Counter

# --- File Handling Logic ---
DB_FILE = "data.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"names_list": [], "history": []}
    return {"names_list": [], "history": []}

def save_data():
    data = {
        "names_list": st.session_state.names_list,
        "history": st.session_state.history
    }
    with open(DB_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Initialize Session State ---
if 'initialized' not in st.session_state:
    saved_data = load_data()
    st.session_state.names_list = saved_data.get("names_list", [])
    st.session_state.history = saved_data.get("history", [])
    st.session_state.initialized = True

# --- Page Layout & Theme ---
st.set_page_config(page_title="Ramadan Spiritual Jar", page_icon="🌙")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Ramadan Spiritual Jar")
st.subheader("برطمان دعوات رمضان")

# --- Sidebar: Management ---
with st.sidebar:
    st.header("📋 Management")
    
    # Input area
    input_text = st.text_area("Add names from comments:", height=150, help="Paste names here, one per line.")
    
    if st.button("➕ Add to Jar"):
        new_entries = [n.strip() for n in input_text.split('\n') if n.strip()]
        if new_entries:
            st.session_state.names_list.extend(new_entries)
            save_data()
            st.success(f"Added {len(new_entries)} names!")
            st.rerun()

    st.divider()
    
    # Duplicate Checker
    st.subheader("🔍 Duplicate Check")
    counts = Counter(st.session_state.names_list)
    duplicates = [name for name, count in counts.items() if count > 1]
    
    if duplicates:
        st.warning(f"Found {len(duplicates)} duplicates.")
        with st.expander("View Duplicates"):
            for d in duplicates:
                st.write(f"• {d} ({counts[d]} times)")
        
        if st.button("✨ Clean Duplicates"):
            seen = set()
            st.session_state.names_list = [x for x in st.session_state.names_list if not (x in seen or seen.add(x))]
            save_data()
            st.rerun()
    else:
        st.caption("No duplicates found.")

    st.divider()
    
    # Reset Logic
    st.subheader("⚠️ Danger Zone")
    confirm_reset = st.checkbox("Confirm I want to wipe all data")
    if st.button("🗑️ Reset Everything"):
        if confirm_reset:
            st.session_state.names_list = []
            st.session_state.history = []
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE) # Clean the physical file too
            save_data()
            st.success("Jar and History wiped!")
            st.rerun()
        else:
            st.error("Check the confirmation box first!")

    st.divider()
    st.metric("Names in Jar", len(st.session_state.names_list))

# --- Main App Logic ---
if st.session_state.names_list:
    st.write("### 📿 Daily Iftar Draw")
    num_to_pick = st.number_input("How many names to draw?", min_value=1, max_value=len(st.session_state.names_list), value=1)
    
    if st.button("🕌 Draw Names"):
        selected = random.sample(st.session_state.names_list, num_to_pick)
        
        st.balloons()
        st.markdown("#### Today's Selected Names:")
        for name in selected:
            st.success(f"⭐ **{name}**")
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)
        
        save_data()
else:
    st.info("The jar is empty! Add names in the sidebar to get started.")

# --- History ---
st.divider()
if st.checkbox("📜 Show History (People we prayed for)"):
    if st.session_state.history:
        # Show in a table for easier reading
        st.table(st.session_state.history[::-1])
    else:
        st.caption("No names drawn yet.")
