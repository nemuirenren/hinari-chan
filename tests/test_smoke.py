"""Smoke tests: compile, wiring, secrets hygiene, no-hardcoded-model ban.

Stdlib unittest only. The model-name ban is enforced without writing the
banned literal: the configured LLM_MODEL value must appear in no tracked
source file.
"""

import compileall
import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
TRACKED_DIRS = ("hinari", "prompts", "tests")


class SmokeTest(unittest.TestCase):
    def test_compiles(self):
        self.assertTrue(compileall.compile_dir(str(ROOT / "hinari"), quiet=1))

    def test_imports(self):
        import hinari.config  # noqa: F401
        import hinari.compat  # noqa: F401
        import hinari.main  # noqa: F401
        import hinari.harness.pipeline  # noqa: F401
        import hinari.harness.state  # noqa: F401
        import hinari.adapters.llm  # noqa: F401
        import hinari.adapters.store  # noqa: F401
        import hinari.adapters.discord_phone  # noqa: F401

    def test_prompts_load(self):
        from hinari.main import load_prompts

        prompts = load_prompts(ROOT / "prompts")
        self.assertTrue(prompts["identity"])
        self.assertTrue(prompts["lore"])
        self.assertTrue(prompts["heart"])
        self.assertIn("update_feelings", prompts["heart"])
        self.assertEqual(len([k for k in prompts["moods"]]), 11)
        self.assertEqual(len(prompts["bands"]), 13)
        self.assertIn("multipliers", prompts["activities"])

    def test_missing_env_fails_clearly(self):
        from hinari import config

        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(config.ConfigError) as ctx:
                config.Config.from_env()
        self.assertIn("LLM_MODEL", str(ctx.exception))

    def test_log_redacts_secrets(self):
        from hinari.main import setup_logging

        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "log.txt"
            setup_logging(log_path, ["SECRET123456789"])
            logging.getLogger("hinari.smoke").info("using SECRET123456789 here")
            logging.shutdown()
            text = log_path.read_text(encoding="utf-8")
        self.assertNotIn("SECRET123456789", text)
        self.assertIn("***", text)

    def test_configured_model_not_hardcoded(self):
        model = os.getenv("LLM_MODEL", "")
        if not model or len(model) < 4:
            self.skipTest("LLM_MODEL not set; nothing to check")
        hits = []
        for dirname in TRACKED_DIRS:
            for path in (ROOT / dirname).rglob("*"):
                if path.is_file() and path.suffix in {".py", ".md", ".json", ".yaml"}:
                    try:
                        if model in path.read_text(encoding="utf-8"):
                            hits.append(str(path.relative_to(ROOT)))
                    except UnicodeDecodeError:
                        continue
        self.assertEqual(hits, [], f"model value hardcoded in: {hits}")


class CurfewTest(unittest.TestCase):
    def test_window_boundaries(self):
        from hinari.main import curfew_active

        self.assertFalse(curfew_active(0))
        self.assertTrue(curfew_active(1))
        self.assertTrue(curfew_active(4))
        self.assertFalse(curfew_active(5))
        self.assertFalse(curfew_active(23))

    def test_window_comes_from_config(self):
        from hinari import config

        self.assertEqual((config.CURFEW_START, config.CURFEW_END), (1, 5))


if __name__ == "__main__":
    unittest.main()
