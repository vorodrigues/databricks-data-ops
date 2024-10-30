# Databricks notebook source
target = dbutils.widgets.get("target")

# COMMAND ----------

spark.sql(f'''
  alter table main.vr_mi_{target}_kafka.table1
  set tags ('gold')
''')
