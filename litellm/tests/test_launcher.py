import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml


LAUNCHER = Path(__file__).parents[1] / "rootfs/usr/local/bin/litellm-addon"
BUNDLED_CONFIG = Path(__file__).parents[1] / "rootfs/etc/litellm-addon/litellm.yaml"
ADDON_CONFIG = Path(__file__).parents[1] / "config.yaml"


def load_launcher():
    loader = importlib.machinery.SourceFileLoader("litellm_addon", str(LAUNCHER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.launcher = load_launcher()

    def test_default_config_is_valid_yaml_with_required_sections(self):
        config = yaml.safe_load(BUNDLED_CONFIG.read_text(encoding="utf-8"))
        aliases = {item["model_name"] for item in config["model_list"]}
        self.assertEqual(
            aliases,
            {"claude-haiku-4-5-20251001", "claude-sonnet-4-6", "claude-opus-4-8"},
        )
        self.assertIn("prometheus", config["litellm_settings"]["callbacks"])
        self.assertIn("guardrails", config)
        self.assertIn("master_key", config["general_settings"])

    def test_addon_config_directory_is_mounted_writable(self):
        config = yaml.safe_load(ADDON_CONFIG.read_text(encoding="utf-8"))
        self.assertIn(
            {"type": "addon_config", "read_only": False},
            config["map"],
        )

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
