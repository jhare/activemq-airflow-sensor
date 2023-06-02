from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from your_sensor_module import ActiveMQSensor

def check_active_mq_queue():
    message_count_check_method = lambda channel, method, properties, body: (body == b'expected_message')
    sensor = ActiveMQSensor(check_active_mq_queue, queue='your_queue_name', poke_interval=60)

dag = DAG('active_mq_sensor_dag', default_args={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2023-06-01',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
})

check_active_mq_sensor_task = PythonOperator(
    task_id='check_active_mq_sensor',
    python_callable=check_active_mq_sensor,
    dag=dag
)
