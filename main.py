"""CSC110 Fall 2020: California Fires Entities

This file is created by Azka Azmi, Zaina Azhar, Rachel (Jingxuan) Tang
Date: December 7th, 2020

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. This file was created for the CSC110 final project only.

This file is Copyright (c) 2020 Azka Azmi,
Zaina Azhar and Rachel (Jingxuan) Tang.
"""

from __future__ import annotations
import ctypes
from calculations import Calculations


def prompt() -> int:
    """Run the prompt menu, return the choice selected.
    The loop will not exit until a valid number is entered.

    Preconditions:
        - answer.isnumeric()
    """

    print('#### MENU ####')
    print('1. Average acres burned in California')
    print('2. Acres to annual global temperature')
    print('3. Linear regression of annual global temperature')
    print('4. Average drought levels in California')
    print('5. Drought to acres burned in California')
    print('6. Predict global temperatures')
    print('7. Generate report')
    print('8. END PROGRAM')

    while True:
        answer = input('What would you like to see? ')
        if answer.isnumeric() and 0 < int(answer) < 9:
            return int(answer)
        else:
            print('That is not a valid input or it is not '
                  'on the menu! Please try again :)')


def introduction() -> None:
    """" A function that provides the user with an introduction to the program.
    """
    print('Welcome to Azka, Zaina and Rachel\'s program on Wildfire '
          'Data throughout North America!')
    while True:
        choice = input('Would you like to learn more before you begin? (Y/N)')
        if choice.lower() == 'y':
            print('\nThe aim of this program is to analyze and assess the trends related to')
            print('wildfires that have been unfortunately ravaging across North America')
            print('these past several years.')
            print('\nSpecifically, this program\'s goal is to determine whether there ')
            print('is a relationship between the two products of climate change: ')
            print('rising temperatures and droughts, and the frequency of wildfires.')
            print('In order to do so we\'ll be presenting you with graphical data ')
            print('based on 3 specific data sets. To learn more about these datasets ')
            print('please see the requirements.txt file for this program.')
        elif choice.lower() != 'n':
            print('\nHmmm, it seems like your input is unclear, we\'ll let you try again:')
            continue

        input('\nLet\'s get started, hit enter to begin!')
        break


def run() -> None:
    """Run the main loop. Each time the function is called,
    a menu will appear prompting the user to choose an option to display.
    Call this function individually for each option in the menu (enter 1
    to see option 1, call function again to see option 2, etc)

    """
    introduction()

    # create event object and read necessary files
    a_event = Calculations()
    a_event.read_csv_temp_data('annual_average_temp.csv')
    a_event.read_csv_fire_data('California_Fire_Incidents.csv')
    a_event.read_csv_drought_data('cali_drought.csv')
    choice = prompt()

    if choice == 1:
        a_event.cali_acre_bar_graph()
    elif choice == 2:
        a_event.acres_to_temp()
    elif choice == 3:
        a_event.temp_linear_regression()
    elif choice == 4:
        a_event.cali_drought_bar_graph()
    elif choice == 5:
        a_event.drought_to_acres()
    elif choice == 6:
        a_event.predict_temp()
    elif choice == 7:
        # generate a pop up message
        ctypes.windll.user32.MessageBoxW(0, 'Check file directory for report',
                                         'REPORT Generated', 1)
        a_event.generate_report()
    elif choice == 8:
        print('End of program. Enter: run() again if you\'d like '
              'to use the program for another result!')

    if choice != 8:
        print('Graphical visual has been presented! '
              'Enter: run() again if you\'d like to use the '
              'program again for another result!')


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
        'extra-imports': ['ctypes', 'calculations'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': ['prompt', 'introduction', 'run'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9999']
    })
