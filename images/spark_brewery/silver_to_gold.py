# import libraries
import os
from os.path import abspath
from datetime import datetime
import logging
from resources.golden_utils import (
    gold_table,
    gold_modelling,
    time_update_gold
)

from resources.conf_paths import (
    silver_layer_path,
    golden_layer_path
)

from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from delta import DeltaTable



if __name__ == '__main__':
    # init session
    spark = (
        SparkSession.builder.appName("silver-to-gold-sparksession")
        .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
        .enableHiveSupport()
        .getOrCreate()
    )

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    try:
        df_silver_data = DeltaTable.forPath(spark, silver_layer_path) \
            .toDF()
        logging.info(f' [SUCCESS] | LOAD DATA FROM {silver_layer_path}')

    except Exception as e:
        logging.error(f'[ERROR] | FAILED TO LOAD DATA. ERROR: {str(e)}')
        raise
    
    try:
        gold_table(spark, golden_layer_path)
        logging.info(f'[SUCCESS] | CREATED GOLD TABLE IN {golden_layer_path}')

    except Exception as e:
        logging.error(f'[ERROR] | FAILED TO CREATE GOLD TABLE. ERROR: {str(e)}')
        raise

    time_load = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    df_gold_data = gold_modelling(df_silver_data) \
        .withColumn(
            time_update_gold, F.lit(time_load).cast('timestamp')
        )
        

    try:
        # save into gold_layer
        df_gold_data.write \
            .format('delta') \
            .mode('overwrite') \
            .save(golden_layer_path)
        logging.info(f' [SUCCESS] | SAVE DATA INTO {golden_layer_path}')
        
    except Exception as e:
        logging.error(f'[ERROR] | FAILED TO SAVE DATA. ERROR: {str(e)}')
        raise
    
    spark.stop()