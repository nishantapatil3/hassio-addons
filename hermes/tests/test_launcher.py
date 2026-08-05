import importlib.machinery
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


LAUNCHER = Path(__file__).parents[1] / "rootfs/usr/local/bin/hermes-addon"
LOADER = importlib.machinery.SourceFileLoader("hermes_addon", str(LAUNCHER))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LauncherTests(unittest.TestCase):
    def test_maps_options_and_supervisor_token(self):
        options = {
            "openrouter_api_key": "sk-or-test",
            "hass_url": "http://supervisor/core",
            "api_server_enabled": True,
            "api_server_key": "api-secret",
            "dashboard_enabled": True,
            "dashboard_username": "admin",
            "dashboard_password": "dashboard-secret",
            "gateway_allow_all_users": False,
        }
        with patch.dict(
            MODULE.os.environ,
            {"SUPERVISOR_TOKEN": "supervisor-secret"},
            clear=True,
        ):
            MODULE.set_option_environment(options)

            self.assertEqual(MODULE.os.environ["OPENROUTER_API_KEY"], "sk-or-test")
            self.assertEqual(
                MODULE.os.environ["HASS_TOKEN"], "supervisor-secret"
            )
            self.assertEqual(MODULE.os.environ["API_SERVER_HOST"], "0.0.0.0")
            self.assertEqual(
                MODULE.os.environ["HERMES_DASHBOARD_BASIC_AUTH_USERNAME"], "admin"
            )
            self.assertEqual(MODULE.os.environ["GATEWAY_ALLOW_ALL_USERS"], "false")

    def test_explicit_home_assistant_token_wins(self):
        with patch.dict(
            MODULE.os.environ,
            {"SUPERVISOR_TOKEN": "supervisor-secret"},
            clear=True,
        ):
            MODULE.set_option_environment(
                {"hass_token": "long-lived-token", "hass_url": "http://ha:8123"}
            )

            self.assertEqual(MODULE.os.environ["HASS_TOKEN"], "long-lived-token")
            self.assertEqual(MODULE.os.environ["HASS_URL"], "http://ha:8123")

    def test_api_server_requires_a_key(self):
        with self.assertRaisesRegex(ValueError, "api_server_key"):
            MODULE.set_option_environment(
                {"api_server_enabled": True, "api_server_key": "short"}
            )

    def test_dashboard_requires_credentials(self):
        with self.assertRaisesRegex(ValueError, "dashboard_username"):
            MODULE.set_option_environment({"dashboard_enabled": True})

    def test_load_options(self):
        with tempfile.TemporaryDirectory() as directory:
            options_file = Path(directory) / "options.json"
            options_file.write_text(
                json.dumps({"openrouter_api_key": "sk-or-test"}),
                encoding="utf-8",
            )
            with patch.object(MODULE, "OPTIONS_FILE", options_file):
                self.assertEqual(
                    MODULE.load_options(), {"openrouter_api_key": "sk-or-test"}
                )


if __name__ == "__main__":
    unittest.main()
