from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'kanishk',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'ecommerce_pipeline_dag',
    default_args=default_args,
    description='Run Spark streaming and Kafka producer',
    schedule_interval=None,
    catchup=False,
)

# Spark Stream (inside Spark container)
start_stream = BashOperator(
    task_id='start_spark_stream',
    bash_command="""
    docker exec spark spark-submit \
      --master "local[*]" \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,\
org.apache.kafka:kafka-clients:3.2.0,\
org.xerial.snappy:snappy-java:1.1.8.4,\
org.apache.commons:commons-pool2:2.11.1,\
org.lz4:lz4-java:1.7.1,\
io.dropwizard.metrics:metrics-core:4.1.12.1 \
      /opt/spark_jobs/stream_orders.py
    """,
    dag=dag,
)

# Optional: wait to make sure stream is ready
wait_for_stream = BashOperator(
    task_id='wait_for_stream',
    bash_command='sleep 20',
    dag=dag,
)

# Kafka Producer
start_producer = BashOperator(
    task_id='start_kafka_producer',
    bash_command='python3 /opt/airflow/ecommerce_pipeline/kafka_producer/send_orders.py',
    dag=dag,
)

start_stream >> wait_for_stream >> start_producer