-- Databricks notebook source
-- MAGIC %md # Meta Ingestion - Setup

-- COMMAND ----------

-- MAGIC %md ## 1/ Setup databases

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS vr_demo.kafka; -- used for control tables
CREATE DATABASE IF NOT EXISTS vr_demo.kafka_bronze;
CREATE DATABASE IF NOT EXISTS vr_demo.kafka_silver;

-- COMMAND ----------

-- MAGIC %md ## 2/ Setup control table

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS vr_demo.kafka.control (
  catalog STRING NOT NULL COMMENT 'Destination catalog',
  database STRING NOT NULL COMMENT 'Destination database',
  table STRING NOT NULL COMMENT 'Destination table',
  active BOOLEAN COMMENT 'Used for enabling/disabling ingestion for this table',
  topic STRING COMMENT 'Source Kafka topic',
  schema STRING COMMENT 'Used for desearlizing data from Kafka',
  merge_keys STRING COMMENT 'Used for merging data from bronze to silver tables',
  ts_key STRING COMMENT 'Used for sorting and deduplicating data',
  clustering_keys STRING COMMENT 'Used for defining liquid clustering keys (unused yet)',
  CONSTRAINT table_pk PRIMARY KEY(catalog, database, table)
)

-- COMMAND ----------

-- MAGIC %md ## 3/ Example table registration

-- COMMAND ----------

INSERT INTO vr_demo.kafka.control VALUES (
  'vr_demo',
  'kafka',
  'table1',
  true,
  'topic1',
  'struct<action:string,processingTime:string,time:bigint>',
  'eventid',
  'processingTime',
  'time,action'
)
