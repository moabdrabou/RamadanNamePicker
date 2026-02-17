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

# --- تصميم الصفحة وتحسين الألوان ---
st.set_page_config(page_title="Ramadan Spiritual Jar", page_icon="🌙")

st.markdown("""
    <style>
    /* تحسين شكل الأزرار */
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    
    /* إصلاح ألوان الـ Metric لتكون واضحة (علاج المشكلة في الصورة) */
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
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Ramadan Spiritual Jar")
st.subheader("برطمان دعوات رمضان")

# --- قسم الكوسة (مباشرة تحت العنوان) ---
st.markdown('<div class="kousa-section">', unsafe_allow_html=True)
st.markdown("### 🌟 نظام الكوسة (أسماء ثابتة يومياً)")
col_a, col_b, col_c = st.columns(3)
with col_a:
    f1 = st.text_input("الاسم الثابت 1", key="k1", placeholder="مثلاً: والدي")
with col_b:
    f2 = st.text_input("الاسم الثابت 2", key="k2", placeholder="مثلاً: والدتي")
with col_c:
    f3 = st.text_input("الاسم الثابت 3", key="k3", placeholder="مثلاً: اسمي")
st.markdown('</div>', unsafe_allow_html=True)

# تحويل الأسماء الثابتة لقائمة
fixed_winners = [n.strip() for n in [f1, f2, f3] if n.strip()]

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
if st.session_state.names_list or fixed_winners:
    num_random = st.number_input("كم اسم عشوائي نختار اليوم؟", min_value=0, max_value=len(st.session_state.names_list), value=1)
    
    if st.button("🕌 ابدأ السحب"):
        results = []
        
        # 1. تنفيذ نظام الكوسة أولاً
        for name in fixed_winners:
            results.append({"name": name, "type": "fixed"})
            st.session_state.history.append(name)
            if name in st.session_state.names_list:
                st.session_state.names_list.remove(name)

        # 2. السحب العشوائي
        if num_random > 0 and st.session_state.names_list:
            random_picks = random.sample(st.session_state.names_list, num_random)
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
    st.info("البرطمان فارغ! أضف أسماء من القائمة الجانبية أو أدخل أسماء ثابتة.")

# --- الأرشيف ---
st.divider()
if st.checkbox("📜 عرض أرشيف الدعوات"):
    if st.session_state.history:
        for name in reversed(st.session_state.history):
            st.markdown(f"- {name}")
