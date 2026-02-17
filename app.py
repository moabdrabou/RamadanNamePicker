import streamlit as st
import random
import json
import os
from collections import Counter

# --- HARD-CODED KOUSA NAMES ---
# Add your priority names here. They will be picked every day.
FIXED_DAILY_NAMES = ["محمود سمير"] 

# --- إعدادات الملفات ---
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

# --- تهيئة الحالة (Session State) ---
if 'initialized' not in st.session_state:
    saved_data = load_data()
    st.session_state.names_list = saved_data.get("names_list", [])
    st.session_state.history = saved_data.get("history", [])
    st.session_state.initialized = True

# --- تصميم الصفحة وتحسين الألوان ---
st.set_page_config(page_title="Ramadan Spiritual Jar", page_icon="🌙")

st.markdown("""
    <style>
    /* تحسين شكل الأزرار */
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    
    /* إصلاح ألوان الـ Metric لتكون واضحة */
    [data-testid="stMetricValue"] { color: #007bff !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #31333F !important; }
    [data-testid="stMetric"] { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e0e0e0;
    }
    
    /* تنسيق قسم الكوسة */
    .kousa-section {
        background-color: #fff9e6;
        padding: 20px;
        border-radius: 10px;
        border: 1px dashed #ffcc00;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Ramadan Spiritual Jar")
st.subheader("برطمان دعوات رمضان")

# --- قسم الكوسة (Hard-coded display) ---
st.markdown('<div class="kousa-section">', unsafe_allow_html=True)
st.markdown("### 🌟 نظام الكوسة (أسماء ثابتة يومياً)")
st.markdown(f"**{' ، '.join(FIXED_DAILY_NAMES)}**")
st.markdown('</div>', unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("📋 الإدارة")
    input_text = st.text_area("أضف أسماء من التعليقات:", height=150, placeholder="ضع الأسماء هنا، اسم في كل سطر...")
    
    if st.button("➕ إضافة للبرطمان"):
        new_entries = [n.strip() for n in input_text.split('\n') if n.strip()]
        if new_entries:
            st.session_state.names_list.extend(new_entries)
            save_data()
            st.success(f"تم إضافة {len(new_entries)} اسم!")
            st.rerun()

    st.divider()
    
    # فحص التكرار
    st.subheader("🔍 فحص المكرر")
    counts = Counter(st.session_state.names_list)
    duplicates = [name for name, count in counts.items() if count > 1]
    if duplicates:
        st.warning(f"يوجد {len(duplicates)} أسماء مكررة.")
        if st.button("✨ تنظيف المكرر"):
            st.session_state.names_list = list(dict.fromkeys(st.session_state.names_list))
            save_data()
            st.rerun()

    st.divider()
    
    # إعادة الضبط
    st.subheader("⚠️ منطقة الخطر")
    confirm = st.checkbox("تأكيد رغبتي في مسح البيانات")
    if st.button("🗑️ مسح البرطمان والأرشيف"):
        if confirm:
            st.session_state.names_list = []
            st.session_state.history = []
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            save_data()
            st.rerun()

    st.divider()
    st.metric(label="عدد الأسماء داخل البرطمان", value=len(st.session_state.names_list))

# --- سحب الأسماء ---
st.write("### 📿 سحب اليوم")

# FIX: Dynamic logic for the number input to prevent the ValueAboveMaxError
jar_count = len(st.session_state.names_list)
max_val = max(0, jar_count)
default_val = 1 if jar_count > 0 else 0

num_random = st.number_input(
    "كم اسم عشوائي نختار اليوم؟", 
    min_value=0, 
    max_value=max_val, 
    value=default_val
)

if st.button("🕌 ابدأ السحب"):
    results = []
    
    # 1. تنفيذ نظام الكوسة أولاً
    for name in FIXED_DAILY_NAMES:
        results.append({"name": name, "type": "fixed"})
        st.session_state.history.append(name)
        if name in st.session_state.names_list:
            st.session_state.names_list.remove(name)

    # 2. السحب العشوائي
    if num_random > 0 and st.session_state.names_list:
        actual_random_count = min(num_random, len(st.session_state.names_list))
        random_picks = random.sample(st.session_state.names_list, actual_random_count)
        for name in random_picks:
            results.append({"name": name, "type": "random"})
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)

    # 3. عرض النتائج
    if results:
        st.balloons()
        st.markdown("#### أسماء اليوم المستجاب دعاؤهم بإذن الله:")
        for item in results:
            if item["type"] == "fixed":
                st.info(f"🌟 **{item['name']}** (دعوة ثابتة)")
            else:
                st.success(f"🎲 **{item['name']}** (سحب عشوائي)")
        save_data()
    else:
        st.error("البرطمان فاضي ومافيش أسماء ثابتة!")

# --- الأرشيف ---
st.divider()
if st.checkbox("📜 عرض أرشيف الدعوات"):
    if st.session_state.history:
        for name in reversed(st.session_state.history):
            st.markdown(f"- {name}")
