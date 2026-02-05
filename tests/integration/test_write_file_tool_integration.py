import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from engineering_team.tools.write_file import WriteFileTool


@contextmanager
def temp_cwd():
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            yield Path(temp_dir)
        finally:
            os.chdir(original_cwd)


class WriteFileToolIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tool = WriteFileTool()

    def test_writes_file_in_frontend_directory(self):
        with temp_cwd() as temp_dir:
            self.tool._run("output/frontend/app/index.js", "console.log('ok')")
            target = temp_dir / "output/frontend/app/index.js"
            self.assertTrue(target.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), "console.log('ok')")

    def test_creates_nested_directories(self):
        with temp_cwd() as temp_dir:
            self.tool._run("output/frontend/components/ui/button.js", "export {}")
            target_dir = temp_dir / "output/frontend/components/ui"
            self.assertTrue(target_dir.is_dir())

    def test_overwrites_existing_file(self):
        with temp_cwd() as temp_dir:
            path = "output/frontend/app.js"
            self.tool._run(path, "first")
            self.tool._run(path, "second")
            target = temp_dir / path
            self.assertEqual(target.read_text(encoding="utf-8"), "second")

    def test_handles_unicode_content(self):
        with temp_cwd() as temp_dir:
            content = "こんにちは世界"
            self.tool._run("output/frontend/i18n.js", content)
            target = temp_dir / "output/frontend/i18n.js"
            self.assertEqual(target.read_text(encoding="utf-8"), content)

    def test_output_frontend_directory_exists_after_write(self):
        with temp_cwd() as temp_dir:
            self.tool._run("output/frontend/app.js", "content")
            self.assertTrue((temp_dir / "output/frontend").exists())


if __name__ == "__main__":
    unittest.main()
