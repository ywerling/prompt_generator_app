STYLE_KEYWORDS = {
    "photorealistic": "photorealistic, hyperrealistic, 8k, DSLR, sharp focus",
    "digital_art": "digital art, artstation, trending, vibrant colours",
    "oil_painting": "oil painting, impasto, textured canvas, classical",
    "watercolor": "watercolour, soft edges, wet-on-wet, pastel tones",
    "anime": "anime style, manga, cel shading, clean lines",
    "concept_art": "concept art, cinematic, detailed environment, matte painting",
    "pixel_art": "pixel art, 16-bit, retro game style",
    "3d_render": "3D render, octane render, subsurface scattering, ray tracing",
}

LIGHTING_KEYWORDS = {
    "golden_hour": "golden hour lighting, warm tones, long shadows",
    "neon": "neon glow, cyberpunk lighting, colourful reflections",
    "studio": "studio lighting, softbox, professional photography",
    "dramatic": "dramatic lighting, chiaroscuro, deep shadows, high contrast",
    "soft": "soft diffused lighting, overcast, gentle shadows",
    "volumetric": "volumetric lighting, god rays, atmospheric haze",
}

PLATFORM_SUFFIXES = {
    "midjourney": "--ar {ratio} --v 6 --style raw",
    "dalle": "",
    "stable_diffusion": ", masterpiece, best quality",
    "firefly": "",
    "leonardo": ", ultra detailed, high quality",
}


def build_prompt(idea, platform, style, lighting, ratio, keywords):
    parts = [idea]
    if style in STYLE_KEYWORDS:
        parts.append(STYLE_KEYWORDS[style])
    if lighting in LIGHTING_KEYWORDS:
        parts.append(LIGHTING_KEYWORDS[lighting])
    if keywords:
        parts.append(keywords)
    result = ", ".join(part for part in parts if part)
    suffix = PLATFORM_SUFFIXES.get(platform, "")
    if suffix:
        result += " " + suffix.replace("{ratio}", ratio)
    return result
