# Make you create your first Kafka topic from kafka directory with the command below
# $ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka-topic3

# This application needs to be run as:
# spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar --master local[*] 03-streamingkafka3.py

import pyspark

# Import StreamingContext which is the main entry point for all streaming functionality.

from pyspark.streaming import StreamingContext

# Import Kafka Utils from the library (jar file) downloaded and specified in while running pyspark shell

from pyspark.streaming.kafka import KafkaUtils

# Create a SparkContext with two execution threads, and StreamingContext with batch interval of 1 second.

sc = pyspark.SparkContext(appName='kafka-streaming')
ssc = StreamingContext(sc, 1)

# Create an input DStream using KafkaUtils.createDirectStream passing the parameters - Spark Streaming Context, topic and broker(s).

kafkaStream = KafkaUtils.createDirectStream(ssc, ['kafka-topic3'], {"metadata.broker.list": 'localhost:9092'})

# This is called Direct approach as it does not involve any receivers unlike the previous approach. This approach ensures stronger end-to-end guarantees. Instead of using receivers to receive data, this approach periodically queries Kafka to get the latest offsets in each topic+partition. Accordingly it defines the offset ranges to process in each batch of messages. When the jobs to process the data are launched, Kafka's simple consumer API is used to read the defined ranges of offsets from Kafka (similar to read files from a file system).

# The data is now handled as a normal RDD in our application to perform word count.

lines = kafkaStream.map(lambda x: x[1])

counts = lines.flatMap(lambda line: line.split(' ')).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)

counts.pprint()

ssc.start()
ssc.awaitTermination()

# We can terminate it by interrupting the kernel (sending Control+C)
ssc.stop()
sc.stop()
