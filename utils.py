# utils.py (updated to apply mappings)

from questions import user_category_map, purpose_category_map, sdg_category_number_map, sdg_number_to_category
import re

def extract_sdg_numbers(text):
    return list(map(int, re.findall(r'\b\d+\b', text)))

def map_user_category(user_text):
    key = user_text.strip().title()
    number = user_category_map.get(key, None)
    return key, number

def map_purpose_category(purpose_text):
    key = purpose_text.strip().title()
    number = purpose_category_map.get(key, None)
    return key, number

def map_sdg_category(sdg_numbers_list):
    """
    Takes a list of SDG numbers like [9], [1, 8], etc., and returns the category (Innovation, Economic, etc.)
    """
    categories = set()
    for sdg in sdg_numbers_list:
        category = sdg_number_to_category.get(sdg)
        if category:
            categories.add(category)

    if not categories:
        return None, None

    # Assuming only one category is chosen, pick most likely (sorted by priority if needed)
    category = list(categories)[0]
    number = list(sdg_category_number_map.values())[list(sdg_category_number_map.keys()).index(category)]
    return category, number

def clean_answer_text(text):
    return text.strip()

def get_all_sheet2_fields():
    from questions import sheet2_fields
    return sheet2_fields

def get_all_sheet1_fields():
    from questions import sheet1_fields
    return sheet1_fields
