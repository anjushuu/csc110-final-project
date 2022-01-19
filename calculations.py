"""CSC110 Fall 2020: California Fires Entities

This file is created by Azka Azmi, Zaina Azhar, Rachel (Jingxuan) Tang
Date: December 7th, 2020

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. This file was created for the CSC110 final project only.

This file is Copyright (c) 2020 Azka Azmi,
Zaina Azhar and Rachel (Jingxuan) Tang.
"""

from __future__ import annotations

import csv

# graph stuffs
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from entities import CaliFires, Temp, Drought
from fire_system import FireSystem


class Calculations:
    """Class that holds all the functions used to display
    data.
    """
    # Private Instance Attributes:
    #   - system: used to store a FireSystem

    _system: FireSystem

    def __init__(self) -> None:
        """Initialize an empty system
        """
        self._system = FireSystem()

    def read_csv_fire_data(self, filepath: str) -> None:
        """Create cali fire objects from the data mapped from a CSV file.
        To ensure the csv file is readable, save the file as UTF 8 csv

        Preconditions:
            - filepath refers to a csv file in the format of
              California_Fire_Incidents.csv
        """
        total_fires = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0}
        with open(filepath, encoding="utf8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                name = row[25]
                if row[0] != '':
                    acres = int(row[0])
                else:
                    acres = 0

                if row[20] != '':
                    injuries = int(row[20])
                else:
                    injuries = 0

                if row[1].lower() == 'true':
                    active = True
                else:
                    active = False

                year = int(row[4])
                total_fires[year] += 1
                fire = CaliFires(name, year, acres, active, injuries)

                self._system.add_cali_fire(fire)

    def read_csv_temp_data(self, filepath: str) -> None:
        """Create temperature objects from the data mapped from a CSV file.
        To ensure the csv file is readable, save the file as UTF 8 csv

        Preconditions:
            - filepath refers to a csv file in the format of
              annual_average_temp.csv
        """

        with open(filepath, encoding="utf8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                year = int(row[0])
                temp = float(row[1])
                temp_obj = Temp(year, temp)

                self._system.add_temp(temp_obj)

    def read_csv_drought_data(self, filepath: str) -> None:
        """Create drought objects from the data mapped from a CSV file.
        To ensure the csv file is readable, save the file as UTF 8 csv

        Preconditions:
            - filepath refers to a csv file in the format of
              cali_drought.csv
        """

        with open(filepath, encoding="utf8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                year = int(row[0][6:])
                d4 = float(row[1])
                d3 = float(row[2])
                d2 = float(row[3])
                d1 = float(row[4])
                d0 = float(row[5])
                drought = Drought(year, d0, d1, d2, d3, d4)

                self._system.add_drought(drought)

    def cali_acre_bar_graph(self) -> None:
        """Display a bar graph displaying total acres burned
        per year in California from 2013 to 2019

        Preconditions:
            - self._system != ''
        """

        # x axis
        # I know from the dataset the years are 2013-2019
        years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

        # y axis
        # get the corresponding acres value by indexing the dictionary
        x = self._system.get_acres()
        acres = [x[2013], x[2014], x[2015], x[2016], x[2017], x[2018], x[2019]]

        # plot graph
        plt.bar(years, acres, color=(0.2, 0.4, 0.8, 0.8))

        # Add some text for labels, title and custom x-axis tick labels, etc.
        plt.ylabel('Acres Burned')
        plt.title('Total Acres Burned in California')
        plt.xlabel('Years')

        # display graph
        plt.show()

    def acres_to_temp(self) -> None:
        """Display a graph using plotly to see if there's a relation between global rises
        in temperature and the acres burned in california

        From the graph, there appears to be no correlation between rising temperatures
        and acres burned.

        Preconditions:
            - self._system != ''
        """
        # Create a blank figure
        fig = go.Figure()

        # y coordinates
        y = self._system.get_acres()
        acres = [y[2013], y[2014], y[2015], y[2016], y[2017], y[2018], y[2019]]
        # x coordinates
        x = self._system.get_temp()
        temp = [x[2013], x[2014], x[2015], x[2016], x[2017], x[2018], x[2019]]

        # Add the raw data
        fig.add_trace(go.Scatter(x=temp, y=acres,
                                 mode='markers',
                                 name='Relation Between Acres Burned and Rise in Temperature'))

        fig.update_layout(title='Relation Between Acres Burned and Rise in Temperature',
                          xaxis_title='Changes in Temperature',
                          yaxis_title='Acres Burned')

        # Display the figure in a web browser.
        fig.show()

    def temp_linear_regression(self) -> None:
        """Display a linear regression graph comparing the change in global
        temperature through the years 1880 to 2019 using sklearn

        Preconditions:
            - self._system != ''
        """
        # blank graph
        plt.clf()
        # y coordinates
        year = np.array(self._system.get_temp_year())
        # x coordinates
        temp = np.array(self._system.get_temp_temp())

        # reshaping to 2D array
        year = year.reshape(-1, 1)
        temp = temp.reshape(-1, 1)

        # Create linear regression object
        regr = linear_model.LinearRegression()
        regr.fit(year, temp)

        # plot the graph
        plt.scatter(year, temp, color='black')
        # Make predictions
        temp_predict = regr.predict(year)

        # regression line
        plt.plot(year, temp_predict, color='blue', linewidth=1)

        # labels
        plt.xlabel('Years')
        plt.ylabel('Changes in global temperature')
        plt.title('Changes in Global Temperature from 1880 to 2019')
        plt.xticks(np.arange(1880, 2020, 15))
        plt.yticks(np.arange(-1.0, 1.25, 0.25))

        plt.show()

    def cali_drought_bar_graph(self) -> None:
        """Display a stacked bar graph comparing the level of drought
        in California through the years 2000 to 2020 using matplotlib

        The percentages add up past 100% as regions could have
        overlapping drought levels

        Preconditions:
            - self._system != ''
        """

        info = self._system.get_droughts()

        # y data sets
        # uses insert instead of append because the dictionary
        # starts at year 2020 but the graph must start at year 2000
        d0, d1, d2, d3, d4 = [], [], [], [], []
        for year in info:
            d0.insert(0, info[year][0][0] / info[year][1])
            d1.insert(0, info[year][0][1] / info[year][1])
            d2.insert(0, info[year][0][2] / info[year][1])
            d3.insert(0, info[year][0][3] / info[year][1])
            d4.insert(0, info[year][0][4] / info[year][1])

        ind = np.arange(21)  # the x locations for the groups
        width = 0.50  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, d0, width)
        p2 = plt.bar(ind, d1, width, bottom=d0)
        p3 = plt.bar(ind, d2, width, bottom=d1)
        p4 = plt.bar(ind, d3, width, bottom=d2)
        p5 = plt.bar(ind, d4, width, bottom=d3)

        plt.ylabel('Percentage')
        plt.xlabel('Years 2000 - 2020')
        plt.title('Drought Levels in California')
        plt.xticks(ind, list(range(00, 21)))
        plt.yticks(np.arange(0, 201, 10))
        plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('d0', 'd1',
                                                         'd2', 'd3',
                                                         'd4'))

        plt.show()

    def drought_to_acres(self) -> None:
        """Plot relations between drought levels and acres burned in California
        from 2013-2019 using plotly

        Preconditions:
            - self._system != ''
        """

        years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019']
        # get the corresponding acres value by indexing the dictionary
        x = self._system.get_acres()
        acres = [x[2013], x[2014], x[2015], x[2016], x[2017], x[2018], x[2019]]

        info = self._system.get_droughts()

        # line 1, 2, 3, 4, 5
        d0, d1, d2, d3, d4 = [], [], [], [], []
        for year in info:
            d0.insert(0, info[year][0][0] / info[year][1])
            d1.insert(0, info[year][0][1] / info[year][1])
            d2.insert(0, info[year][0][2] / info[year][1])
            d3.insert(0, info[year][0][3] / info[year][1])
            d4.insert(0, info[year][0][4] / info[year][1])

        fig = make_subplots(rows=3, cols=2)
        fig.add_trace(go.Scatter(x=years, y=acres,
                                 mode='lines+markers',
                                 name='acres burned'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=years, y=d0[13:-1],
                                 mode='lines+markers',
                                 name='d0'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=years, y=d1[13:-1],
                                 mode='lines+markers',
                                 name='d1'),
                      row=3, col=1)
        fig.add_trace(go.Scatter(x=years, y=d2[13:-1],
                                 mode='lines+markers',
                                 name='d2'),
                      row=1, col=2)
        fig.add_trace(go.Scatter(x=years, y=d3[13:-1],
                                 mode='lines+markers',
                                 name='d3'),
                      row=2, col=2)
        fig.add_trace(go.Scatter(x=years, y=d4[13:-1],
                                 mode='lines+markers',
                                 name='d4'),
                      row=3, col=2)

        fig.update_layout(title='Relation Between Acres Burned and Drought in California',
                          xaxis_title='Years')
        fig.show()

    def predict_temp(self) -> None:
        """Predict future changes in temperature globally based on the linear
        regression line generated before. Equation taken from assignment 1

        A linear graph is generated from the years 2020-2040
        Preconditions:
            - self._system != ''
        """

        # x coordinates
        x_values = self._system.get_temp_year()
        # y coordinates
        y_values = self._system.get_temp_temp()
        average_x = sum(x_values) / 140  # the data consists of 140 years
        average_y = sum(y_values) / 140

        # calculate a and b value using equation from A1
        b_topx = [(x_i - average_x) for x_i in x_values]  # all the values of (xi - x_average)
        b_topy = [(y_i - average_y) for y_i in y_values]  # all the values of (y1 - y_average)
        b_top = sum([b_topx[i] * b_topy[i] for i in range(len(b_topx))])
        b_bottom = sum([(x_i - average_x) ** 2 for x_i in x_values])
        b = b_top / b_bottom
        a = average_y - (b * average_x)

        # generate y values using (a,b)
        new_y = []
        for x in range(2020, 2041):
            new_y.append(a + b * x)

        # plot a line graph in plotly
        fig = go.Figure()

        # Add the raw data
        fig.add_trace(go.Scatter(x=list(range(2020, 2041)), y=new_y,
                                 mode='lines+markers', name='Temperature Prediction'))

        fig.update_layout(title='Temperature Prediction For the Next 20 Years',
                          xaxis_title='Years',
                          yaxis_title='Changes in Temperature')

        # Display the figure in a web browser.
        fig.show()

    def generate_report(self) -> None:
        """Generate a text file in the file directory analyzing the results
        of all the calculations performed on all the collected data sets.
        """

        # write a new file
        f = open("REPORT.txt", "w")
        f.write('###   REPORT   ###  \n')
        f.write('Analysis of Data: \n')

        data = ['1. There seems to be no correlation between '
                'acres burned and rises in annual temperature \n',
                '2. There seems to be a correlation between '
                'rising amounts of acres burned \n and an increase '
                'of areas in drought/with abnormally dry climate. '
                'This correlation \n suggests dry climate and droughts '
                'increase the frequency and intensity of wildfires. \n'
                '3. Scientists claim that climate change has made '
                'areas of typically \n dry climate become drier, and '
                'similarly areas of wet climate have become wetter. \n',
                '4. From the graphs, it\'s apparent that in 2018, '
                'there was a sudden spike in acres burned, \n most likely '
                'influenced by both increasing dryness '
                'and external incident. \n'
                '5. Any active fires in California currently: '
                + str(self._system.show_active_fires())
                ]
        for i in data:
            f.write(i)
        f.close()


if __name__ == '__main__':
    import python_ta

    import doctest

    doctest.testmod()

    # python TA
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['numpy', 'plotly', 'matplotlib',
                          'sklearn', 'csv'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': ['generate_report',
                       'read_csv_fire_data',
                       'read_csv_drought_data',
                       'read_csv_temp_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200',
                    'E9999', 'E9998']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
