import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from inspect import signature
from typing import Callable

# setup logger
import logging
logger = logging.getLogger(__name__)


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

def rainfall_curve_fit(path:str, formula:Callable, output_timeseries:list) -> pd.DataFrame:
    """
    This function takes a path of a CSV-formatted Rainfall Intensity-Duration-Frequency
    table and returns a time-series dataframe return period. This function follows the 
    Alternating Block Method for Stochastic Rainfall estimation.
    """

    # Read RIDF csv file
    input_ridf = pd.read_csv(path, index_col=0)
    # Initialize ridf pandas extension
    input_ridf.ridf
    # Convert the headers into integers
    input_ridf.columns = input_ridf.columns.map(int)
    # Convert minutes to hours, minutes makes the curve fit unstable
    input_ridf.columns = input_ridf.columns / 60
    logging.debug(f"rainfall_curve_fit received this input:\n{input_ridf}")

    # Transpose and curve fit the dataframe for a curve fitting model
    # that can complete missing return periods
    cf_T = CurveFitter(formula, input_ridf.T)

    # Estimate missing return period
    timeseries_150yr = cf_T.estimate_data(150)
    # Concatenate estimated data to get an RIDF table with desired Return Periods
    ridf_complete_rp = pd.concat([input_ridf, timeseries_150yr])
    logger.debug(f"The estimated 150-year RP values per duration are:\n{ridf_complete_rp}")
    logger.debug(f"The complete list of return period for analysis:\n {ridf_complete_rp.columns}")

    # Estimate Curve Fit constants for each return period
    cf_150 = CurveFitter(formula, ridf_complete_rp)
    logger.debug(f"The resulting coefficient table regression analysis:\n{cf_150.coeff_table}")

    # estimate stochastic rainfall
    dfi = cf_150.estimate_data(output_timeseries)
    logger.debug(dfi)

    # Rearrange into rainfall event using AlternateBlock object
    df_altblock = AlterBlock(dfi)
    logger.debug(f"The result of the AlternateBlock:\n{df_altblock.df_output}")

    return df_altblock

# RIDF Object
@pd.api.extensions.register_dataframe_accessor("ridf")
class Ridf():
    """
    This class extends the pandas dataframe class with ridf-related 
    functionality. It converts the headers into integers, and checks
    if the headers are sorted correctly.
    """

    def __init__(self, obj):
        logging.debug(f"Beginning Ridf initialization")
        logging.debug(f"Received obj: {obj}")
        # check if progression is correct
        err_msg = "column headers should be minutes and increasing order"
        assert self._is_col_correct_order(obj) == True, err_msg

    def _is_col_correct_order(self, obj) -> bool:
        """
        This method checks if columns are sorted correctly, increasing
        order from left to right.
        """
        
        # initialize the order flag as true
        has_correct_ordered_cols = True
        logger.debug(f"obj: {obj}")
        logger.debug(f"obj.columns: {obj.columns}")

        # loop through columns starting from the second column
        for col_num in range(1, len(obj.columns)):
            # if number is less than previous (likely hours)
            if float(obj.columns[col_num]) < float(obj.columns[col_num - 1]):
                # set flag to false
                has_correct_ordered_cols = False
        # return flag
        return has_correct_ordered_cols
    
    def _convert_headers_to_integer(self, obj):
        """
        This method ensures that the column headers are all integers
        """

        # convert all headers to integer
        obj.columns = obj.columns.map(int)
        logging.debug(f"obj.columns after conversion to integers:\n{obj.columns}")

