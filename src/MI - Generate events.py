# Databricks notebook source
# You can connect to Kafka over either SSL/TLS encrypted connection, or with an unencrypted plaintext connection.
# Just choose the set of corresponding endpoints to use.
# If you chose the tls servers, you must enable SSL in the Kafka connection, see later for an example.
kafka_bootstrap_servers_tls = dbutils.secrets.get("oetrta", "kafka-bootstrap-servers-tls")
#kafka_bootstrap_servers_plaintext = dbutils.secrets.get("oetrta", "oetrta-kafka-servers-plain")
# Full username, e.g. "aaron.binns@databricks.com"
username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user')
# Short form of username, suitable for use as part of a topic name.
user = username.split("@")[0].replace(".","_")
# DBFS directory for this project, we will store the Kafka checkpoint in there
project_dir = f"/home/{username}/kafka_demo"
checkpoint_location = f"{project_dir}/checkpoints/kafka"

# COMMAND ----------

# MAGIC %md ## Create topic

# COMMAND ----------

topic = f"{user}_oetrta_kafka_topic"
print(topic)

# COMMAND ----------

# DBTITLE 1,Create UDF for UUID
from datetime import datetime
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime
import random, string, uuid

uuidUdf= udf(lambda : uuid.uuid4().hex,StringType())

# COMMAND ----------

input_path = "/databricks-datasets/structured-streaming/events"
input_schema = spark.read.json(input_path).schema

# COMMAND ----------

print(input_schema)

# COMMAND ----------

# DBTITLE 1,Loading streaming dataset
input_path = "/databricks-datasets/structured-streaming/events"
input_schema = spark.read.json(input_path).schema

input_stream = (spark
  .readStream
  .schema(input_schema)
  .json(input_path)
  .withColumn("processingTime", lit(datetime.now().timestamp()).cast("timestamp"))
  .withColumn("eventId", uuidUdf()))

# display(input_stream)

# COMMAND ----------

# DBTITLE 1,WriteStream to Kafka
# Clear checkpoint location
dbutils.fs.rm(checkpoint_location, True)

# For the sake of an example, we will write to the Kafka servers using SSL/TLS encryption
# Hence, we have to set the kafka.security.protocol property to "SSL"
(input_stream
   .select(col("eventId").alias("key"), to_json(struct(col('action'), col('time'), col('processingTime'))).alias("value"))
   .writeStream
   .format("kafka")
   .option("kafka.bootstrap.servers", kafka_bootstrap_servers_tls )
   .option("kafka.security.protocol", "SSL")
   .option("checkpointLocation", checkpoint_location)
   .option("topic", topic)
   .trigger(availableNow=True)
   .start()
)
