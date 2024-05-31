import pytest
from src.curve_fit import rainfall_curve_fit, hoerl_mod
import pandas as pd


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

        INPUT_DATA = r".\test\data\port\input_mmhr.csv"
        OUTPUT_DATA = r".\test\data\port\output_expected_mmhr.csv"

        self._test_data(INPUT_DATA, OUTPUT_DATA)

    def test_iloilo(self):
        """Tests data against the iloilo data set"""

        INPUT_DATA = r".\test\data\iloilo\input_mmhr.csv"
        OUTPUT_DATA = r".\test\data\iloilo\output_expected_mmhr.csv"

        self._test_data(INPUT_DATA, OUTPUT_DATA)