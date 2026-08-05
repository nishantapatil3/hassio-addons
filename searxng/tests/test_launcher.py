import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


LAUNCHER = Path(__file__).parents[1] / "rootfs/usr/local/bin/searxng-addon"
LOADER = importlib.machinery.SourceFileLoader("searxng_addon", str(LAUNCHER))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LauncherTest(unittest.TestCase):
    def test_configures_upstream_environment_and_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            options_file = Path(temporary) / "options.json"
            cache_dir = Path(temporary) / "cache"
            options_file.write_text(
                json.dumps(
                    {
                        "base_url": "https://search.example/",
                        "image_proxy": False,
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(MODULE, "OPTIONS_FILE", options_file), patch.object(
                MODULE, "CACHE_DIR", cache_dir
            ), patch.dict(os.environ, {}, clear=True):
                MODULE.configure_environment(MODULE.load_options())
                self.assertEqual(
                    os.environ["SEARXNG_BASE_URL"], "https://search.example/"
                )
                self.assertEqual(os.environ["SEARXNG_IMAGE_PROXY"], "false")
            self.assertTrue(cache_dir.is_dir())

    def test_rejects_empty_base_url(self):
        with self.assertRaises(ValueError):
            MODULE.configure_environment({"base_url": ""})


if __name__ == "__main__":
    unittest.main()
