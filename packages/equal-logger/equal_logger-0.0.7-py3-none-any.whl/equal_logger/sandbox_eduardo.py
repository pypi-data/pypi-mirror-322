from equal_logger import Logger
from equal_logger import SqlQualityTest

logger = Logger(
    cloud="GCP",
    script_name="sandbox_1.py",
    data_source="Testando",
    project="pessoal",
    credentials=r"C:\Users\eduardo\Desktop\EQUAL-GITHUB\equal-logger\src\equal_logger\cred.json"
)

# %% == testing logger ==

logger.success("titulo 1", "descricao 1", print_log=False)
logger.info("titulo 1", "descricao 1", print_log=False)
logger.error("titulo 1", "descricao 1", print_log=False)

logger.save()

# %% == testing quality for bigQuery ==

# tester = SqlQualityTest(logger)
#
# tester.test_duplicate_rows('ext.linhas_duplicadas', 'ID')  # RETORNA NOK
# tester.test_duplicate_rows('ext.sem_duplicatas', 'ID')  # RETORNA OK
# tester.test_query_returns_zero_rows('SELECT * FROM ext.sem_duplicatas WHERE 0=0')  # RETORNA NOK
# tester.test_query_returns_zero_rows('SELECT * FROM ext.sem_duplicatas WHERE 1=0')  # RETORNA OK
# tester.test_temporal_null_or_zero_values(schema_table='ext.tabela_com_data',
#                                          date_column='data',
#                                          evaluated_column='numero',
#                                          days=1)  # RETORNA NOK
# tester.test_temporal_null_or_zero_values(schema_table='ext.tabela_com_data',
#                                          date_column='data',
#                                          evaluated_column='numero',
#                                          days=7)  # RETORNA OK
#
# tester.test_has_data_for_each_day(schema_table='ext.tabela_com_data',
#                                   date_column='data',
#                                   days=365,
#                                   include_today=True)
#
# logger.save()

# %% == testing quality for SQL Pool ==

tester = SqlQualityTest(
    logger=logger,
    credentials_path=r'C:\Users\eduardo\Desktop\EQUAL-GITHUB\equal-logger\src\equal_logger\cred_azure.json',
    cloud="AZURE"
)

# tester.test_duplicate_rows('dw.DIM_CLIENTE', 'ID_CLIENTE_DB')  # RETORNA NOK
# tester.test_duplicate_rows('dw.DIM_FILIAIS', 'ID_ACADEMIA_W12')  # RETORNA OK
tester.test_query_returns_zero_rows('SELECT ID_ACADEMIA_W12 FROM dw_pbi.AGG_TICKET_MEDIO WHERE 0=0')  # RETORNA NOK
tester.test_query_returns_zero_rows('SELECT ID_ACADEMIA_W12 FROM dw_pbi.AGG_TICKET_MEDIO WHERE 1=0')  # RETORNA OK
# tester.test_temporal_null_or_zero_values(schema_table='customize_allpfitness.meta_fact_ads_insights',
#                                          date_column='event_date',
#                                          evaluated_column='lead',
#                                          days=7)  # RETORNA OK
