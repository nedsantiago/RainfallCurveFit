import sys
sys.path.append("../src/")
import log
import logging
from curve_fit import *
import pandas as pd


class TestRainfallCurveFit():
    """This class collects all the functions that test the whole curve fit program.
    It take the test input data, and checks if it matches to the expected output data."""
    logger = logging.getLogger(__name__)

    def _test_data(self, input_dir, output_dir):
        """This method takes the directories of the input and expected output, and
        checks if the rainfall curve fit passes"""
        
        # round results to the fourth decimal place
        ROUND_DECIMAL = 4

        # Now with the curve fit constants, get hourly rainfall intensities
        HOURLY_24 = [i for i in range(1, 24+1)]
        logger.debug(f"The value of HOURLY_24: {HOURLY_24}")

        # calculate the result of rainfall curve fit
        altblock = rainfall_curve_fit(input_dir, hoerl_mod, HOURLY_24)
        dfin = altblock.df_output.round(ROUND_DECIMAL)
        logger.debug(f"dfin:\n{dfin}")

        # load test data
        dfout = pd.read_csv(output_dir, index_col=0).round(ROUND_DECIMAL)
        dfout.columns = dfout.columns.map(int)
        logger.debug(f"dfout:\n{dfout}")

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
    logger = logging.getLogger(__name__)

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