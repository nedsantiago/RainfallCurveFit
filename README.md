<div align="center" style="height:250px;margin: auto;">
  <img src="./docs/icons/logo_altblock.svg"><br>
</div>

# Alternating Block Method for Stochastic Rainfall
![GitHub Actions Build Status](https://github.com/nedsantiago/altblock_stochastic/actions/workflows/python-app.yml/badge.svg)


## Purpose
This script aims to reduce the time spent converting Rainfall-Intensity Duration Frequency Curves (RIDF) into usable rainfall data for Hydrologic and Hydraulic Simulations.

## Project Author
* Ned Santiago, started on November 28, 2022

## Usage
Change directory to the source directory
```
cd ./src/
```

Run main.py
```
py ./main.py
```

Select a csv file with the following format, where each value uses mm/hr as its units:
|     | 10    | 20    | 30    | 60    | 120  | 180  | 360  | 720  | 1440 |
|-----|-------|-------|-------|-------|------|------|------|------|------|
| 2   | 123.9 | 96.1  | 81.3  | 55.8  | 37.5 | 28.6 | 18.0 | 11.0 | 6.3  |
| 5   | 171.9 | 132.5 | 111.8 | 76.0  | 51.8 | 40.2 | 25.9 | 16.1 | 9.5  |
| 10  | 203.7 | 156.5 | 131.9 | 89.4  | 61.3 | 47.9 | 31.1 | 19.5 | 11.5 |
| 20  | 234.2 | 179.6 | 151.2 | 102.3 | 70.4 | 55.3 | 36.1 | 22.7 | 13.5 |
| 25  | 243.8 | 186.9 | 157.4 | 106.4 | 73.3 | 57.6 | 37.7 | 23.7 | 14.1 |
| 50  | 273.6 | 209.5 | 176.3 | 118.9 | 82.2 | 64.8 | 42.5 | 26.9 | 16.0 |
| 100 | 303.2 | 231.9 | 195.0 | 131.4 | 91.0 | 72.0 | 47.4 | 30.0 | 17.9 |

Select where to save the result


## Components
* Data Handler
    * DirectoryHandler - retrieves the file paths and stores for use
* Rainfall Calculator
    * rainfall curve fit function
    * Ridf - an ridf object that holds the rainfal-intensity duration table
    * AlterBlock - rearranges the time series data into an alternating block result
* curve fit
    * CurveFitter - the calculator for curve fitting
* visualize results
    * Grapher - graphs and produces figures


## Future Updates
- [x] Github integration
- [x] Pytest integration
- [x] Singleton data handler, separate data handler and path taker
- [x] Provide a GUI to the DataRetriever object
- [ ] Make a small website to act as an improved GUI implementation
- [ ] Create a test for each class
- [ ] Organize classes into clearly defined python files
- [x] Logging file that shows the process of the calculation, important for debugging the software
- [x] Use class handlers.RotatingFileHandler in log file to also force log file size limit
- [ ] Change Ridf class
    - [x] Ridf should enforce that durations should be in minutes format, always increasing from left to right
    - [ ] Maybe enforce that it should be an intensity scale i.e. mm/hr per return-period-duration and not mm per return-period-duration
    - [x] Ridf should act more like a dataframe with functionality to check data validity. Thus, need to inherit pd.Dataframe
    - [ ] Ridf can have an abstract method so that it can be built on by another class
- [x] Change CurveFitter class
    - [x] CurveFitter should immediately start curve fitting after receiving the path to the data -> CurveFitter runs the curve fit algorithm after receiving a dataframe
    - [x] Optimize the CurveFitter code, many variables were not used or not needed (e.g. some column and index length variables)
    - [x] CurveFitter curvefit method should only work on one row of data, another method should be responsible for compiling to table -> this is already the functionality of scipy curve_fit
    - [x] CurveFitter curvefit method should work with any formula or varying variable counts of formulas 'abc', 'abcd', 'a', etc. -> CurveFitter now has this functionality
    - [x] CurveFitter's estimate_data method should convert an appended list into a dataframe and stop using concat dataframe
    - [x] CurveFitter now accepts list of x values for input, making this a more scalable solution
- [ ] Possible Data Interfacer between other objects and Grapher object to separate duties of data transformation and display, takes a dataframe and converts it into sets of x and y data for a grapher. This could be in the Grapher object itself.
- [ ] Change AlterBlock class
    - [ ] AlterBlock can be a dataframe with added functionality to create alternating blocks.
    - [ ] AlterBlock should rewrite the axis with possibility for time-series-like indexes
- [ ] Remove (redundant) DataRecorder class since new AlterBlock class will inherit the needed functionality pandas dataframe class
- [ ] Setup a new test that uses the old method as the test data, difference should be less than 5%
- [x] Use minutes as the fundamental data type of the analysis, so that everything can be an integer. (Was forced to re-convert back to hours because using minutes added instability to the curve fit calculation)
- [ ] Variable time steps
- [ ] Add error handling
- [ ] Selection of rainfall stations
- [ ] Use as a plugin to other programs
- [ ] CurveFitter detects how many parameter a function requires and makes a list of columns accordingly
- [ ] Make a documentation, possible logo of droplet hole in a graph
- [ ] Maybe add this to a personal website as part of a portfolio
- [ ] Curvefitter should detect whether the requested return period or duration already exists in the dataframe
- [ ] CurveFitter should be able to take multiple return period or duration requests
- [ ] Adding a function that properly formats dataframes to correct progression of return period and durations.
- [ ] rainfall_curve_fit should be more flexible with what time-series data it can estimate (1hr-, 30min-, 1min-interval)
- [x] remove xdata and ydata functionality form Ridf since the dataframe attributes handle this already.
- [x] remove func argument in graph_data and estimate_data because it should always be using the private _formula attribute