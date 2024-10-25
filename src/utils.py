# 0/ Parameters - Update with your settings
project_dir = "/home/victor.rodrigues@databricks.com/meta_ingestion"
checkpoint_location = f"{project_dir}/checkpoints"
kafka_secret_scope = "oetrta"
kafka_secret_key = "kafka-bootstrap-servers-tls"



# 1/ Define merge function
def merge_delta(microbatch, target):

  table = f'{target.catalog}.{target.database}_silver.{target.table}'
  merge_keys = target.merge_keys.split(',')
  on_clause = " AND ".join([f"t.{key} = s.{key}" for key in merge_keys])
  ts_key = target.ts_key

  if target.clustering_keys:
    clustering_keys = target.clustering_keys.split(',')
  else:
    clustering_keys = None

  # Deduplica registros dentro do microbatch e mantém somente o mais recente
  microbatch = microbatch.orderBy(ts_key, ascending=False).dropDuplicates(merge_keys)
  microbatch.createOrReplaceTempView("microbatch")
  
  try:
    # Caso a tabela já exista, os dados serão atualizados com MERGE
    # microbatch._jdf.sparkSession().sql(f"""
    microbatch.sparkSession.sql(f"""
      MERGE INTO {table} t
      USING microbatch s
      ON {on_clause}
      -- WHEN MATCHED AND s.op_code = 'd' THEN DELETE
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *
    """)
  except:
    # Caso a tabela ainda não exista, será criada
    if clustering_keys:
      microbatch.writeTo(table).clusterBy(*clustering_keys).create()
    else:
      microbatch.writeTo(table).create()



# 2/ Define ingestion function
from pyspark.sql.functions import *

def KafkaIngestion(target, spark):
  
  catalog = target.catalog
  database = target.database
  table = target.table
  topic = target.topic
  schema = target.schema

  print(f'Ingesting table {catalog}.{database}.{table}')

  from databricks.sdk.runtime import dbutils
  kafka_bootstrap_servers_tls = dbutils.secrets.get(kafka_secret_scope, kafka_secret_key)

  # Bronze Layer

  rawDF = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers_tls)
    .option("kafka.security.protocol", "SSL")
    .option("startingOffsets", "earliest")
    .option("subscribe", topic)
    .load()
  )

  bronzeDF = rawDF.select(
      col("key").cast("string").alias("key"),
      col("value").cast("string").alias("value")
  )

  (bronzeDF.writeStream
    .outputMode("append")
    .option("checkpointLocation", f"{checkpoint_location}/{catalog}/{database}_bronze/{table}")
    .trigger(availableNow=True)
    .table(f"{catalog}.{database}_bronze.{table}")
    .awaitTermination()
  )

  # Silver Layer

  silverDF = (spark.readStream.table(f"{catalog}.{database}_bronze.{table}")
    .select(col("key").alias("eventId"), from_json(col("value"), schema).alias("json"))
    .select("eventId", "json.*")
  )

  (silverDF.writeStream
    .outputMode("update")
    .option("checkpointLocation", f"{checkpoint_location}/{catalog}/{database}_silver/{table}")
    .trigger(availableNow=True)
    .foreachBatch(lambda microbatch, x: merge_delta(microbatch, target))
    .start()
    .awaitTermination()
  )