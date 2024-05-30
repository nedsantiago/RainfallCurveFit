import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
import logging


def main():
    # Declaring the folder location, file name, and formula
    folder_path = r"..\test\data\port"
    file_name = r"input_mmhr.csv"
    export_path = r"..\test\data\port\output_mmhr.csv"
    formula = hoerl_mod

    # Using the DataRetriever, create the path for the file
    ridf_retriever = DirectoryHandler()

    ridf_retriever.full_path(
        folder_path = folder_path,
        file_name = file_name)

    # Conduct rainfall curve fit
    df_new = rainfall_curve_fit(ridf_retriever.file_path, formula)

    # Record the final data into csv format
    record = DataRecorder()
    record.export_to_csv(df_new.df_output,export_path)


def rainfall_curve_fit(path, formula):
    """This function takes a path of a Rainfall-Intensity-Duration Frequency table
    and returns a table of time-series data for each return period. This follows the
    Alternating Block Method for Stochastic Rainfall estimation"""

    # Using the Ridf object, create a Pandas DataFrame of the RIDF table. Then clean and organize
    ridf_raw = Ridf(path)

    ## Note: take adavantage of transposition, df.T for getting 150-year RP
    # Estimate the 150-year Return Period
    cf_T = CurveFitter()
    cf_T.curvefit(formula, ridf_raw.df.T)

    # Replace the current dataframe with a new one with 150-year RP
    ridf_adj = ridf_raw
    ridf_adj.df = cf_T.estimate_data(150,formula,ridf_raw.df)
    ridf_adj.time_scale()
    # print(f"The value of ridf_adj.df:\n{ridf_adj.df}")

    # Get the curve fit constants for each return period
    cf_adj = CurveFitter()
    cf_adj.curvefit(formula, ridf_adj.df)
    # print(f"The value of cf_adj.coeff_table:\n{cf_adj.coeff_table}")

    # Now with the curve fit constants, get the hourly rainfall intensities
    HOURLY_24 = [i for i in range(1,24+1)]
    # print(f"The value of HOURLY_24: {HOURLY_24}")

    dfi = pd.DataFrame()
    for i in HOURLY_24:
        # print(f"For hour {i} of type {type(i)}:")
        dfi = cf_adj.estimate_data(i,formula,dfi)
        # print(dfi)

    # Rearrange into rainfall event using AlternateBlock object
    df_new = AlterBlock(dfi)
    # print(f"The result of the AlternateBlock:\n{df_new.df_output}")

    return df_new
    

# Delcare all curve models to be trialed
def weibull(x,a,b,c):
    return a-b*np.exp(-c*x)
def weibull0(x,a,b,c,d):
    return a-b*np.exp(-c*x**d)
def sigmoid_b(x,a,b,c):
    return a/(1.0+np.exp(-1*(x-b)/c))
def hoerl_mod(x,a,b,c):
    return a*b**(1/x)*x**c
def vap_pres(x,a,b,c):
    return np.exp(a+(b/x)+c*np.log(x))
def log_fit(x,a,b):
    return a+b*np.log(x)

# Retriever Object
class DirectoryHandler:
    """Builds and saves a file path for later use"""
    file_path = ""
    def full_path(self, folder_path:str, file_name:str):
        self.file_path = os.path.join(folder_path,file_name)
        return  self.file_path

# RIDF Object
class Ridf:
    """This object contains the rainfall-intensity-duration frequency
    table in its raw, approximated, and resulting values"""
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path,index_col= 0)   # EDIT init with df

    def clean(self):
        """This method checks for incorrect or missing data."""
        pass
    def time_scale(self):
        """This method changes the time scale data type 
        and format to a standard format."""
        mydict = {'10':1/6,'20':1/3,'30':1/2, # EDIT DICTIONARY
        '1':1,'2':2,'3':3,
        '6':6,'12':12,'24':24}
        self.df = self.df.rename(columns= mydict)
    def xdata(self):
        """This method creates the x-axis data, which is mainly used
        for graphs"""
        return self.df.index
    def ydata(self):
        """This method creates the y-axis data, which is mainly used
        for graphs"""
        pass

