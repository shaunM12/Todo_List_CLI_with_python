import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import main


class TodoCliTests(unittest.TestCase):
    def setUp(self):
        self._orig_tasks = list(main.tasks)
        self._orig_todo_file = main.TODO_FILE
        main.tasks.clear()

    def tearDown(self):
        main.tasks.clear()
        main.tasks.extend(self._orig_tasks)
        main.TODO_FILE = self._orig_todo_file

    def test_add_task_rejects_empty_title(self):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            created = main.add_one_task("   ")

        self.assertFalse(created)
        self.assertIn("Task title cannot be empty.", output.getvalue())
        self.assertEqual(main.tasks, [])

    def test_add_task_accepts_and_strips_title(self):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            created = main.add_one_task("  Buy milk  ")

        self.assertTrue(created)
        self.assertEqual(main.tasks, ["Buy milk"])
        self.assertIn('Added task: "Buy milk"', output.getvalue())

    def test_delete_task_validation_and_success(self):
        main.tasks.extend(["One", "Two"])

        with patch("sys.stdout", new_callable=io.StringIO) as output:
            ok_text = main.delete_task("abc")
            ok_range = main.delete_task("10")
            ok_delete = main.delete_task("1")

        self.assertFalse(ok_text)
        self.assertFalse(ok_range)
        self.assertTrue(ok_delete)
        self.assertEqual(main.tasks, ["Two"])
        printed = output.getvalue()
        self.assertIn("Please enter a valid task number.", printed)
        self.assertIn("Task number not found.", printed)
        self.assertIn('Deleted task: "One"', printed)

    def test_save_and_load_roundtrip(self):
        with TemporaryDirectory() as tmp_dir:
            main.TODO_FILE = Path(tmp_dir) / "todos.csv"
            main.tasks.extend(["A", "B"])
            main.save_todos()
            main.tasks.clear()

            main.load_todos()

        self.assertEqual(main.tasks, ["A", "B"])

    def test_main_flow_add_list_delete_and_quit(self):
        # Sequence: add task, list, delete first task, quit.
        user_inputs = iter(["1", "Learn tests", "2", "3", "1", "4"])

        with TemporaryDirectory() as tmp_dir:
            main.TODO_FILE = Path(tmp_dir) / "todos.csv"
            with patch("builtins.input", side_effect=lambda _: next(user_inputs)):
                with patch("sys.stdout", new_callable=io.StringIO) as output:
                    main.main()

            printed = output.getvalue()
            self.assertIn("Todo List CLI", printed)
            self.assertIn('Added task: "Learn tests"', printed)
            self.assertIn("1. Learn tests", printed)
            self.assertIn('Deleted task: "Learn tests"', printed)
            self.assertIn("Todos saved. Goodbye!", printed)


if __name__ == "__main__":
    unittest.main()
