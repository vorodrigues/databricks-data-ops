from metaingestion.kafka.batch import *

def MetaIngestion(conf, spark):
  
  source = conf.source
  
  if source == "kafka_batch":
    KafkaBatchIngestion(conf, spark)
  else:
    raise Exception('ERROR: Source not found')