import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from engineering_team.tools.write_file import WriteFileInput, WriteFileTool


@contextmanager
def temp_cwd():
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            yield Path(temp_dir)
        finally:
            os.chdir(original_cwd)


class WriteFileToolUnitTests(unittest.TestCase):
    def setUp(self):
        self.tool = WriteFileTool()

    def test_write_file_input_round_trip(self):
        payload = WriteFileInput(path="output/frontend/app.js", content="console.log('hi')")
        self.assertEqual(payload.path, "output/frontend/app.js")
        self.assertEqual(payload.content, "console.log('hi')")

    def test_write_file_tool_metadata(self):
        self.assertEqual(self.tool.name, "write_file")
        self.assertIn("output/frontend", self.tool.description)
        self.assertIs(self.tool.args_schema, WriteFileInput)

    def test_rejects_absolute_path(self):
        with self.assertRaises(ValueError):
            self.tool._run("/output/frontend/app.js", "content")

    def test_rejects_home_path(self):
        with self.assertRaises(ValueError):
            self.tool._run("~/output/frontend/app.js", "content")

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            self.tool._run("output/frontend/../app.js", "content")

    def test_rejects_missing_prefix(self):
        with self.assertRaises(ValueError):
            self.tool._run("output/other/app.js", "content")

    def test_writes_file_successfully(self):
        with temp_cwd() as temp_dir:
            result = self.tool._run("output/frontend/app.js", "content")
            self.assertEqual(result, "Wrote output/frontend/app.js")
            self.assertTrue((temp_dir / "output/frontend/app.js").exists())


if __name__ == "__main__":
    unittest.main()
