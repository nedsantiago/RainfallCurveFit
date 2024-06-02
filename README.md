# Alternating Block Method for Stochastic Rainfall
![GitHub Actions Build Status](https://github.com/nedsantiago/altblock_stochastic/actions/workflows/python-app.yml/badge.svg)


## Purpose
This script aims to reduce the time spent converting Rainfall-Intensity Duration Frequency Curves (RIDF) into usable rainfall data for Hydrologic and Hydraulic Simulations

## Project Author
* Ned Santiago, started on November 28, 2022

## Components
* File Retrievers
    * DirectoryHandler - retrieves the file paths and stores for use
* rainfall calculations
    * Ridf - an ridf object that holds the rainfal-intensity duration table
    * AlterBlock - rearranges the time series data into an alternating block result
* curve fit
    * CurveFitter - the calculator for curve fitting
* visualize results
    * Grapher - graphs and produces figures

## Required Inputs
* The path to the directory of the rainfall data
* File name of the rainfall data
* File name and directory of the output

## Future Updates
- [x] Github integration
- [x] Pytest integration
- [x] Singleton data handler, separate data handler and path taker
- [x] Provide a GUI to the DataRetriever object
- [x] Logging file that shows the process of the calculation, important for debugging the software
- [ ] Use class handlers.RotatingFileHandler in log file to also force log file size limit
- [ ] Setup a new test that uses the old method as the test data, difference should be less than 5%
- [ ] Use minutes as the fundamental data type of the analysis, so that everything can be an integer
- [ ] Ridf should enforce that durations should be in minutes format, always increasing from left to right
- [ ] Maybe enforce that it should be an intensity scale i.e. mm/hr per return-period-duration and not mm per return-period-duration
- [ ] Ridf should act more like a dataframe with functionality to check data validity. Thus, need to inherit pd.Dataframe
- [ ] Ridf can have an abstract method so that it can be built on by another class
- [ ] CurveFitter should immediately start curve fitting after receiving the path to the data
- [ ] Optimize the CurveFitter code, many variables were not used or not needed (e.g. some column and index length variables)
- [ ] CurveFitter curvefit method should only work on one row of data, another method should be responsible for compiling to table
- [ ] CurveFitter curvefit method should work with any formula or varying variable counts of formulas 'abc', 'abcd', 'a', etc.
- [ ] CurveFitter's estimate_data method should be convert an appended list into a dataframe and stop using concat dataframe
- [ ] Possible Data Interfacer between other objects and Grapher object to separate duties of data transformation and display, takes a dataframe and converts it into sets of x and y data for a grapher. This could be in the Grapher object itself.
- [ ] AlterBlock can be a dataframe with added functionality to create alternating blocks.
- [ ] AlterBlock should rewrite the axis with possibility for time-series-like indexes
- [ ] Variable time steps
- [ ] Add error handling
- [ ] Selection of rainfall stations
- [ ] Use as a plugin to other programs
- [ ] CurveFitter detects how many parameter a function requires and makes a list of columns accordingly
- [ ] Make a documentation, possible logo of droplet hole in a graph
- [ ] Maybe add this to a personal website as part of a portfolio