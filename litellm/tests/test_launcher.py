import importlib.machinery
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


LAUNCHER = Path(__file__).parents[1] / "rootfs/usr/local/bin/litellm-addon"


def load_launcher():
    loader = importlib.machinery.SourceFileLoader("litellm_addon", str(LAUNCHER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.launcher = load_launcher()

    def test_default_config_has_compose_model_routes(self):
        config = self.launcher.build_config(
            {
                "enable_prometheus": True,
                "enable_file_guardrail": True,
                "log_level": "info",
            }
        )
        aliases = {item["model_name"] for item in config["model_list"]}
        self.assertEqual(
            aliases,
            {
                "claude-haiku-4-5-20251001",
                "claude-sonnet-4-6",
                "claude-opus-4-8",
            },
        )
        self.assertIn("prometheus", config["litellm_settings"]["callbacks"])
        self.assertIn("guardrails", config)
        self.assertFalse(config["general_settings"]["store_model_in_db"])

    def test_external_services_are_only_enabled_when_configured(self):
        config = self.launcher.build_config(
            {
                "database_url": "postgresql://example/litellm",
                "redis_url": "redis://example/0",
                "searxng_api_base": "http://example:8080",
                "nvidia_api_key": "secret",
                "enable_prometheus": False,
                "enable_file_guardrail": False,
                "log_level": "debug",
            }
        )
        self.assertTrue(config["general_settings"]["store_model_in_db"])
        self.assertTrue(config["litellm_settings"]["cache"])
        self.assertIn("search_tools", config)
        self.assertNotIn("guardrails", config)
        self.assertEqual(len(config["model_list"]), 4)
        self.assertNotIn("prometheus", config["litellm_settings"]["callbacks"])

    def test_custom_config_cannot_escape_config_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            config_dir = Path(directory) / "config"
            config_dir.mkdir()
            outside = Path(directory) / "outside.yaml"
            outside.write_text("model_list: []\n", encoding="utf-8")
            self.launcher.CONFIG_DIR = config_dir
            with self.assertRaisesRegex(ValueError, "must remain inside"):
                self.launcher.resolve_custom_config("../outside.yaml")

    def test_salt_key_is_stable_and_private(self):
        with tempfile.TemporaryDirectory() as directory:
            self.launcher.DATA_DIR = Path(directory)
            self.launcher.SALT_KEY_PATH = Path(directory) / "salt_key"
            first = self.launcher.get_salt_key()
            second = self.launcher.get_salt_key()
            self.assertEqual(first, second)
            self.assertTrue(first.startswith("sk-salt-"))
            self.assertEqual(
                self.launcher.SALT_KEY_PATH.stat().st_mode & 0o777,
                0o600,
            )


if __name__ == "__main__":
    unittest.main()
