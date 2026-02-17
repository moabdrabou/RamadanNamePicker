import streamlit as st
import random
import json
import os
from collections import Counter

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

# --- تصميم الصفحة ---
st.set_page_config(page_title="Ramadan Spiritual Jar", page_icon="🌙")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #28a745 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #31333F !important; }
    [data-testid="stMetric"] { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Ramadan Spiritual Jar")
st.subheader("برطمان دعوات رمضان")

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("📋 الإدارة")
    
    input_text = st.text_area("أضف أسماء جديدة (اسم في كل سطر):", height=100)
    
    if st.button("➕ إضافة للبرطمان"):
        new_entries = [n.strip() for n in input_text.split('\n') if n.strip()]
        if new_entries:
            st.session_state.names_list.extend(new_entries)
            save_data()
            st.success(f"تم إضافة {len(new_entries)} اسم!")
            st.rerun()

    st.divider()

    # --- نظام الكوسة (أسماء ثابتة يومياً) ---
    st.subheader("🌟 نظام الكوسة (أسماء ثابتة)")
    st.write("الأسماء دي هتطلع كل يوم (True Condition) بره القرعة العشوائية.")
    fixed_name_1 = st.text_input("الاسم الأول الثابت", key="fixed_1")
    fixed_name_2 = st.text_input("الاسم الثاني الثابت", key="fixed_2")
    fixed_name_3 = st.text_input("الاسم الثالث الثابت", key="fixed_3")
    
    # تحويل الأسماء الثابتة لقائمة (تجاهل الفراغات)
    fixed_winners = [n.strip() for n in [fixed_name_1, fixed_name_2, fixed_name_3] if n.strip()]

    st.divider()
    
    # حذف التكرار
    if st.button("✨ تنظيف الأسماء المكررة"):
        st.session_state.names_list = list(dict.fromkeys(st.session_state.names_list))
        save_data()
        st.rerun()

    # إعادة ضبط
    st.subheader("⚠️ خطر")
    if st.checkbox("تأكيد مسح كل البيانات"):
        if st.button("🗑️ مسح البرطمان والارشيف"):
            st.session_state.names_list = []
            st.session_state.history = []
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            save_data()
            st.rerun()

    st.divider()
    st.metric(label="عدد الأسماء في البرطمان", value=len(st.session_state.names_list))

# --- المنطق الأساسي للسحب ---
st.write("### 📿 سحب دعوات اليوم")

if st.button("🕌 اسحب الأسماء الآن"):
    results = []
    
    # 1. نظام الكوسة (True Condition): أضف الأسماء الثابتة أولاً دائماً
    for name in fixed_winners:
        results.append({"name": name, "type": "fixed"})
        st.session_state.history.append(name)
        # إذا كان الاسم موجود في البرطمان، احذفه عشان ميتكررش
        if name in st.session_state.names_list:
            st.session_state.names_list.remove(name)

    # 2. نظام القرعة العشوائية: كمل العدد لـ 3 لو الأسماء الثابتة أقل من 3
    needed_random = 3 - len(results)
    if needed_random > 0 and st.session_state.names_list:
        actual_random_count = min(needed_random, len(st.session_state.names_list))
        random_picks = random.sample(st.session_state.names_list, actual_random_count)
        
        for name in random_picks:
            results.append({"name": name, "type": "random"})
            st.session_state.names_list.remove(name)
            st.session_state.history.append(name)

    # 3. عرض النتائج
    if results:
        st.balloons()
        st.markdown("#### أسماء النهاردة اللي هندعيلهم:")
        for res in results:
            if res["type"] == "fixed":
                st.info(f"✨ **{res['name']}** (دعوة ثابتة يومياً)")
            else:
                st.success(f"🌙 **{res['name']}** (سحب عشوائي من البرطمان)")
        save_data()
    else:
        st.error("البرطمان فاضي ومافيش أسماء ثابتة!")

# --- الأرشيف ---
st.divider()
if st.checkbox("📜 عرض أرشيف الدعوات"):
    if st.session_state.history:
        for name in reversed(st.session_state.history):
            st.markdown(f"- {name}")
    else:
        st.caption("لسه مابدأناش سحب!")
