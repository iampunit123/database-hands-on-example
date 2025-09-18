import dlt
from dlt.sources.sql_database import sql_database

# Connect to MySQL
mysql_pipeline = dlt.pipeline(
    pipeline_name="mysql_to_postgres",
    destination="postgres",  # target DB
    dataset_name="gallery"
)

# MySQL connection
source = sql_database(
    credentials="mysql+pymysql://root:1234@localhost:3306/gallery",
    schema="gallery"
)

# Run migration
mysql_pipeline.run(source)
