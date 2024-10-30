# Databricks notebook source
target = dbutils.widgets.get("target")

# COMMAND ----------

spark.sql(f'''
  alter table main.vr_mi_{target}_kafka_silver.table1
  set tags ('gold')
''')
