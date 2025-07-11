import streamlit as st
from google_search import search_with_trust
from gemini_interface import ask_gemini
from answer import format_answer
from context import FIELD_CONTEXTS, FIELD_QUERY_OVERRIDES
from history_manager import save_full_search, get_history_strings, get_history_entry, delete_history_entry
from utils import (
    map_user_category,
    map_purpose_category,
    map_sdg_category,
    clean_answer_text,
    get_all_sheet1_fields,
    get_all_sheet2_fields,
    extract_sdg_numbers
)

# --- Streamlit Page Config ---
st.set_page_config(page_title="Satellite Data Chatbot", layout="wide")

if "query_done" not in st.session_state:
    st.session_state.query_done = False
if "current_satellite" not in st.session_state:
    st.session_state.current_satellite = ""
if "current_fields" not in st.session_state:
    st.session_state.current_fields = []
if "current_sheet" not in st.session_state:
    st.session_state.current_sheet = ""
if "selected_history_index" not in st.session_state:
    st.session_state.selected_history_index = None

st.title("🛰️ Satellite Query Chatbot")

if st.sidebar.button("🔄 New Search"):
    st.session_state.query_done = False
    st.session_state.selected_history_index = None
    st.session_state.current_satellite = ""
    st.session_state.current_fields = []
    st.session_state.current_sheet = ""
    st.rerun()

if st.sidebar.button("🗑️ Clear All History"):
    from history_manager import clear_history
    clear_history()
    st.session_state.selected_history_index = None
    st.rerun()

# --- Sidebar: History Viewer ---
st.sidebar.markdown("## 📜 Search History")
search_filter = st.sidebar.text_input("Search satellite...", "")

# Load and filter history
search_history = get_history_strings()
filtered_history = [
    (i, label) for i, label in enumerate(search_history[::-1])  # latest first
    if search_filter.lower() in label.lower()
]

if filtered_history:
    for i, label in filtered_history:
        col1, col2 = st.sidebar.columns([6, 1])
        with col1:
            if st.button(label, key=f"history_{i}"):
                st.session_state.selected_history_index = i
                st.session_state.query_done = False
                st.rerun()
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                delete_history_entry(i)
                if st.session_state.selected_history_index == i:
                    st.session_state.selected_history_index = None
                st.rerun()
else:
    st.sidebar.info("No matching history found.")

# Track selected entry in session state
if "selected_history_index" not in st.session_state:
    st.session_state.selected_history_index = None

# --- Run a Search and Collect Results ---
def run_satellite_query(satellite_name, sheet_option, selected_fields):
    results = {}
    for field in selected_fields:
        field_lower = field.lower()
        extra_context = ""
        query_template = FIELD_QUERY_OVERRIDES.get(field_lower, "{satellite} {field}")
        query = query_template.format(satellite=satellite_name, field=field)

        raw_snippet, source_url, trust_level = search_with_trust(query)
        if not raw_snippet:
            raw_snippet = "Data not available"
            source_url = None

        for key in FIELD_CONTEXTS:
            if key in field_lower:
                extra_context = FIELD_CONTEXTS[key]
                break

        answer = ask_gemini(satellite_name, field, raw_snippet, source_url, extra_context)
        answer = clean_answer_text(answer)

        if answer.lower() == "data not available" and trust_level != "tertiary":
            raw_snippet, source_url, trust_level = search_with_trust(query, try_open_search=True)
            if raw_snippet:
                answer = ask_gemini(satellite_name, field, raw_snippet, source_url, extra_context)
                answer = clean_answer_text(answer)

        # Process for GPT data tab (Sheet2)
        if "Sheet2" in sheet_option:
            if field_lower == "user":
                answer, _ = map_user_category(answer)
            elif field_lower == "user category number":
                _, number = map_user_category(answer)
                answer = str(number) if number is not None else "Data not available"
            elif field_lower == "purpose":
                answer, _ = map_purpose_category(answer)
            elif field_lower == "purpose category number":
                _, number = map_purpose_category(answer)
                answer = str(number) if number is not None else "Data not available"
            elif field_lower == "sdg category":
                sdg_numbers = extract_sdg_numbers(answer)
                category, _ = map_sdg_category(sdg_numbers)
                answer = category if category else "Data not available"
            elif field_lower == "sdg category identification numbers":
                sdg_numbers = extract_sdg_numbers(answer)
                _, number = map_sdg_category(sdg_numbers)
                answer = str(number) if number else "Data not available"

        results[field] = {
            "answer": answer,
            "source_url": source_url,
            "trust_level": trust_level
        }

        formatted = format_answer(field, answer, source_url, trust_level)
        st.markdown(formatted)
        st.markdown("---")

    return results

# --- If a History Item is Clicked, Render Cached Result ---
if st.session_state.selected_history_index is not None:
    cached = get_history_entry(st.session_state.selected_history_index)
    satellite = cached["satellite"]
    sheet = cached["sheet"]
    fields = cached["fields"]
    results = cached["results"]

    st.info(f"📜 Showing saved results for: **{satellite} | {sheet}** (Read-only)")
    for field in fields:
        result = results.get(field, {})
        answer = result.get("answer", "Data not available")
        source_url = result.get("source_url")
        trust_level = result.get("trust_level", "unknown")
        formatted = format_answer(field, answer, source_url, trust_level)
        st.markdown(formatted)
        st.markdown("---")

# --- New Search Mode ---
else:
    st.markdown("### 🔍 New Satellite Search")

    sheet_option = st.radio(
        "Select which sheet to query:",
        ["data tab (Sheet1)", "gpt data tab (Sheet2)"]
    )

    fields = get_all_sheet1_fields() if "Sheet1" in sheet_option else get_all_sheet2_fields()
    satellite_name = st.text_input("Enter Satellite Name")
    selected_fields = st.multiselect("Select specific queries:", options=fields, default=[])

    if st.checkbox("Select all queries"):
        selected_fields = fields

    if st.button("Get Answers"):
        if satellite_name and selected_fields:
            with st.spinner("Fetching answers..."):
                results = run_satellite_query(satellite_name, sheet_option, selected_fields)
                save_full_search(satellite_name, sheet_option, selected_fields, results)
        else:
            st.error("Please enter satellite name and select at least one query.")
