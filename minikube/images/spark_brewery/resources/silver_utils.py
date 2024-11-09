import pyspark.sql.functions as F
from pyspark.sql.types import (
    StringType, 
    FloatType, 
    StructType, 
    StructField
)



SCHEMA_RAW_DATA = StructType([
    StructField('id',             StringType(), False),
    StructField('name',           StringType(), True),
    StructField('brewery_type',   StringType(), True),
    StructField('address_1',      StringType(), True),
    StructField('address_2',      StringType(), True),
    StructField('address_3',      StringType(), True),
    StructField('city',           StringType(), True),
    StructField('state_province', StringType(), True),
    StructField('postal_code',    StringType(), True),
    StructField('country',        StringType(), True),
    StructField('longitude',      StringType(), True),
    StructField('latitude',       StringType(), True),
    StructField('phone',          StringType(), True),
    StructField('website_url',    StringType(), True),
    StructField('state',          StringType(), True),
    StructField('street',         StringType(), True),
])




def adjusting_column_types(df):
    """
    Adjusts the column types and sanitizes data in the given DataFrame.

    This function casts various columns in the DataFrame to specific types, 
    such as converting 'id' to IntegerType and 'latitude' and 'longitude' 
    to FloatType after replacing commas with periods. It also ensures that 
    'latitude' and 'longitude' are within valid ranges, setting them to 0.0 
    if they exceed the allowed boundaries.

    Parameters:
        df (DataFrame): Input DataFrame with columns to be adjusted.

    Returns:
        DataFrame: A new DataFrame with adjusted column types and sanitized data.
    """
    df_adjusted_type = df \
        .withColumn('id', F.col('id').cast(StringType())) \
        .withColumn('name', F.col('name').cast(StringType())) \
        .withColumn('brewery_type', F.col('brewery_type').cast(StringType())) \
        .withColumn('address_1', F.col('address_1').cast(StringType())) \
        .withColumn('address_2', F.col('address_2').cast(StringType())) \
        .withColumn('address_3', F.col('address_3').cast(StringType())) \
        .withColumn('city', F.col('city').cast(StringType())) \
        .withColumn('postal_code', F.col('postal_code').cast(StringType())) \
        .withColumn('country', F.col('country').cast(StringType())) \
        .withColumn(
            'latitude', F.regexp_replace('latitude', ',', '.').cast(FloatType())
        ) \
        .withColumn(
            'latitude', F.when(
                (F.col('latitude') > 90) | (F.col('latitude') < -90), 0.0
            ).otherwise(F.col('latitude'))
        ) \
        .withColumn(
            'longitude', F.regexp_replace('longitude', ',', '.').cast(FloatType())
        ) \
        .withColumn(
            'longitude', F.when(
                (F.col('longitude') > 180) | (F.col('longitude') < -180), 0.0
            ).otherwise(F.col('longitude'))
        ) \
        .withColumn('phone', F.col('phone').cast(StringType())) \
        .withColumn('website_url', F.col('website_url').cast(StringType())) \
        .withColumn('state', F.col('state').cast(StringType())) \
        .withColumn('street', F.col('street').cast(StringType()))

    return df_adjusted_type


def clean_columns_for_silver(df):
    """
    Cleans specific text columns in the DataFrame by:
    - Removing extra spaces
    - Converting text to lowercase
    - Removing special characters

    Args:
        df (DataFrame): The Spark DataFrame.

    Returns:
        DataFrame: A DataFrame with cleaned columns.
    """
    columns_to_clean = ['address_1', 'address_2', 'address_3', 'city', 
                        'country', 'state', 'street']
    
    for column in columns_to_clean:
        df = df.withColumn(
            column,
            F.lower(F.trim(F.regexp_replace(F.col(column), '[^a-zA-Z0-9 ]', '')))
        )
    
    return df
