"""CSC110 Fall 2020: California Fires Entities

This file is created by Azka Azmi, Zaina Azhar, Rachel (Jingxuan) Tang
Date: December 7th, 2020

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. This file was created for the CSC110 final project only.

This file is Copyright (c) 2020 Azka Azmi,
Zaina Azhar and Rachel (Jingxuan) Tang.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CaliFires:
    """California Wild Fires and their information.

    Instance Attributes:
      - name: the name given to the fire
      - year: the archive year of the fire
      - acres: total acres burned
      - active: whether the fire is still active in 2019
      - injuries: the number of people who were injured in the incident

    Representation Invariants:
      - self.name != ''
      - 2013 <= self.year <= 2019
      - self.acres >= 0
      - self.injuries >= 0
    """

    name: str
    year: int
    acres: int
    active: bool
    injuries: int


@dataclass
class Temp:
    """The annual rise in temperature in celsius

    Instance Attributes:
      - year: the year
      - temp: the temperature change of that year in celsius

    Representation Invariants:
      - 1880 <= self.year <= 2019
    """

    year: int
    temp: float


@dataclass
class Drought:
    """The annual drought levels in California (represented by percentage)

    Instance Attributes:
      - year: the year
      - d0: abnormally dry (in percentage)
      - d1: moderate drought
      - d2: severe drought
      - d3: extreme drought
      - d4: exceptional drought

    Representation Invariants:
      - 2000 <= self.year <= 2020
    """

    year: int
    d0: float
    d1: float
    d2: float
    d3: float
    d4: float


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    # python TA
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': [],
        # the names (strs) of functions that call print/open/input
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9999']
    })
