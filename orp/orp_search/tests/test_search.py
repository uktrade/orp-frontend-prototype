import unittest

from unittest.mock import MagicMock, call, patch

from orp_search.utils.search import create_search_query


class TestCreateSearchQuery(unittest.TestCase):

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_single_word_query(self, mock_search_query):
        result = create_search_query("test")
        mock_search_query.assert_called_with("test", search_type="plain")
        self.assertEqual(result, mock_search_query.return_value)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_implicit_and_search_operator_query(self, mock_search_query):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2]

        # Call the function
        _ = create_search_query("test trial")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__and__.assert_called_once_with(mock_query2)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_multiple_implicit_and_search_operator_query(
        self, mock_search_query
    ):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")
        mock_query3 = MagicMock(name="MockQuery3")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2, mock_query3]

        # Call the function
        _ = create_search_query("test trial error")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
            call("error", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__and__.assert_called_with(mock_query3)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_and_search_operator_query(self, mock_search_query):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2]

        # Call the function
        _ = create_search_query("test AND trial")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__and__.assert_called_once_with(mock_query2)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_multiple_and_search_operator_query(self, mock_search_query):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")
        mock_query3 = MagicMock(name="MockQuery3")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2, mock_query3]

        # Call the function
        _ = create_search_query("test AND trial AND error")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
            call("error", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__and__.assert_called_with(mock_query3)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_or_search_operator_query(self, mock_search_query):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2]

        # Call the function
        _ = create_search_query("test OR trial")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__or__.assert_called_once_with(mock_query2)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_multiple_or_search_operator_query(self, mock_search_query):
        # Mock SearchQuery instances
        mock_query1 = MagicMock(name="MockQuery1")
        mock_query2 = MagicMock(name="MockQuery2")
        mock_query3 = MagicMock(name="MockQuery3")

        # Configure the mock to return mock objects
        mock_search_query.side_effect = [mock_query1, mock_query2, mock_query3]

        # Call the function
        _ = create_search_query("test OR trial OR error")

        # Assert that SearchQuery was called with expected arguments
        calls = [
            call("test", search_type="plain"),
            call("trial", search_type="plain"),
            call("error", search_type="plain"),
        ]
        mock_search_query.assert_has_calls(calls, any_order=False)

        # Assert the AND operation was applied
        mock_query1.__or__.assert_called_with(mock_query3)

    @patch("orp_search.utils.search.SearchQuery", autospec=True)
    def test_phrase_search_query(self, mock_search_query):
        result = create_search_query('"test trial"')
        mock_search_query.assert_called_with(
            "test trial", search_type="phrase"
        )
        self.assertEqual(result, mock_search_query.return_value)


if __name__ == "__main__":
    unittest.main()
