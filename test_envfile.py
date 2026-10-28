import unittest

from envfile import blank_count, blank_keys, changed_keys, emit_env, filled_count, filled_keys, key_count, only_left, only_right, overlay_env, parse_env, shared_keys, without_keys, shared_count


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
        self.assertEqual(only_right(before, after), ["ROLE"])
        self.assertEqual(blank_keys({"NAME": "Ada", "EMPTY": ""}), ["EMPTY"])
        self.assertEqual(filled_keys({"NAME": "Ada", "EMPTY": ""}), ["NAME"])
        self.assertEqual(key_count({"NAME": "Ada", "EMPTY": ""}), 2)
        self.assertEqual(blank_count({"NAME": "Ada", "EMPTY": ""}), 1)
        self.assertEqual(filled_count({"NAME": "Ada", "EMPTY": ""}), 1)
        self.assertEqual(before["CITY"], "North")

    def test_reject_bad_key(self) -> None:
        with self.assertRaises(ValueError):
            parse_env("BAD KEY=1\n")


        self.assertEqual(shared_count({"A": "1"}, {"A": "2", "B": "3"}), 1)

if __name__ == "__main__":
    unittest.main()
