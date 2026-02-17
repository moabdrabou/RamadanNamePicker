import streamlit as st
import random
import json
import os
from collections import Counter

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
if 'initialized' not in st.session_state:
    saved_data = load_data()
    st.session_state.names_list = saved_data["names_list"]
    st.session_state.history = saved_data["history"]
    st.session_state.initialized = True

# --- Page Layout ---
st.set_page_config(page_title="Ramadan Spiritual Jar", page_icon="🌙")

st.title("🌙 Ramadan Spiritual Jar")
st.subheader("برطمان دعوات رمضان")

# --- Sidebar: Management ---
with st.sidebar:
    st.header("📋 Management")
    input_text = st.text_area("Add names from comments:", height=150, help="One name per line")
    
    if st.button("➕ Add to Jar"):
        new_entries = [n.strip() for n in input_text.split('\n') if n.strip()]
        st.session_state.names_list.extend(new_entries)
        save_data()
        st.rerun()

    st.divider()
    
    # --- DUPLICATE CHECKER SECTION ---
    st.subheader("🔍 Duplicate Check")
    # Count occurrences of each name
    counts = Counter(st.session_state.names_list)
    duplicates = [name for name, count in counts.items() if count > 1]
    
    if duplicates:
        st.warning(f"Found {len(duplicates)} duplicate names.")
        with st.expander("View Duplicates"):
            for d in duplicates:
                st.write(f"• {d} ({counts[d]} times)")
        
        if st.button("✨ Clean Duplicates"):
            # Keep order but remove duplicates
            seen = set()
            st.session_state.names_list = [x for x in st.session_state.names_list if not (x in seen or seen.add(x))]
            save_data()
            st.success("List cleaned!")
            st.rerun()
    else:
        st.success("No duplicates found!")

    st.divider()
    
    if st.button("🗑️ Reset Everything"):
        if st.checkbox("Confirm Reset"):
            st.session_state.names_list = []
            st.session_state.history = []
            save_data()
            st.rerun()

    st.metric("Total Names in Jar", len(st.session_state.names_list))

# --- Main App Logic ---
if st.session_state.names_list:
    st.write("### 📿 Daily Iftar Draw")
    num_to_pick = st.number_input("How many names to draw today?", min_value=1, max_value=len(st.session_state.names_list), value=1)
    
    if st.button("🕌 Draw Names"):
        selected = random.sample(st.session_state.names_list, num_to_pick)
        
        st.balloons() # Festive effect for the draw
        st.markdown("#### The names chosen for today's Duaa:")
        for name in selected:
            st.success(f"⭐ **{name}**")
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)
        
        save_data()
else:
    st.info("The jar is empty! Add names from your Facebook/Instagram post comments in the sidebar.")

# --- History ---
st.divider()
if st.checkbox("📜 Show History (People we prayed for)"):
    if st.session_state.history:
        for h_name in reversed(st.session_state.history):
            st.text(f"✅ {h_name}")
    else:
        st.caption("No names have been drawn yet.")
