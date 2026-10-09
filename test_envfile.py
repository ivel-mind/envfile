import unittest

from envfile import changed_keys, emit_env, only_left, overlay_env, parse_env, shared_keys, without_keys


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

    def test_changed_keys(self) -> None:
        before = {"NAME": "Ada", "CITY": "North"}
        after = {"NAME": "Ada", "CITY": "South", "ROLE": "dev"}
        self.assertEqual(changed_keys(before, after), ["CITY", "ROLE"])
        self.assertEqual(without_keys(before, ["CITY"]), {"NAME": "Ada"})
        self.assertEqual(shared_keys(before, after), ["NAME", "CITY"])
        self.assertEqual(only_left(before, {"NAME": "Ada"}), ["CITY"])
        self.assertEqual(before["CITY"], "North")

    def test_reject_bad_key(self) -> None:
        with self.assertRaises(ValueError):
            parse_env("BAD KEY=1\n")


if __name__ == "__main__":
    unittest.main()
