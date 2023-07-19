from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import pandas as pd
import mysql.connector
import shutil
import logging
from airflow.operators.dagrun_operator import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 17),
    'email': ['clebersguimaraes@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'catchup': False
}

def extract_mysql_data():
    try:
        conn = mysql.connector.connect(
            host='192.168.2.5',
            port=3306,
            database='adventureworks',
            user='root',
            password='rio@123'
        )

        cur = conn.cursor()

        query = "SELECT * FROM purchaseorderdetail"  # Atualize o nome da tabela conforme necessário
        cur.execute(query)

        data = cur.fetchall()
        header = [i[0] for i in cur.description]  # Obter os nomes das colunas

        cur.close()
        conn.close()

        # Crie um DataFrame com os dados e salve-o como CSV
        df = pd.DataFrame(data, columns=header)
        
        # Gere um nome de arquivo com a data e hora atual
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f'/home/dataset/data_pipeline_db_{current_datetime}.csv'
        df.to_csv(csv_path, index=False)

        logging.info("Dados extraídos do banco de dados e salvos como CSV")
    except Exception as e:
        logging.error("Erro ao conectar ao banco de dados: %s", str(e))
        # Aqui você pode adicionar ações adicionais, como enviar uma notificação ou registrar o erro em algum lugar.

def copy_csv_file():
    source_file = '/home/dados/order_details.csv'
    
    # Gere um nome de arquivo com a data e hora atual
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_file = f'/home/dataset/data_pipeline_csv_{current_datetime}.csv'

    # Copiar o arquivo CSV para o destino
    shutil.copyfile(source_file, destination_file)

    logging.info("Arquivo CSV copiado para o diretório de destino")

with DAG('data_pipeline', default_args=default_args, schedule_interval='30 * * * *') as dag:
    task_extract_db_data = PythonOperator(
        task_id='extract_data_from_database',
        python_callable=extract_mysql_data,
        provide_context=True,
        retries=0
    )

    task_copy_csv_file = PythonOperator(
        task_id='copy_csv_file',
        python_callable=copy_csv_file,
        provide_context=True,
        retries=0
    )
    
    task_extract_db_data >> task_copy_csv_file
