DATA_INGESTION_DIR = 'data_ingestion'
DATA_INGESTION_DOWNLOAD_DIR = 'download'
DATA_INGESTION_FILE_NAME = 'finance_complaint'
DATA_INGESTION_FEATURE_STORE_DIR = 'feature_store'
DATA_INGESTION_FAILED_DIR = 'failed_download_file'
DATA_INGESTION_METADATA_FILE_NAME = 'meta_info.yaml'
DATA_INGESTION_MIN_START_DATE = '2011-12-01'
DATA_INGESTION_DATA_SOURCE_URL = f"https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/" \
                      f"?date_received_max=<todate>&date_received_min=<fromdate>" \
                      f"&field=all&format=json"