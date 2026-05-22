import re

def tool_extract_tv_count(text):
    text_lower = text.lower()
    matches = re.findall(r'(\d+)\s*(?:tv|television)', text_lower)
    if matches:
        return int(matches[0])
    numbers = re.findall(r'\b\d+\b', text_lower)
    if numbers:
        return int(numbers[0])
    return None

def tool_extract_city(address_string):
    parts = [p.strip() for p in address_string.split(",")]
    if len(parts) > 1:
        return parts[-1]
    return "Unknown"