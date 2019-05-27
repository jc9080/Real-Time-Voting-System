import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.0 pyspark-shell'

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from kafka import KafkaProducer

import json

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        print(key_bytes, value_bytes)
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

def send_to_kafka_aggreg_vote(partition):
    kafka_producer = connect_kafka_producer()
    for record in partition:
        print('HERE: ', record)
        formatted_record = {
            record[0] : record[1]
        }
        publish_message(kafka_producer, 'aggregate-votes', 'agvote', json.dumps(formatted_record))
    if kafka_producer is not None:
        kafka_producer.close()

app_name = 'spark-streaming'
batchInterval = 30
# Integrate with Spark Streaming
sc = SparkContext(appName=app_name)
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, batchInterval)
topic_name = 'unverified-votes'
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', app_name, {topic_name:1})
parsed = kafkaStream.map(lambda v: json.loads(v[1]))
parsed.map(lambda x:'Votes in this batch: %s' % x).pprint()

pres_votes = parsed.map(lambda x: x['president']).countByValue()
pres_votes.pprint()
pres_votes.foreachRDD(lambda rdd: rdd.foreachPartition(send_to_kafka_aggreg_vote))

vp_votes = parsed.map(lambda x: x['vice-president']).countByValue()
vp_votes.pprint()
vp_votes.foreachRDD(lambda rdd: rdd.foreachPartition(send_to_kafka_aggreg_vote))

ssc.start()
ssc.awaitTermination()

# record = ('a', 5)
# kafka_producer = connect_kafka_producer()
# publish_message(kafka_producer, 'aggregate-votes', 'vote', json.dumps(record))
# if kafka_producer is not None:
#     kafka_producer.close()