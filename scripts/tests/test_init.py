import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]


class InitManifestTests(unittest.TestCase):
    def test_lite_profile_discovers_sources_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            command = [sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", tmp, "--profile", "lite"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "engineering-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["modules"][0]["source_paths"], ["backend"])
            self.assertFalse(next(doc for doc in data["documents"] if doc["id"] == "DB")["required"])
            again = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(again.returncode, 2)

    def test_output_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", tmp, "--output", "../manifest.json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
