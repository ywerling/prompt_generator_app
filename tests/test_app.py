import unittest
from unittest.mock import patch

from prompt_app import create_app
from prompt_app.services.landscape_builder import build_landscape_prompt
from prompt_app.services.prompt_builder import build_prompt
from prompt_app.services.generic_builder import build_generic_prompt
from prompt_app.services.template_builder import build_template_prompt, parse_template


class AppRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.client = self.app.test_client()

    def test_get_routes_render(self):
        for path in ("/", "/prompt", "/generic", "/landscape", "/prompt_generator", "/character", "/template", "/scrape"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_prompt_generator_preserves_choices_and_builds_result(self):
        response = self.client.post(
            "/prompt_generator",
            data={
                "idea": "A glass city",
                "platform": "midjourney",
                "style": "concept_art",
                "lighting": "neon",
                "ratio": "16:9",
                "keywords": "rain",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A glass city", response.data)
        self.assertIn(b'value="16:9" selected', response.data)

    def test_landscape_post_builds_result(self):
        response = self.client.post(
            "/landscape",
            data={
                "description": "A quiet valley.",
                "time_of_day": "sunset",
                "weather": "misty",
                "season": "autumn",
                "action": "generate",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A quiet valley.", response.data)
        self.assertIn(b"misty weather", response.data)

    def test_generic_generator_builds_result(self):
        response = self.client.post(
            "/generic",
            data={
                "subject": "A clockwork owl",
                "background": "ancient library",
                "style": "Surrealism",
                "art_type": "concept art",
                "camera_angle": "close-up",
                "lighting": "candlelight",
                "color_palette": "-----",
                "color_vibe": "-----",
                "composition": "Rule of Thirds",
                "special_effect": "-----",
                "miscellaneous": "8K",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A clockwork owl, ancient library, Surrealism", response.data)
        self.assertNotIn(b"A clockwork owl, ancient library, -----", response.data)

    def test_template_generator_builds_result(self):
        response = self.client.post(
            "/template",
            data={
                "template": "draw a {PERSON} in the style of {ARTIST}",
                "value_PERSON": "violinist",
                "value_ARTIST": "Van Gogh",
                "action": "generate",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"draw a violinist in the style of Van Gogh", response.data)

    @patch("prompt_app.routes.generators.save_prompt")
    def test_template_generator_saves_result(self, save_prompt_mock):
        response = self.client.post(
            "/template",
            data={
                "template": "draw a {PERSON}",
                "value_PERSON": "violinist",
                "generated_prompt": "draw a violinist",
                "action": "save",
            },
        )
        self.assertEqual(response.status_code, 200)
        save_prompt_mock.assert_called_once_with(
            "Template prompt: draw a violinist", "draw a violinist"
        )
        self.assertIn(b"Prompt saved to the database", response.data)


class ServiceTestCase(unittest.TestCase):
    def test_generic_builder_omits_empty_choices(self):
        result = build_generic_prompt(
            {"subject": "Dragon", "background": "", "style": "-----", "lighting": "moonlight"}
        )
        self.assertEqual(result, "Dragon, moonlight")

    def test_prompt_builder(self):
        result = build_prompt("Forest", "midjourney", "anime", "soft", "4:3", "moss")
        self.assertIn("anime style", result)
        self.assertIn("--ar 4:3", result)

    def test_landscape_builder(self):
        result = build_landscape_prompt(
            "Coast.",
            {"time_of_day": "night", "weather": "stormy", "season": "winter"},
        )
        self.assertIn("stormy weather in winter", result)

    def test_template_builder(self):
        segments, placeholders = parse_template("A {SUBJECT} beside {SUBJECT} in {PLACE}")
        self.assertEqual(placeholders, ["SUBJECT", "PLACE"])
        self.assertEqual(
            build_template_prompt(
                "A {SUBJECT} in {PLACE}", {"SUBJECT": "  fox ", "PLACE": "a forest"}
            ),
            "A fox in a forest",
        )


if __name__ == "__main__":
    unittest.main()
