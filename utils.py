import prompt_parameters
import person_parameters


def process_generic_form_data(form_data):
    # Process form data from the request and return the necessary information
    subject = form_data.get("subject")
    background = form_data.get("background")
    style = form_data.get("style")
    art_type = form_data.get("art_type")
    camera_angle = form_data.get("camera_angle")
    lighting = form_data.get("lighting")
    color_palette = form_data.get("color_palette")
    color_vibe = form_data.get("color_vibe")
    composition = form_data.get("composition")
    special_effect = form_data.get("special_effect")
    miscellaneous = form_data.get("miscellaneous")

    prompt = ""

    if len(subject) > 0:
        prompt += subject
        prompt += ", "

    if len(background) > 0:
        prompt += background
        prompt += ", "

    if style != prompt_parameters.NONE_STRING:
        prompt += style
        prompt += ", "

    if art_type != prompt_parameters.NONE_STRING:
        prompt += art_type
        prompt += ", "

    if camera_angle != prompt_parameters.NONE_STRING:
        prompt += camera_angle
        prompt += ", "

    if lighting != prompt_parameters.NONE_STRING:
        prompt += lighting
        prompt += ", "

    if color_palette != prompt_parameters.NONE_STRING:
        prompt += color_palette
        prompt += ", "

    if color_vibe != prompt_parameters.NONE_STRING:
        prompt += color_vibe
        prompt += ", "

    if composition != prompt_parameters.NONE_STRING:
        prompt += composition
        prompt += ", "

    if special_effect != prompt_parameters.NONE_STRING:
        prompt += special_effect
        prompt += ", "

    if miscellaneous != prompt_parameters.NONE_STRING:
        prompt += miscellaneous
        prompt += ", "

    prompt = simplify_string(prompt)

    return prompt

    # Continue processing all necessary fields
    # Return the processed data as needed
    # return {
    #     'subject': subject,
    #     'background': background,
    #     'style': style,
    #     # Add more fields here
    # }


def process_landscape_form_data(form_data):
    # Process form data from the request and return the necessary information
    description = form_data.get("description")
    season = form_data.get("season")
    time_of_day = form_data.get("time_of_day")
    weather = form_data.get("weather")
    terrain = form_data.get("terrain")
    mood = form_data.get("mood")

    prompt = ""

    if len(description) > 0:
        prompt += description
        prompt += ", "

    if season != prompt_parameters.NONE_STRING:
        prompt += season
        prompt += ", "

    if time_of_day != prompt_parameters.NONE_STRING:
        prompt += time_of_day
        prompt += ", "

    if weather != prompt_parameters.NONE_STRING:
        prompt += weather
        prompt += ", "

    if terrain != prompt_parameters.NONE_STRING:
        prompt += terrain
        prompt += ", "

    if mood != prompt_parameters.NONE_STRING:
        prompt += mood
        prompt += ", "

    prompt = simplify_string(prompt)

    return prompt


def process_character_form_data(form_data):
    # Process form data from the request and return the necessary information
    # subject = form_data.get("subject")

    gender = form_data.get("gender")
    scene = form_data.get("scene")
    race = form_data.get("race")
    hair_color = form_data.get("hair_color")
    body_type = form_data.get("body_type")
    body_pose  = form_data.get("body_pose")
    skin = form_data.get("skin")
    hair_type = form_data.get("hair_type")
    clothing_material = form_data.get("clothing_material")
    clothing_color = form_data.get("clothing_color")
    clothing_type = form_data.get("clothing_type")
    tool = form_data.get("tool")
    tool_action = form_data.get("tool_action")
    activity = form_data.get("activity")
    activity_detail = form_data.get("activity_detail")
    background = form_data.get("background")


    generated_prompt = ""

    if scene != prompt_parameters.NONE_STRING:
        generated_prompt += scene
        generated_prompt += " scene, "

    if gender != prompt_parameters.NONE_STRING:
        generated_prompt += gender
        generated_prompt += " "

    if race != prompt_parameters.NONE_STRING:
        generated_prompt += race
        generated_prompt += " "

    if body_type != prompt_parameters.NONE_STRING:
        generated_prompt += body_type
        generated_prompt += ", "

    if skin != prompt_parameters.NONE_STRING:
        generated_prompt += skin
        generated_prompt += " skin, "

    if hair_color != prompt_parameters.NONE_STRING:
        generated_prompt += hair_color
        generated_prompt += " "

    if hair_type != prompt_parameters.NONE_STRING:
        generated_prompt += hair_type
        generated_prompt += " hair, "

    if clothing_color != prompt_parameters.NONE_STRING:
        generated_prompt += clothing_color
        generated_prompt += " "

    if clothing_material != prompt_parameters.NONE_STRING:
        generated_prompt += clothing_material
        generated_prompt += " "

    if clothing_type != prompt_parameters.NONE_STRING:
        generated_prompt += clothing_type
        generated_prompt += ", "

    if body_pose != prompt_parameters.NONE_STRING:
        generated_prompt += body_pose
        generated_prompt += " pose, "

    if tool_action != prompt_parameters.NONE_STRING:
        generated_prompt += tool_action
        generated_prompt += " "

    if tool != prompt_parameters.NONE_STRING:
        generated_prompt += "a "
        generated_prompt += tool
        generated_prompt += ", "

    if activity != prompt_parameters.NONE_STRING:
        generated_prompt += activity
        generated_prompt += " "

    if len(activity_detail) > 1:
        generated_prompt += activity_detail
        generated_prompt += ", "

    if len(background) > 1:
        generated_prompt += "the background consists of "
        generated_prompt += background
        generated_prompt += ", "

    # add some generic elements to the prompt often used in portrait images to increase the probability of a quality
    # image
    generated_prompt += person_parameters.COMMON_PROMPT_ENDING
    # print(f"Prompt: {generated_prompt}")

    return generated_prompt


def simplify_string(input_string):
    # remove unnecessary characters from the prompt, initially the trailing spaces
    # can be expanded for other beautification effect
    output_string = input_string.rstrip(' ,')
    return output_string
