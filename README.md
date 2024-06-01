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
- [ ] Add error handling
- [ ] Variable time steps
- [ ] Selection of rainfall stations
- [ ] Use as a plugin to other programs
- [ ] CurveFitter detects how many parameter a function requires and makes a list of columns accordingly