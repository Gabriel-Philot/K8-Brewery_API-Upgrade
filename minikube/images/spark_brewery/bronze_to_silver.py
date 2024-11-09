import os
from os.path import abspath
from datetime import datetime
import logging
from resources.utils import load_config
from resources.silver_utils import (
    SCHEMA_RAW_DATA,
    adjusting_column_types,
    clean_columns_for_silver
)

from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


config = load_config()

bronze_layer_path = config['storages']["brew_paths"]['bronze']
silver_layer_path = config['storages']["brew_paths"]['silver']



if __name__ == '__main__':
    # init session
    spark = (
        SparkSession.builder.appName("bronze-to-silver-sparksession")
        .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
        .enableHiveSupport()
        .getOrCreate()
    )

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")


    try:
        df_raw_data = spark \
            .read.schema(SCHEMA_RAW_DATA).json(bronze_layer_path, multiLine=True)
        logging.info(f' [SUCCESS] | LOAD DATA FROM {bronze_layer_path}')
    except Exception as e:
        logging.error(f'[ERROR] | FAILED TO LOAD DATA. ERROR: {str(e)}')
        raise
    
    # After reviewing, 'state_province' is identical to 'state', so we can drop it.
    df_raw_data = df_raw_data.drop('state_province')

    df_silver = adjusting_column_types(df_raw_data)
    df_silver = clean_columns_for_silver(df_silver)

    # adding 'last_updated_silver'
    time_load = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    df_silver = df_silver \
        .withColumn(
                'last_updated_silver', F.lit(time_load).cast('timestamp')
        ).distinct() # removing duplicates
    

    try:
        # save into silver_layer
        df_silver.write \
            .format('delta') \
            .mode('overwrite') \
            .option('path', silver_layer_path) \
            .partitionBy('country') \
            .save()

        logging.info(f'[SUCCESS] | SAVE DATA INTO {silver_layer_path}')
    except Exception as e:
        logging.error(f'[ERROR] | FAILED TO SAVE DATA INTO. ERROR: {str(e)}')
        raise
    
    df_silver.printSchema()

    # Stop the Spark session
    spark.stop()

