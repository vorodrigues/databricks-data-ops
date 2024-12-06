# Databricks notebook source
# MAGIC %md # Meta Ingestion - Ingest Table

# COMMAND ----------

# MAGIC %md ## Import ingestion functions

# COMMAND ----------

from metaingestion import MetaIngestion

# COMMAND ----------

# MAGIC %md ## Load parameters

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
database = dbutils.widgets.get("database")
table = dbutils.widgets.get('table')

# COMMAND ----------

# MAGIC %md ## Load configurations

# COMMAND ----------

conf = spark.sql(f'select * from vr_demo.kafka.control where catalog = "{catalog}" and database = "{database}" and table = "{table}"').collect()[0]
print(conf)

# COMMAND ----------

# MAGIC %md ## Ingest data

# COMMAND ----------

MetaIngestion(conf, spark)
