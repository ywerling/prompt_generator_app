LANDSCAPE_DROPDOWNS = [
    {"name": "time_of_day", "label": "Time of day", "options": ["sunrise", "morning", "midday", "afternoon", "evening", "sunset", "night"], "default": "sunrise"},
    {"name": "weather", "label": "Weather", "options": ["clear", "cloudy", "misty", "rainy", "stormy", "snowy"], "default": "clear"},
    {"name": "season", "label": "Season", "options": ["spring", "summer", "autumn", "winter"], "default": "spring"},
]


def default_selections():
    return {item["name"]: item["default"] for item in LANDSCAPE_DROPDOWNS}


def validated_selections(form):
    selections = default_selections()
    for item in LANDSCAPE_DROPDOWNS:
        selected = form.get(item["name"], item["default"])
        if selected in item["options"]:
            selections[item["name"]] = selected
    return selections


def build_landscape_prompt(description, selections):
    return (
        f"{description} Set during {selections['time_of_day']}, with "
        f"{selections['weather']} weather in {selections['season']}. "
        "Expansive landscape composition, rich natural detail, atmospheric depth, and cinematic lighting."
    )
