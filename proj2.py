from __future__ import annotations
import sys
import csv
from dataclasses import dataclass
from typing import *

sys.setrecursionlimit(10_000)

# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]

@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node]

# Then your functions.
def parse_row(fields: list[str]) -> Row:

    def to_float(x: str) -> Optional[float]:
            return float(x) if x != "" else None

    return Row(
        country = fields[0],
        year = int(fields[1]),
        electricity_and_heat_co2_emissions = to_float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita = to_float(fields[3]),
        energy_co2_emissions = to_float(fields[4]),
        energy_co2_emissions_per_capita = to_float(fields[5]),
        total_co2_emissions_excluding_lucf = to_float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita = to_float(fields[7]),
    )

def build_iter(reader) -> Optional[Node]:
        
    try:
        row = next(reader)
        return Node(parse_row(row), build_iter(reader))
    except StopIteration:
        return None

def read_csv_lines(filename: str) -> Optional[Node]:
    
    expected_header = [
        "country",
        "year",
        "electricity_and_heat_co2_emissions",
        "electricity_and_heat_co2_emissions_per_capita",
        "energy_co2_emissions",
        "energy_co2_emissions_per_capita",
        "total_co2_emissions_excluding_lucf",
        "total_co2_emissions_excluding_lucf_per_capita",
    ]

    with open(filename, newline = "") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        if header != expected_header:
            raise ValueError("Invalid CSV header")

        return build_iter(reader)

def listlen(data: Optional[Node]) -> int:
    
    if data is None:
        return 0
    return 1 + listlen(data.next)

def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:

    if data is None:
        return None
    
    rest = filter_rows(data.next, field_name, comparison, value)

    current_value = data.value.__dict__[field_name]

    def matches() -> bool:
        if current_value is None:
            return False
        
        if field_name == "country":
            return comparison == "equal" and str(current_value) == str(value)
        
        try:

            cv = float(current_value)
            v = float(value)

        except:

            return False
        
        if comparison == "less_than":
            return cv < v
        
        elif comparison == "greater_than":
            return cv > v

        elif comparison == "equal":
            return cv == v

        else:
            raise ValueError("Invalid comparison")

    if matches():
        return Node(data.value, rest)
    else:
        return rest