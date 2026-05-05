import unittest
from typing import *
from proj2 import Row, Node, parse_row, read_csv_lines, listlen, filter_rows

class TestParsing(unittest.TestCase):
   
    def test_parse_row_full(self):
        row = parse_row([
            "USA",
            "1990",
            "100.0",
            "1.5",
            "200.0",
            "2.5",
            "300.0",
            "3.5"
        ])

        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 1990)
        self.assertEqual(row.energy_co2_emissions, 200.0)

    def test_parse_row_missing_values(self):
        row = parse_row([
            "Canada",
            "2000",
            "",
            "",
            "",
            "",
            "",
            ""
        ])

        self.assertEqual(row.country, "Canada")
        self.assertEqual(row.year, 2000)
        self.assertIsNone(row.energy_co2_emissions)
        self.assertIsNone(row.total_co2_emissions_excluding_lucf_per_capita)

class TestCSV(unittest.TestCase):

    def test_read_csv_returns_node_or_none(self):
        result = read_csv_lines("some-ghg-emissions.csv")
        self.assertTrue(result is None or isinstance(result, Node))

    def test_csv_length_matches_listlen(self):
        head = read_csv_lines("some-ghg-emissions.csv")
        if head is not None:
            self.assertEqual(listlen(head), self._manual_count(head))

    def _manual_count(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        return 1 + self._manual_count(node.next)

class TestListLen(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(listlen(None), 0)
    
    def test_simple_chain(self):
        r1 = Row("X", 2000, None, None, None, None, None, None)
        r2 = Row("Y", 2001, None, None, None, None, None, None)
        lst = Node(r1, Node(r2, None))
        self.assertEqual(listlen(lst), 2)

class TestFilterRows(unittest.TestCase):

    def make_list(self):
        r1 = Row("USA", 2000, 10, 1, 20, 2, 30, 3)
        r2 = Row("Canada", 2001, 20, 2, 40, 4, 20, 3)
        r3 = Row("Mexico", 2002, 40, 3, 80, 8, 10, 7)
        
        return Node(r1, Node(r2, Node(r3, None)))
    
    def test_filter_country_equal(self):
        data = self.make_list()
        
        result = filter_rows(data, "country", "equal", "USA")

        self.assertIsNotNone(result)
        self.assertEqual(result.value.country, "USA")
        self.assertIsNone(result.next)
    
    def test_filter_greater_than(self):
        data = self.make_list()
        
        result = filter_rows(data, "energy_co2_emissions", "greater_than", 30)

        self.assertTrue(result.value.energy_co2_emissions > 30)

    def test_filter_less_than(self):
        data = self.make_list()
        
        result = filter_rows(data, "energy_co2_emissions", "less_than", 10)

        self.assertIsNone(result)
    
    def test_filt_none_values_skipped(self):
        r1 = Row("Mexico", 2000, None, None, None, None, None, None)
        r2 = Row("Canada", 2001, 10, 4, 20, 2, 25, 3)
        data = Node(r1, Node(r2, None))

        result = filter_rows(data, "energy_co2_emissions", "greater_than", 5)
        self.assertEqual(result.value.country, "Canada")

if __name__ == "__main__":
    unittest.main()