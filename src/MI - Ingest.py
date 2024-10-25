# Databricks notebook source
# MAGIC %md # Meta Ingestion - Ingest Table

# COMMAND ----------

# MAGIC %md ## Import ingestion functions

# COMMAND ----------

from utils import *

# COMMAND ----------

# MAGIC %md ## Load parameters

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
database = dbutils.widgets.get("database")
table = dbutils.widgets.get('table')

# COMMAND ----------

# MAGIC %md ## Load configurations

# COMMAND ----------

conf = spark.sql(f'select * from main.vr_mi_admin.control where catalog = "{catalog}" and database = "{database}" and table = "{table}"').collect()[0]
print(conf)

# COMMAND ----------

# MAGIC %md ## Ingest data

# COMMAND ----------

KafkaIngestion(conf, spark)
