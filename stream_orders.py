from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("KafkaOrderConsumer") \
    .config("spark.jars.packages", 
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,"
        "org.apache.kafka:kafka-clients:3.2.0,"
        "org.xerial.snappy:snappy-java:1.1.8.4,"
        "org.apache.commons:commons-pool2:2.11.1,"
        "org.lz4:lz4-java:1.7.1,"
        "io.dropwizard.metrics:metrics-core:4.1.12.1") \
    .config("spark.hadoop.fs.s3a.access.key", "") \
    .config("spark.hadoop.fs.s3a.secret.key", "") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Step 2: Define schema for the JSON value
order_schema = StructType([
    StructField("order_id", StringType()),
    StructField("user", StructType([
        StructField("user_id", StringType()),
        StructField("name", StringType()),
        StructField("email", StringType()),
        StructField("address", StringType()),
        StructField("registered_at", StringType())
    ])),
    StructField("product", StructType([
        StructField("product_id", StringType()),
        StructField("name", StringType()),
        StructField("price", DoubleType()),
        StructField("category", StringType()),
        StructField("stock", IntegerType())
    ])),
    StructField("quantity", IntegerType()),
    StructField("total_price", DoubleType()),
    StructField("ordered_at", StringType())
])


# read from kafka

df_kafka = spark.readStream \
     .format("kafka") \
     .option("kafka.bootstrap.servers", "kafka:29092") \
     .option("failOnDataLoss", "false") \
     .option("subscribe", "orders") \
     .option("startingOffsets", "latest") \
     .load()

# Step 4: Convert Kafka value from bytes to string, then JSON
df_orders = df_kafka.selectExpr("CAST(value AS STRING) as json_str") \
    .withColumn("data", from_json(col("json_str"), order_schema)) \
    .select(
        col("data.order_id"),
        col("data.user.user_id").alias("user_id"),
        col("data.user.name").alias("user_name"),
        col("data.user.email").alias("user_email"),
        col("data.user.address").alias("user_address"),
        col("data.user.registered_at").alias("user_registered_at"),
        col("data.product.product_id").alias("product_id"),
        col("data.product.name").alias("product_name"),
        col("data.product.price").alias("product_price"),
        col("data.product.category").alias("product_category"),
        col("data.product.stock").alias("product_stock"),
        col("data.quantity"),
        col("data.total_price"),
        col("data.ordered_at")
    )

# Step 5: Start streaming output to console


# Console output

df_orders.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
# File output
# Write to disk as Parquet into "../data/"
query = df_orders.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3a://ecommerce-pipeline-kanishk/processed_orders/") \
    .option("checkpointLocation", "s3a://ecommerce-pipeline-kanishk/checkpoints/orders/") \
    .start()

query.awaitTermination()
