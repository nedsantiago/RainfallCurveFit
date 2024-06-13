import log
from data_handler import DirectoryHandler, request_open_file, request_write_file
from curve_fit import rainfall_curve_fit, DataRecorder, hoerl_mod


def main():
    # setup logger
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("BEGIN ALTBLOCK STOCHASTIC")
    
    # Using the DataHandler as settings file
    settings = DirectoryHandler()

    # Declaring formula
    formula = hoerl_mod

    # declare input and output paths, gui interaction can be done here
    INPUT_PATH = request_open_file("Open CSV RIDF file")
    OUTPUT_PATH = request_write_file("Save as")

    settings.add_path("ridf", INPUT_PATH)
    settings.add_path("csv_result", OUTPUT_PATH)

    # Now with the curve fit constants, get hourly rainfall intensities
    HOURLY_24 = [i for i in range(1, 24+1)]
    logger.debug(f"The value of HOURLY_24: {HOURLY_24}")

    # Conduct rainfall curve fit
    df_new = rainfall_curve_fit(settings.paths["ridf"], formula, HOURLY_24)

    # Record the final data into csv format
    record = DataRecorder()
    record.export_to_csv(df_new.df_output, settings.paths["csv_result"])


if __name__ == "__main__":
    print(f"Beginning {__file__}")
    main()
    print(f"Completed {__file__}")