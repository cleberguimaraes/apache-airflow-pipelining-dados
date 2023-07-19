Pipelining de dados com Apache Airflow

Este projeto é um exemplo de um Data Pipeline utilizando o Apache Airflow para extrair dados de uma tabela MySQL em um servidor remoto e copiar um arquivo CSV de outro servidor para um diretório de destino. O Airflow é uma plataforma de orquestração de fluxo de trabalho de código aberto, que permite agendar, monitorar e gerenciar fluxos de trabalho complexos.

Pré-requisitos

Antes de testar o projeto, certifique-se de ter o seguinte instalado em seu ambiente:

- Python (versão 3.6 ou superior)
- Apache Airflow (você pode instalar o Airflow seguindo as instruções do site oficial)

Configuração

1. Baixe o arquivo `data_pipeline.py` deste repositório.

2. Copie o arquivo `data_pipeline.py` para o diretório de DAGs do Airflow. O caminho típico para o diretório de DAGs é `/path/to/airflow/dags`. Certifique-se de que o arquivo esteja no diretório correto para que o Airflow possa reconhecê-lo e executá-lo.

3. No arquivo `data_pipeline.py`, verifique e atualize os parâmetros de conexão do banco de dados MySQL. Certifique-se de que o host, porta, usuário e senha estejam corretos. No exemplo abaixo, o servidor do banco de dados é `192.168.2.5`, mas você deve substituir pelo endereço do seu servidor:

   host='000.000.0.0',
   port=3306,
   database='adventureworks',
   user='airflow',
   password='*******'

4. Verifique se o usuário do Airflow tem permissões adequadas no banco de dados para estabelecer a conexão.

5. Defina o diretório de origem do arquivo CSV no servidor remoto no arquivo `data_pipeline.py`, atualizando a variável `source_file`. No exemplo abaixo, o arquivo `order_details.csv` está localizado em `/home/dados` no servidor de origem, mas você deve substituir pelo caminho correto:

   source_file = '/home/dados/order_details.csv'

6. Verifique se o usuário do Airflow tem permissões adequadas no servidor de origem para acessar o diretório e o arquivo.

7. Defina o diretório de destino para a cópia do arquivo CSV no arquivo `data_pipeline.py`, atualizando a variável `destination_file`. O código já foi atualizado para incluir a data e hora atual no nome do arquivo, evitando a sobregravação de arquivos:

   current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
   destination_file = f'/home/dataset/data_pipeline_csv_{current_datetime}.csv'

8. Verifique se o usuário do Airflow tem permissões adequadas no servidor de destino para gravar o arquivo no diretório especificado.

Além de garantir que o usuário do Airflow tenha permissões adequadas para estabelecer a conexão com o banco de dados, é igualmente importante verificar e configurar as permissões nos servidores de arquivo e no servidor onde as informações serão salvas. A seguir, detalharemos as etapas para verificar e ajustar essas permissões:

Servidor do Banco de Dados (192.168.00.0)

1. Verifique se o usuário do Airflow tem as permissões corretas para acessar o banco de dados `adventureworks` no servidor remoto `192.168.2.5`. O usuário deve ter privilégios para executar consultas (SELECT) na tabela `purchaseorderdetail`.

2. Certifique-se de que o servidor MySQL permita conexões de clientes remotos. Verifique as configurações no arquivo de configuração do MySQL (normalmente `my.cnf` ou `mysql.conf.d/mysqld.cnf`) e confirme que o parâmetro `bind-address` não está configurado para aceitar apenas conexões locais. Se necessário, ajuste-o para aceitar conexões de outros endereços IP.

Servidor de Origem (onde está o arquivo CSV)

1. No servidor onde o arquivo CSV `order_details.csv` está localizado (por exemplo, `/home/dados/order_details.csv`), verifique se o usuário do Airflow tem permissões de leitura para acessar o diretório e o arquivo. O usuário deve ter permissões para ler o arquivo CSV.

Servidor de Destino (onde as informações serão salvas)

1. No servidor onde os arquivos CSV gerados pelo Data Pipeline serão salvos (por exemplo, `/home/dataset`), verifique se o usuário do Airflow tem permissões de gravação para acessar o diretório de destino. O usuário deve ter permissões para gravar os arquivos CSV gerados pelo Data Pipeline no diretório `/home/dataset`.

2. Garanta que o diretório de destino exista e tenha as permissões adequadas para permitir a gravação de arquivos.

Observações Finais

As permissões adequadas nos servidores são fundamentais para garantir a execução das tarefas no airflow. Certifique-se de realizar as verificações e ajustes necessários em cada servidor, conforme descrito acima, antes de executar a DAG.

Execução

1. Inicie o Apache Airflow:

   airflow webserver -p 8080

2. Abra o Airflow em seu navegador em http://localhost:8080.

3. Ative a DAG `data_pipeline` clicando no botão "ON" ao lado do nome da DAG.

4. Clique em "Trigger DAG" para iniciar a execução do Data Pipeline.

Verificação

Após a execução da DAG, verifique se os arquivos `data_pipeline_csv.csv` e `data_pipeline_db.csv` foram gerados no diretório `/home/dataset`. Os arquivos CSV terão um sufixo de data e hora atual, conforme configurado no passo anterior, para evitar a sobregravação de arquivos.

Conclusão

Neste guia, fornecemos instruções detalhadas para configurar e executar o Data Pipeline com o Apache Airflow. Ao seguir as etapas descritas acima, você estará preparado para extrair dados de um banco de dados remoto, copiar arquivos CSV de um servidor de origem e salvar as informações em um servidor de destino. A configuração de permissões adequadas nos servidores é fundamental para o funcionamento correto do Data Pipeline. Verificar as permissões do usuário do Airflow no servidor do banco de dados, no servidor de origem (onde está o arquivo CSV) e no servidor de destino (onde as informações serão salvas) é essencial para garantir que todas as etapas do pipeline ocorram sem problemas.
