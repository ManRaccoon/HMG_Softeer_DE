import config
import log
import etl_extract
import etl_transform
import etl_load
import etl_analysis

def main():

    # EXTRACT 과정 진행
    log.message("Start EXTRACT step")
    etl_extract.extract_GDP(config.GDP_URL, config.JSON_PATH)
    log.message("Finish EXTRACT step: JSON file saved")

    # TRANSFORM 과정 진행
    log.message("Start TRANSFORM step")
    df = etl_transform.transform_GDP(config.JSON_PATH)
    log.message("Finish TRANSFORM step: Data ready")

    # LOAD 과정 진행
    log.message("Start LOAD step")
    etl_load.load_GDP(config.LOAD_JSON_PATH, df)
    log.message("Finish LOAD step: Data inserted into JSON file")

    etl_analysis.gdp_over_100b(config.LOAD_JSON_PATH)
    etl_analysis.gdp_region_avg(config.LOAD_JSON_PATH)

if __name__ == "__main__":
    main()