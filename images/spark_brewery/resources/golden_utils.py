from delta import DeltaTable
import pyspark.sql.functions as F

time_update_gold = 'last_updated_gold'
agregation_name = 'breweries_count'


def gold_table(spark, path_gold):
    (
        DeltaTable.createIfNotExists(spark)
        .tableName("brewery_type_location")
        .location(path_gold)
        .addColumn("brewery_type", "string")
        .addColumn("country", "string")
        .addColumn("state", "string")
        .addColumn("city", "string")
        .addColumn(agregation_name, "int")
        .addColumn(time_update_gold, "TIMESTAMP")
        .execute()
    )
    
def gold_modelling(df):
   df = df.select(
       'brewery_type',
       'country',
       'state',
       'city'
    ) \
    .groupBy('brewery_type', 'country', 'state', 'city').count() \
    .withColumnRenamed('count', agregation_name) \
    .withColumn(agregation_name, F.col(agregation_name).cast("int"))
   
   return df