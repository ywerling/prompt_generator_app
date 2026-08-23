import prompt_parameters


GENERIC_FIELDS = (
    "subject",
    "background",
    "style",
    "art_type",
    "camera_angle",
    "lighting",
    "color_palette",
    "color_vibe",
    "composition",
    "special_effect",
    "miscellaneous",
)


def build_generic_prompt(form_data):
    """Build a comma-separated prompt from validated generic form values."""
    values = []
    for field_name in GENERIC_FIELDS:
        value = (form_data.get(field_name) or "").strip()
        if value and value != prompt_parameters.NONE_STRING:
            values.append(value)
    return ", ".join(values)
