"""CSC110 Fall 2020: California Fires Entities

This file is created by Azka Azmi, Zaina Azhar, Rachel (Jingxuan) Tang
Date: December 7th, 2020

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. This file was created for the CSC110 final project only.

This file is Copyright (c) 2020 Azka Azmi,
Zaina Azhar and Rachel (Jingxuan) Tang.
"""

from __future__ import annotations
from typing import List, Dict
from entities import CaliFires, Temp, Drought


class FireSystem:
    """A system that maintains all entities (fire, drought, temp).

    Representation Invariants:
        - self.name != ''
        - self.year != ''
    """
    # Private Instance Attributes:
    #   - _cali_fires: a list of california fire objects
    #   - _rising_temps: a list of temp objects as a tuple like (year, temp)
    #   - _cali_droughts: a list of drought objects

    _cali_fires: List[CaliFires]
    _rising_temps: List[Temp]
    _cali_droughts: List[Drought]

    def __init__(self) -> None:
        """Initialize a new fire system.

        The system starts with no entities.
        """
        self._cali_fires = []
        self._rising_temps = []
        self._cali_droughts = []

    def add_cali_fire(self, fire: CaliFires) -> None:
        """Add the provided fire object to the fire system
        """
        self._cali_fires.append(fire)

    def add_temp(self, temp: Temp) -> None:
        """Add the provided temperature object to the fire system
        """
        self._rising_temps.append(temp)

    def add_drought(self, drought: Drought) -> None:
        """Add the provided drought object to the fire system
        """
        self._cali_droughts.append(drought)

    def get_acres(self) -> Dict[int, int]:
        """Returns a dict mapping year to acres burned of each fire
        object in the system (california)
        """
        dictionary = {}
        for i in self._cali_fires:
            if i.year not in dictionary:
                dictionary[i.year] = i.acres
            else:
                dictionary[i.year] = dictionary[i.year] + i.acres
        return dictionary

    def get_temp_year(self) -> List[int]:
        """Returns a list of all the years in each temp object
        """
        return [x.year for x in self._rising_temps]

    def get_temp_temp(self) -> List[float]:
        """Returns a list of all the changes in temperature in each
        temp object
        """
        return [x.temp for x in self._rising_temps]

    def get_temp(self) -> Dict[int, float]:
        """Return a dict mapping of year to changes in global
        temperature
        """
        return {x.year: x.temp for x in self._rising_temps}

    def get_droughts(self) -> Dict[int, List[float]]:
        """Returns a dict mapping year to drought levels of each drought
        object in the system
        """
        dictionary = {}
        for i in self._cali_droughts:
            if i.year not in dictionary:
                dictionary[i.year] = [[i.d0, i.d1, i.d2, i.d3, i.d4], 0]
            else:
                dictionary[i.year][0][0] = dictionary[i.year][0][0] + i.d0
                dictionary[i.year][0][1] = dictionary[i.year][0][1] + i.d1
                dictionary[i.year][0][2] = dictionary[i.year][0][2] + i.d2
                dictionary[i.year][0][3] = dictionary[i.year][0][3] + i.d3
                dictionary[i.year][0][4] = dictionary[i.year][0][4] + i.d4
                dictionary[i.year][1] = dictionary[i.year][1] + 1
        return dictionary

    def show_active_fires(self) -> List[str]:
        """Returns a dict mapping of the name of the california
        fire if it's still active in 2019
        Returns an empty list if none are active
        """
        return [x.name for x in self._cali_fires if x.active]


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
        'extra-imports': ['typing', 'entities'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9999']
    })
