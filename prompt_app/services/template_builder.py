import re


PLACEHOLDER_PATTERN = re.compile(r"\{([A-Za-z][A-Za-z0-9_]*)\}")


def parse_template(template):
    """Return display segments and unique placeholder names for a template."""
    segments = []
    placeholders = []
    cursor = 0
    for match in PLACEHOLDER_PATTERN.finditer(template):
        if match.start() > cursor:
            segments.append(("text", template[cursor:match.start()]))
        name = match.group(1)
        segments.append(("field", name))
        if name not in placeholders:
            placeholders.append(name)
        cursor = match.end()
    if cursor < len(template):
        segments.append(("text", template[cursor:]))
    return segments, placeholders


def build_template_prompt(template, values):
    """Replace placeholders and normalize whitespace in the completed prompt."""
    def replacement(match):
        return values.get(match.group(1), "").strip()

    return " ".join(PLACEHOLDER_PATTERN.sub(replacement, template).split())
