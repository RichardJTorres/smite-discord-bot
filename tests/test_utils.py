import json
import os
from unittest import TestCase

from smite_bot.utils import parse_motd


class TestUtils(TestCase):
    def test_parse_motd(self):
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, "data/motd.json")) as f:
            motds = f.read()

        motds = json.loads(motds)
        parsed = parse_motd(motds[0].get("description"))

        expected = {
            "description": "The battle of Ragnarok is here and all the gods are gathered in Asgard. Bring your favorite god to this fight at the end of the world. ",
            "Map": " Assault",
            "Starting Cooldown Reduction": "40%",
            "Maximum Cooldown Reduction": " 80%",
            "Gods": "All",
            "Selection": "All Pick (2 bans each team)",
        }

        self.assertEqual(parsed, expected)
