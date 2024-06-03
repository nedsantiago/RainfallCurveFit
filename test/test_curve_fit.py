import sys
sys.path.append("../src/")
import log
import logging
from curve_fit import *
import pandas as pd


logger = logging.getLogger(__name__)

class TestRainfallCurveFit():
    """This class collects all the functions that test the whole curve fit program.
    It take the test input data, and checks if it matches to the expected output data."""

    def _test_data(self, input_dir, output_dir):
        """This method takes the directories of the input and expected output, and
        checks if the rainfall curve fit passes"""
        
        # round results to the fourth decimal place
        ROUND_DECIMAL = 4

        # calculate the result of rainfall curve fit
        altblock = rainfall_curve_fit(input_dir, hoerl_mod)
        dfin = altblock.df_output.round(ROUND_DECIMAL)
        print(f"dfin:\n{dfin}")

        # load test data
        dfout = pd.read_csv(output_dir, index_col=0).round(ROUND_DECIMAL)
        dfout.columns = dfout.columns.map(int)
        print(f"dfout:\n{dfout}")

        # checking if the results match the test data
        assert dfin.equals(dfout), f"Result of {input_dir} do not match {output_dir}"

    def test_port(self):
        """Tests data against the port data set"""

        logger.debug("Beginning test_port")
        INPUT_DATA = r"./data/port/input_mmhr.csv"
        OUTPUT_DATA = r"./data/port/output_expected_mmhr.csv"

        self._test_data(INPUT_DATA, OUTPUT_DATA)

    def test_iloilo(self):
        """Tests data against the iloilo data set"""

        logger.debug("Beginning test_iloilo")
        INPUT_DATA = r"./data/iloilo/input_mmhr.csv"
        OUTPUT_DATA = r"./data/iloilo/output_expected_mmhr.csv"

        self._test_data(INPUT_DATA, OUTPUT_DATA)

class TestRidf():
    """
    This class collects the tests used for the Ridf class object.
    """

    def _test_input_vs_output(self, test_input, expected_output):
        """Checks for equivalence"""
        err_msg = f"Result of {test_input} do not match {expected_output}"
        assert test_input == expected_output, err_msg

    def _preprocess_input(self, test_input):
        pass

    def _preprocess_output(self, expected_output):
        pass

    def test_ridf(self):
        pass