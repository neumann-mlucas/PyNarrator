import unittest

from model.dialog import DialogNode, DialogOption, LoadDialogs


class TestDialogModel(unittest.TestCase):
    def setUp(self):
        # Setup test data or mocks here if needed
        pass

    def test_parse_option(self):
        test_option = {"label": "test_label", "text": "Test option text."}
        option = LoadDialogs.parse_option(test_option)
        self.assertIsInstance(option, DialogOption)
        self.assertEqual(option.label, "test_label")
        self.assertEqual(option.text, "Test option text.")

    def test_parse_dialog_valid_data(self):
        # Define a test dialog dictionary with valid data
        test_dialog_data = {
            "label": "dialog",
            "text": "This is a dialog.",
            "image": "image.png",
            "option1": {"label": "option1", "text": "Option 1 text."},
            "option2": {"label": "option2", "text": "Option 2 text."},
        }

        # Call the parse_dialog function with the test data
        result_dialog = LoadDialogs.parse_dialog(test_dialog_data)

        # Assert that the result is an instance of DialogNode
        self.assertIsInstance(result_dialog, DialogNode)

        # Assert that the label, text, and image attributes are correctly set
        self.assertEqual(result_dialog.label, "dialog")
        self.assertEqual(result_dialog.text, "This is a dialog.")
        self.assertEqual(result_dialog.image, "image.png")

        # Assert that the options are correctly parsed into DialogOption instances
        self.assertEqual(len(result_dialog.options), 2)
        self.assertTrue(
            all(isinstance(option, DialogOption) for option in result_dialog.options)
        )
        self.assertEqual(result_dialog.options[0].label, "option1")
        self.assertEqual(result_dialog.options[1].label, "option2")

    def test_parse_dialog_missing_required_fields(self):
        # Define a test dialog dictionary missing required fields
        test_dialog_data_incomplete = {
            # Missing 'label', 'text', 'image'
            "option1": {"label": "option1", "text": "Option 1 text."}
        }

        # Use assertRaises to check that parsing incomplete data returns None or raises an error
        result_dialog = LoadDialogs.parse_dialog(test_dialog_data_incomplete)
        self.assertIsNone(
            result_dialog, "Expected parse_dialog to return None for incomplete data."
        )

    def test_parse_option_valid_data(self):
        test_option_data = {"label": "option1", "text": "This is an option."}
        result_option = LoadDialogs.parse_option(test_option_data)

        self.assertIsInstance(result_option, DialogOption)
        self.assertEqual(result_option.label, "option1")
        self.assertEqual(result_option.text, "This is an option.")

    def test_parse_option_missing_keys(self):
        test_option_data_incomplete = {
            "label": "option2"
            # Missing 'text' key
        }

        with self.assertRaises(KeyError):
            LoadDialogs.parse_option(test_option_data_incomplete)

    def test_validate_dialogs_valid_dialog(self):
        dialog_map = {
            "start": DialogNode(
                "start",
                "Start Dialog",
                "start.png",
                [DialogOption("end", "End Dialog")],
            ),
            "end": DialogNode(
                "start",
                "End Dialog",
                "end.png",
                [DialogOption("start", "Start Dialog")],
            ),
        }

        self.assertIsNone(LoadDialogs.validate_dialogs(dialog_map))

    def test_validate_dialogs_invalid_dialog(self):
        dialog_map = {
            "start": DialogNode(
                "start",
                "Start Dialog",
                "start.png",
                [DialogOption("end", "End Dialog")],
            ),
        }

        with self.assertRaises(Exception):
            LoadDialogs.validate_dialogs(dialog_map)


if __name__ == "__main__":
    unittest.main()