# Curve Fitter Object
class CurveFitter():
    """This object takes a dataframe and outputs a curve-fit parameter table"""

    def curvefit(self, func, df):
        """Calculates the curve-fit parameter table and returns a Pandas Dataframe"""
        self.func = func
        # Placeholder floating point values for xdf
        df_col = df.columns
        self.df_col = df.columns
        self.df_ind = df.index
        self.df_collen = len(df.columns)
        self.df_indlen = len(df.index)
        list_col = list('abc') # EDIT THIS: needs to be useable by many formats
        coeff_table = pd.DataFrame(columns=list_col)
        for i in range(0,len(df.index)):
            # Reads the dataframe for the i-th row
            df_ind = np.array(df.iloc[i,:])
            # Curve Fitting Algorithm
            popt, pcov = curve_fit(func, df_col, df_ind)
			# concatenates this iteration's dataframe to the coefficcient table dataframe
            coeff_table = pd.concat([coeff_table,
            pd.DataFrame([popt], columns = list_col, index = [df.index[i]])])
        self.coeff_table = coeff_table

    def graph_data(self,x_data,func):
        """This method returns graphing-ready data sets"""
        
        # using the x data, get all the y-values for each x-value
        popt = self.coeff_table.iloc[0,:]
        y_data = func(x_data,*popt)
        # return x values as a numpy array
        return y_data
    
    def estimate_data(self,x_value,func, df):           # EDIT x_value to be a list
        """This method estimates the values for a new dataframe or
        dataframe edition"""

        # using the x data, get all the y-values for each x-value
        y_data = pd.DataFrame(columns=[x_value])
        # print(f"Values of self.coeff_table:\n{self.coeff_table}")
        # print(f"Values of self.df_ind:\n{self.df_ind}")
        # print(f"Values of self.df_col:\n{self.df_col}")
        for i in range(0,len(self.df_ind)):
            # take this iteration's constants
            y_ind = self.df_ind[i]
            popt = self.coeff_table.iloc[i,:]
            # print(f"Value of y_ind:\n{y_ind}")
            # print(f"Value of popt for iteration {i}:\n{popt}\nType of popt:\n{type(popt)}")
            # calculate the estimated value
            # concat this into a pandas dataframe 
            y_data = pd.concat([y_data,pd.DataFrame([func(x_value,*popt)], columns = [x_value], index = [y_ind])])
            # print(f"y_data:\n{y_data}")
        # return the complete dataframe
        df2 = pd.concat([y_data.T,df])
        df2 = df2.sort_index()
        return df2

# AlternateBlock object
class AlterBlock():
    """This object takes hourly duration RIDF and converts it into a
    single day rainfall event. First, it takes the cumulative amount
    and subtracts the ith hour rainfall to the i+1 hour rainfall.
    Then, it rearranges a dataframe's values using the Alternating
    Block Method.  Whereby, the largest values are at the middle, and
    the smallest values are near the start and end of the dataset"""
    def __init__(self,df):
        ## Assuming the values are organized from largest to smallest
        
        ## make a new dataframe where i hour is the result of i - (i+1)
        ## if first row, retain
        # print(f"df before the subtraction:\n{df}")
        for i in range(len(df.index)-1,0,-1):
            df.iloc[i,:] = df.iloc[i-1,:] - df.iloc[i,:]
            ## if not first row, subtract value to previous value insert
        # print(f"df AFTER the subtraction:\n{df}")


        ## give two new columns, one that increments from 1 to infinity, and the other
        ## increments between 1 and 0. Each pair must be unique
        ## i.e. 1 0, 2 1, 3 0, 4 1, ...
        df['ind'] = df.index 
        df['IsOdd'] = df['ind'] % 2 != 0
        # print(f"The value of df:\n{df}")

        ## whenever column 2 is 1 add the numbers into another dataframe
        ## where smallest value is at the bottom
        dfbot = df.loc[df['IsOdd'] == 1]
        # print(f"The value of IsOdd DF:\n{dfbot}")
        
        ## whenever column 2 is zero add the number to its own dataframe
        ## where smallest value is at the top
        dftop = df.loc[df['IsOdd'] == 0]
        # print(f"The value of NOT IsOdd DF:\n{dftop.sort_values(by = [dftop.columns[0]],ascending = True)}")
        # print(f"The value of dftop:\n{dftop}")
        
        ## concat the two dataframes
        self.df_output =  pd.concat([dftop.sort_values(by = [dftop.columns[0]],ascending = True),dfbot])
        self.df_output = self.df_output.drop(['IsOdd','ind'], axis=1)

        
# Graphing Object
class Grapher():
    """This object makes it easier to make graphs with a uniform aesthetic"""
    def grapher(self,xdata,ydata,orig_xdata,orig_ydata):
        # record the inputs
        self.xdata = xdata # EDIT: Add these inputs to __init__
        self.ydata = ydata
    
        # graph sizes (later each were divided by 100)
        graph_width = 800 # EDIT: Add these inputs to __init__
        graph_height = 600
    
        # initializing the figure with the sizes
        fig = plt.figure(figsize = (graph_width/100, graph_height/100))
        # adding a plot to the graph
        axes = fig.add_subplot(111)
        xmodel = np.linspace(min(xdata),max(xdata),100)
        
        # adding the axes for the estimated and the actual data
        axes.plot(xdata,ydata,"b-", label="Hoerl Mod")
        axes.plot(orig_xdata,orig_ydata, "r.", label= "Actual")    
    
        # presenting the data for viewing
        plt.ylabel("Rainfall (mm)")
        plt.xlabel("Rainfall Duration (hrs)")
        plt.legend()
        plt.show()
        plt.close('all')

# RIDF Verifier Object



# Recording Object
class DataRecorder():
    """This object takes information and exports it into a file format such as csv"""
    
    def export_to_csv(self,pd_object,export_path):
        """This function takes a pandas dataframe and uses its to_csv function
        to get save the output to the provided export path"""
        pd_object.to_csv(export_path) 


if __name__ == "__main__":
    print(f"Beginning {__file__}")
    main()
    print(f"Completed {__file__}")