# Curve Fitter Object
class CurveFitter():
    """
    This class estimates the parameters that fit a formula to a set of data.
    It takes a formula and a pandas dataframe of the data to be considered.
    Produce data from the curve fit results using the estimate_data method.
    """

    def __init__(self, formula, df):
        """
        Calculates the curve-fit parameter table and saves its results as 
        an attribute
        """

        self._dataframe = df
        self._formula = formula
        self.coeff_table = self._curvefit(formula, df)

    def _curvefit(self, func:Callable, df:pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the curve-fit parameter table and returns a Pandas 
        Dataframe
        """

        # get column names based on alphabet
        func_arg_count = self._get_args_count(func)
        # create a list of column names based on number of required arguments
        list_col = [chr(ord('`') + num + 1) for num in range(0, func_arg_count)]
        # collect list of dictionaries
        ls_dict = list()
        for i in range(0, len(df.index)):
            # Reads the dataframe for the i-th row
            df_ind = np.array(df.iloc[i,:])
            logger.debug(f"curve fitting df.iloc[{i},:]:\n{df.iloc[i,:]}")
            # Curve Fitting Algorithm
            try:
                popt, pcov = curve_fit(func, df.columns, df_ind)
            except RuntimeError as e:
                raise f"SciPy curve_fit could not estimate the parameters({popt}), error:\n {e}"
            # append this iteration to this list of dictionaries
            ls_dict.append(self._create_dict_from_lists(popt,list_col))
        coeff_table = pd.DataFrame(ls_dict)

        return coeff_table

    def _get_args_count(self, formula:Callable) -> int:
        """
        This method estimates the number of arguments a formula requires by
        using the signature function. It takes the number of arguments minus
        one, because 'x' parameter is an independent variable and not a parameter.
        """

        sign = signature(formula)
        return len(sign.parameters) - 1

    def _create_dict_from_lists(self, list_val:list, ls_col:list) -> dict:
        """
        This method takes a list of values and a list of columns then pairs each
        element in value (as value) to a column (as key) and returns a dictionary. 
        It aligns the two lists based on sequence.
        """

        # the two lists must have the same length
        assert len(list_val) == len(ls_col)

        i_dict = dict()
        for i in range(0, len(list_val)):
            i_dict[ls_col[i]] = list_val[i]

        logger.debug(
            f"Result of creating a dictionary for creating a df: {i_dict}"
            )
        
        return i_dict

    def graph_data(self, x_data):
        """This method returns graphing-ready data sets"""
        
        # using the x data, get all the y-values for each x-value
        popt = self.coeff_table.iloc[0,:]
        y_data = self._formula(x_data, *popt)
        # return x values as a numpy array
        return y_data
    
    def estimate_data(self, x_value:list) -> pd.DataFrame:
        """
        This method takes an independent variable and uses that to estimate
        dependent variables using the formula and parameter table curve 
        fit/regression model given.
        """

        logger.debug(f"Index, Columns, and Values of coefficient table:\n{self.coeff_table.index.values}")
        logger.debug(f"{self.coeff_table.columns}")
        logger.debug(f"{self.coeff_table.values}")

        # initialize a list of dictionaries
        ls_dict = list()
        # if x-values is not iterable (likely not a list)
        if not(hasattr(x_value, "__iter__")):
            # make it a list
            x_value = [x_value]
        # loop through the provided x-values to be estimated (row)
        for i in x_value:
            # parallel loop through the coefficient table row (popt) and dataframe index names (column)
            j_dict = dict()
            for j in range(0, len(self._dataframe.index)):
                # get the column name
                col_name = self._dataframe.index[j]
                # get formula parameters
                popt = self.coeff_table.iloc[j,:]
                # evaluate formula and add to dictionary
                j_dict[col_name] = self._formula(i, *popt)
            ls_dict.append(j_dict)

        df = pd.DataFrame(ls_dict)
        df.set_index(pd.Index(x_value), inplace=True)
        return df

# AlternateBlock object
class AlterBlock():
    """
    This object takes hourly duration RIDF and converts it into a
    single day rainfall event. First, it takes the cumulative amount
    and subtracts the ith hour rainfall to the i+1 hour rainfall.
    Then, it rearranges a dataframe's values using the Alternating
    Block Method.  Whereby, the largest values are at the middle, and
    the smallest values are near the start and end of the dataset
    """

    def __init__(self, df:pd.DataFrame):
        # Assuming the values are organized from largest to smallest

        # make a new dataframe where i hour is the result of i - (i+1)
        # if first row, retain
        logger.debug(f"df before subtraction by next value:\n{df}")
        for i in range(len(df.index)-1, 0, -1):
            df.iloc[i,:] = df.iloc[i-1,:] - df.iloc[i,:]
        logger.debug(f"df after the subtraction by next value:\n{df}")

        ## give two new columns, one that increments from 1 to infinity, and the other
        ## increments between 1 and 0. Each pair must be unique
        ## i.e. 1 0, 2 1, 3 0, 4 1, ...
        df['ind'] = df.index 
        df['IsOdd'] = df['ind'] % 2 != 0
        logger.debug(f"The value of df:\n{df}")

        ## whenever column 2 is 1 add the numbers into another dataframe
        ## where smallest value is at the bottom
        df_secondhalf = df.loc[df['IsOdd'] == 1]
        logger.debug(f"The value of IsOdd DF:\n{df_secondhalf}")
        
        ## whenever column 2 is zero add the number to its own dataframe
        ## where smallest value is at the top
        df_firsthalf = df.loc[df['IsOdd'] == 0]
        logger.debug(f"The value of NOT IsOdd DF:\n{df_firsthalf.sort_values(by = [df_firsthalf.columns[0]],ascending = True)}")
        logger.debug(f"The value of dftop:\n{df_firsthalf}")
        
        ## concat the two dataframes
        self.df_output =  pd.concat([df_firsthalf.sort_values(by = [df_firsthalf.columns[0]], ascending = True), df_secondhalf])
        self.df_output = self.df_output.drop(['IsOdd', 'ind'], axis=1)
        
# Graphing Object
class Grapher():
    """
    This object makes it easier to make graphs with a uniform aesthetic
    """

    def grapher(self, xdata, ydata, orig_xdata, orig_ydata):
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
        xmodel = np.linspace(min(xdata), max(xdata), 100)
        
        # adding the axes for the estimated and the actual data
        axes.plot(xdata, ydata, "b-", label="Hoerl Mod")
        axes.plot(orig_xdata, orig_ydata, "r.", label= "Actual")    
    
        # presenting the data for viewing
        plt.ylabel("Rainfall (mm)")
        plt.xlabel("Rainfall Duration (hrs)")
        plt.legend()
        plt.show()
        plt.close('all')

# Recording Object
class DataRecorder():
    """
    This object takes information and exports it into a file format 
    such as csv
    """
    
    def export_to_csv(self, pd_object, export_path):
        """
        This function takes a pandas dataframe and uses its to_csv 
        function to get save the output to the provided export path
        """
        pd_object.to_csv(export_path) 