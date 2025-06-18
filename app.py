import streamlit as st
from google_search import search_with_trust
from gemini_interface import ask_gemini
from answer import format_answer
from context import FIELD_CONTEXTS, FIELD_QUERY_OVERRIDES
from utils import (
    map_user_category,
    map_purpose_category,
    map_sdg_category,
    clean_answer_text,
    get_all_sheet1_fields,
    get_all_sheet2_fields,
    extract_sdg_numbers
)

# Sidebar selection
st.set_page_config(page_title="Satellite Data Chatbot", layout="wide")
sheet_option = st.sidebar.selectbox("Select which sheet to query:", ["data tab (Sheet1)", "gpt data tab (Sheet2)"])

# Query field options
if sheet_option == "data tab (Sheet1)":
    fields = get_all_sheet1_fields()
else:
    fields = get_all_sheet2_fields()

# Satellite name input
satellite_name = st.text_input("Enter Satellite Name")

# Query field selection
selected_fields = st.multiselect(
    "Select specific queries:",
    options=fields,
    default=[]
)

if st.checkbox("Select all queries"):
    selected_fields = fields

# Trigger the search
search_clicked = st.button("Get Answers")
if search_clicked and satellite_name and selected_fields:
    with st.spinner("Fetching answers..."):
        for field in selected_fields:
            field_lower = field.lower()
            extra_context = ""
            query_template = FIELD_QUERY_OVERRIDES.get(field_lower, "{satellite} {field}")
            query = query_template.format(satellite=satellite_name, field=field)

            raw_snippet, source_url, trust_level = search_with_trust(query)

            if not raw_snippet:
                raw_snippet = "Data not available"
                source_url = None

            # Add Gemini context if available for the field
            for key in FIELD_CONTEXTS:
                if key in field_lower:
                    extra_context = FIELD_CONTEXTS[key]
                    break

            answer = ask_gemini(satellite_name, field, raw_snippet, source_url, extra_context)
            print(f"🔍 Gemini raw answer for {satellite_name} - {field}: {answer}")
            answer = clean_answer_text(answer)

            if answer.lower() == "data not available" and trust_level != "tertiary":
                raw_snippet, source_url, trust_level = search_with_trust(query, try_open_search=True)
                if raw_snippet:
                    answer = ask_gemini(satellite_name, field, raw_snippet, source_url, extra_context)
                    print(f"🔁 Gemini fallback answer for {satellite_name} - {field}: {answer}")
                    answer = clean_answer_text(answer)

            # Special logic for Sheet2 fields
            if sheet_option == "gpt data tab (Sheet2)":

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

            formatted = format_answer(field, answer, source_url, trust_level)
            st.markdown(formatted)
            st.markdown("---")

elif search_clicked:
        st.error("Please enter satellite name and select at least one query.")
