import unittest

from envfile import emit_env, overlay_env, parse_env


class EnvfileTest(unittest.TestCase):
    def test_roundtrip_comments_and_export(self) -> None:
        text = "# comment\nexport NAME=Ada\nEMPTY=\nTITLE=\"a b\"\n"
        got = parse_env(text)
        self.assertEqual(got, {"NAME": "Ada", "EMPTY": "", "TITLE": "a b"})
        again = parse_env(emit_env(got))
        self.assertEqual(again, got)

    def test_overlay(self) -> None:
        base = {"NAME": "Ada", "CITY": "North"}
        got = overlay_env(base, {"CITY": "South"})
        self.assertEqual(got, {"NAME": "Ada", "CITY": "South"})
        self.assertEqual(base["CITY"], "North")

    def test_reject_bad_key(self) -> None:
        with self.assertRaises(ValueError):
            parse_env("BAD KEY=1\n")


if __name__ == "__main__":
    unittest.main()
