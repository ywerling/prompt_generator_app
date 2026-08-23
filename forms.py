from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import prompt_parameters
import person_parameters


class GenericForm(FlaskForm):
    subject = StringField("Subject")  # , validators=[DataRequired()])
    background = StringField("Background")
    style = SelectField("Style", choices=prompt_parameters.STYLE_LIST)
    art_type = SelectField("Art Type", choices=prompt_parameters.ART_TYPE_LIST)
    camera_angle = SelectField("Camera Angle", choices=prompt_parameters.CAMERA_ANGLE_LIST)
    lighting = SelectField("Lighting", choices=prompt_parameters.LIGHTING_LIST)
    color_palette = SelectField("Color Palette", choices=prompt_parameters.COLOR_PALETTE_LIST)
    color_vibe = SelectField("Color Vibe", choices=prompt_parameters.COLOR_VIBES_LIST)
    composition = SelectField("Composition", choices=prompt_parameters.COMPOSITIONS_LIST)
    special_effect = SelectField("Special Effect", choices=prompt_parameters.SPECIAL_EFFECTS_LIST)
    miscellaneous = SelectField("Miscellaneous", choices=prompt_parameters.MISCELLANEOUS_LIST)

    submit = SubmitField("Create Prompt")


class LandscapeForm(FlaskForm):
    description = StringField("Landscape Description")

    # Dropdown menus for various landscape characteristics
    season = SelectField("Season", choices=prompt_parameters.SEASONS_LIST)
    time_of_day = SelectField("Time of Day", choices=prompt_parameters.TIME_OF_DAY_LIST)
    weather = SelectField("Weather", choices=prompt_parameters.WEATHER_LIST)
    terrain = SelectField("Terrain", choices=prompt_parameters.TERRAIN_LIST)
    mood = SelectField("Mood", choices=prompt_parameters.MOOD_LIST)

    submit = SubmitField("Create Prompt")


class CharacterForm(FlaskForm):
    activity_detail = StringField("Activity Detail")
    background = StringField("Background")

    # Dropdown menus for various landscape characteristics
    gender = SelectField("Gender", choices=person_parameters.GENDER_LIST)
    scene = SelectField("Scene", choices=person_parameters.SCENES_LIST)
    race = SelectField("Race", choices=person_parameters.RACES_LIST)
    hair_color = SelectField("Hair Color", choices=person_parameters.COLORS_LIST)
    body_type = SelectField("Body Type", choices=person_parameters.BODY_TYPES_LIST)
    body_pose = SelectField("Body Pose", choices=person_parameters.POSES_LIST)
    skin = SelectField("Skin", choices=person_parameters.SKIN_LIST)
    hair_type = SelectField("Hair Type", choices=person_parameters.HAIR_TYPES_LIST)
    clothing_material = SelectField("Clothing Material", choices=person_parameters.CLOTHING_MATERIAL_LIST)
    clothing_color = SelectField("Clothing Color", choices=person_parameters.COLORS_LIST)
    clothing_type = SelectField("Clothing Type", choices=person_parameters.CLOTHING_TYPE_LIST)
    tool = SelectField("Tool", choices=person_parameters.TOOLS_LIST)
    tool_action = SelectField("Tool Action", choices=person_parameters.TOOL_ACTIONS_LIST)
    activity = SelectField("Activity", choices=person_parameters.ACTIVITY_LIST)

    submit = SubmitField("Create Prompt")
