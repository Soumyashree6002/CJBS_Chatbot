import json
import os

HISTORY_FILE = "search_history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_full_search(satellite, sheet_option, selected_fields, results):
    history = load_history()
    sheet_label = "Sheet1" if "Sheet1" in sheet_option else "Sheet2"
    new_entry = {
        "satellite": satellite.strip(),
        "sheet": sheet_label,
        "fields": selected_fields,
        "results": results
    }
    history.append(new_entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_history_strings():
    history = load_history()
    return [f"{entry['satellite']} | {entry['sheet']}" for entry in history]

def get_history_entry(index_from_top=0):
    history = load_history()
    if index_from_top < len(history):
        return history[::-1][index_from_top]  # newest first
    return None

def clear_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def delete_history_entry(index_from_top):
    history = load_history()
    index_in_list = len(history) - 1 - index_from_top  # because we reverse history in UI
    if 0 <= index_in_list < len(history):
        del history[index_in_list]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
