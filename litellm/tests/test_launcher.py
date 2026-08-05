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
        self.assertEqual(
            config["general_settings"]["database_url"],
            "os.environ/DATABASE_URL",
        )
        self.assertTrue(config["litellm_settings"]["cache"])
        self.assertEqual(
            config["litellm_settings"]["cache_params"]["url"],
            "os.environ/REDIS_URL",
        )
        for model in config["model_list"]:
            self.assertEqual(
                model["litellm_params"]["api_key"],
                "os.environ/OPENROUTER_API_KEY",
            )

    def test_addon_config_directory_is_mounted_writable(self):
        config = yaml.safe_load(ADDON_CONFIG.read_text(encoding="utf-8"))
        self.assertIn(
            {"type": "addon_config", "read_only": False},
            config["map"],
        )
        self.assertEqual(
            config["options"]["database_url"],
            "postgresql://postgres:homeassistant@db21ed7f-postgres:5432/litellm",
        )
        self.assertEqual(
            config["options"]["redis_url"],
            "redis://db21ed7f-redis:6379/0",
        )
        self.assertEqual(config["schema"]["database_url"], "str")
        self.assertEqual(config["schema"]["redis_url"], "str")

    def test_legacy_openrouter_placeholders_are_migrated(self):
        with tempfile.TemporaryDirectory() as directory:
            config_file = Path(directory) / "litellm.yaml"
            config_file.write_text(
                "model_list:\n"
                "  - litellm_params:\n"
                "      api_key: sk-your-openrouter-api-key\n"
                "  - litellm_params:\n"
                "      api_key: sk-user-custom-key\n",
                encoding="utf-8",
            )
            self.launcher.CONFIG_FILE = config_file

            self.assertEqual(self.launcher.migrate_legacy_config(), 1)
            migrated = config_file.read_text(encoding="utf-8")
            self.assertIn("api_key: os.environ/OPENROUTER_API_KEY", migrated)
            self.assertIn("api_key: sk-user-custom-key", migrated)
            self.assertEqual(self.launcher.migrate_legacy_config(), 0)

    def test_bundled_database_url_is_migrated_to_ui_option(self):
        with tempfile.TemporaryDirectory() as directory:
            config_file = Path(directory) / "litellm.yaml"
            config_file.write_text(
                "general_settings:\n"
                "  database_url: "
                "postgresql://postgres:homeassistant@db21ed7f-postgres-latest:5432/litellm\n",
                encoding="utf-8",
            )
            self.launcher.CONFIG_FILE = config_file

            self.assertEqual(self.launcher.migrate_legacy_config(), 1)
            self.assertIn(
                "database_url: os.environ/DATABASE_URL",
                config_file.read_text(encoding="utf-8"),
            )

    def test_legacy_redis_cache_is_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            config_file = Path(directory) / "litellm.yaml"
            config_file.write_text(
                "  # To enable Redis response caching, uncomment and fill in your Redis URL:\n"
                "  # cache: true\n"
                "  # cache_params:\n"
                "  #   type: redis\n"
                "  #   url: redis://:password@192.168.1.10:6379/0\n"
                "  #   namespace: litellm-cache\n"
                "  #   ttl: 600\n",
                encoding="utf-8",
            )
            self.launcher.CONFIG_FILE = config_file

            self.assertEqual(self.launcher.migrate_legacy_config(), 1)
            migrated = config_file.read_text(encoding="utf-8")
            self.assertIn("url: os.environ/REDIS_URL", migrated)
            self.assertNotIn("192.168.1.10", migrated)

    def test_database_url_option_is_exported(self):
        original_options_file = self.launcher.OPTIONS_FILE
        original_data_dir = self.launcher.DATA_DIR
        original_salt_key_path = self.launcher.SALT_KEY_PATH
        original_database_url = self.launcher.os.environ.get("DATABASE_URL")
        original_redis_url = self.launcher.os.environ.get("REDIS_URL")
        try:
            with tempfile.TemporaryDirectory() as directory:
                directory_path = Path(directory)
                options_file = directory_path / "options.json"
                options_file.write_text(
                    '{"database_url": "postgresql://db.example/litellm", '
                    '"redis_url": "redis://redis.example:6379/0"}',
                    encoding="utf-8",
                )
                self.launcher.OPTIONS_FILE = options_file
                self.launcher.DATA_DIR = directory_path / "data"
                self.launcher.SALT_KEY_PATH = self.launcher.DATA_DIR / "salt_key"

                self.launcher.configure_environment()

                self.assertEqual(
                    self.launcher.os.environ["DATABASE_URL"],
                    "postgresql://db.example/litellm",
                )
                self.assertEqual(
                    self.launcher.os.environ["REDIS_URL"],
                    "redis://redis.example:6379/0",
                )
        finally:
            self.launcher.OPTIONS_FILE = original_options_file
            self.launcher.DATA_DIR = original_data_dir
            self.launcher.SALT_KEY_PATH = original_salt_key_path
            if original_database_url is None:
                self.launcher.os.environ.pop("DATABASE_URL", None)
            else:
                self.launcher.os.environ["DATABASE_URL"] = original_database_url
            if original_redis_url is None:
                self.launcher.os.environ.pop("REDIS_URL", None)
            else:
                self.launcher.os.environ["REDIS_URL"] = original_redis_url

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
