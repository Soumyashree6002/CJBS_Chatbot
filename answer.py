def format_answer(field_name, answer, source_url=None, trust_level="primary"):
    if answer == "Data not available":
        note = "⚠️ Data not available."
    else:
        # Append trust disclaimer if needed
        if trust_level == "secondary":
            note = "⚠️ Source is from a secondary website. Please verify."
        elif trust_level == "tertiary":
            note = "⚠️ Source is not from a trusted domain. Use with caution."
        else:
            note = ""

    formatted = f"**{field_name}:** {answer}"
    if source_url:
        formatted += f"\n\n🔗 [Source]({source_url})"
    if note:
        formatted += f"\n\n{note}"
    return formatted
