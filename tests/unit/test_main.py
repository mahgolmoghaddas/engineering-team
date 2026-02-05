import importlib
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

import engineering_team.main as main


@contextmanager
def temp_cwd():
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            yield Path(temp_dir)
        finally:
            os.chdir(original_cwd)


class MainModuleUnitTests(unittest.TestCase):
    def test_requirements_describes_account_system(self):
        self.assertIn("account management system", main.requirements)

    def test_module_and_class_names(self):
        self.assertEqual(main.module_name, "accounts.py")
        self.assertEqual(main.class_name, "Account")

    def test_run_invokes_kickoff_with_inputs(self):
        with patch.object(main, "EngineeringTeam") as mock_team:
            instance = mock_team.return_value
            crew = instance.crew.return_value
            crew.kickoff = MagicMock()

            main.run()

            mock_team.assert_called_once()
            crew.kickoff.assert_called_once()
            inputs = crew.kickoff.call_args.kwargs["inputs"]
            self.assertEqual(inputs["module_name"], main.module_name)
            self.assertEqual(inputs["class_name"], main.class_name)
            self.assertEqual(inputs["requirements"], main.requirements)

    def test_import_creates_output_directory(self):
        with temp_cwd() as temp_dir:
            if "engineering_team.main" in importlib.sys.modules:
                importlib.sys.modules.pop("engineering_team.main")
            importlib.import_module("engineering_team.main")
            self.assertTrue((temp_dir / "output").exists())


if __name__ == "__main__":
    unittest.main()
