# Databricks notebook source
# MAGIC %md # Meta Ingestion - List Tables

# COMMAND ----------

# MAGIC %md ## Load parameters

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
database = dbutils.widgets.get("database")

# COMMAND ----------

# MAGIC %md ## List active table ingestions

# COMMAND ----------

tables = [table.table for table in spark.sql(f'select * from main.vr_mi_admin.control where catalog = "{catalog}" and database = "{database}" and active = true').collect()]
print(tables)

# COMMAND ----------

# MAGIC %md ## Return tables

# COMMAND ----------

dbutils.jobs.taskValues.set(key = "tables", value = tables)
