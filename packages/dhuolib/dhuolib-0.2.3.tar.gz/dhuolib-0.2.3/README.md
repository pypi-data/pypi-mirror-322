# DHuolib um produto do DHuo.data

Dhuolib é uma biblioteca projetada para gerenciar o ciclo de vida de modelos de machine learning de forma rápida e eficaz. Com a Dhuolib, é possível implementar e gerenciar ciclos de deploy, controle de versões e gerenciamento de modelos em predição de maneira simples e intuitiva. Este documento tem como objetivo demonstrar essas funcionalidades, facilitando o uso da ferramenta e potencializando sua eficiência.

**==versão: 0.1.9==**

[dhuolib](https://pypi.org/project/dhuolib/)


 ![](https://pypi.org/project/dhuolib/)

# Funcionalidades 

Nesta sessão serão abordadas as principais funcionalidades presentes na dhuolib 

## **Análise Exploratória / Persistencia / Aquisição de Dados**

A análise exploratória de dados envolve a persistência e aquisição de dados de forma eficiente. Utiliza métodos para inserção direta de dados, atualização de tabelas com DataFrames, recuperação de registros e conversão de dados de tabela em DataFrames, facilitando o trabalho dos desenvolvedores na predição de modelos de machine learning.

## **Class: GenericRepository**

A classe GenericRepository simplifica o uso e o acesso ao datalake. Possui diversos métodos, incluindo inserção e busca de dados. Seu objetivo é facilitar o trabalho dos desenvolvedores no processo de predição de modelos de machine learning, fornecendo uma interface simplificada para a interação com os dados.

### **__init__(self, db_connection)**

O repositorio é iniciado passando uma conexão com o banco de dados como parametro no construtor

* **Parameters:**
  * **db_connection**: Uma instancia do DatabaseConnection que provê a conexão e controle de acesso com o datalake

### **create_table_by_dataframe(self, table_name: str, df: pd.DataFrame)**

Cria uma tabela baseada em um dataframe existente

* **Parameters:**
  * **table_name**: Nome da tabela onde o dado será inserido.
  * **dataframe**: Um dataframe representando a tabela e os dados a serem inseridos
* **Returns:**
  * Retorna o numero de itens inseridos na tabela

**Example:**

```python
df = pd.DataFrame({"name": ["example"], "value": [42]})
number_lines = repo.create_table_by_dataframe("my_table", data)
```

### **update_table_by_dataframe(self, table_name: str, df_predict: pd.DataFrame, if_exists: str = "append", is_update_version: bool,  force_replace_delete_itens_in_table**: **bool)**

Atualiza uma tabela adicionando ou substituindo registros usando um DataFrame do pandas.

* **Parâmetros:**
* **table_name ==**obrigatório**==**: O nome da tabela a ser atualizada.
* **dataframe**: Um DataFrame do pandas contendo os registros a serem inseridos.
* **if_exists**: Especifica o comportamento se a tabela já existir, podendo ser replace ou append. O padrão é "append" . 
* **is_update_version:** Faz update  da versão do dado a ser inserido na tabela que vai receber o resultado da predição. A table precisa ter três colunas  ==PREDICT, CREATED_AT e VERSION.==
* **force_replace_delete_itens_in_table: **==WARNING** ==**Esta função também suporta a substituição de valores na tabela. É importante entender que, se essa opção for definida como True, todos os dados da tabela serão substituídos.
* **Example:**

  ```python
  df = pd.DataFrame({"name": ["example"], "value": [42]})
  repo.update_table_by_dataframe("my_table", df)
  ```

**to_dataframe(self, table_name: str , filter_clause: str , list_columns: list )**

Converte os resultados da consulta em um DataFrame do pandas.

* **Parâmetros:**
  * **table_name ==**obrigatório**==**: O nome da tabela a ser consultada.
  * **filter_clause**: Uma cláusula de filtro opcional para aplicar à consulta.
  * **list_columns**: Uma lista opcional de colunas a serem incluídas na consulta.
* **Retorna:**
  * Um DataFrame do pandas contendo os resultados da consulta.
* **Exemplo:**


```python
df = repo.to_dataframe("my_table", filter_clause="value > 10", list_columns=["name", "value"])
```


### **Criação de Experimentos, Ciclo de vida do modelo e Predição**

## **Class: DhuolibExperimentClient**

DhuolibExperimentClient  interage com o serviço Dhuolib para gerenciar experimentos, executar modelos, criar modelos e fazer previsões. Inclui métodos para criar e executar experimentos, criar modelos e fazer previsões em lote.

### **__init__(self, service_uri: str, token: str)**

Inicializa o cliente com um endpoint de serviço.

* **Parâmetros:**
  * **service_uri ==**obrigatório**==**: O uri da api de serviço Dhuolib
  * **token ==**obrigatório**==**:  token de autenticação
* **Lança:**
  * ValueError: Se service_uri ou token não for fornecido.

### **create_experiment(self, experiment_name: str, experiment_tags: dict) -> dict**

Cria um novo experimento com o nome e tags especificados. Se o experimento já existir com o mesmo nome ele retorna um dict com as informações do modelo.

* **Parâmetros:**
  * **experiment_name ==**obrigatório**==**: O nome do experimento.
  * **experiment_tags**: Dicionário opcional de tags para o experimento.
* **Retorna:**
  * Um dicionário contendo os detalhes do experimento criado ou uma mensagem de erro.

**Exemplo:**

```python
experiment_response = dhuolib_client.create_experiment(
        experiment_name="iris-classification", experiment_tags={"tag": "iris"}
    )
```

### **execute_run_for_experiment(self, type_model: str, experiment_name: str, modelpkl_path: str, requirements_path:str, tags: dict) -> dict**

Executa um experimento com o modelo e requisitos especificados.

* **Parâmetros:**
  * **type_model ==**obrigatório**==**: O tipo do modelo.
  * **experiment_name ==**obrigatório**==**: O nome do  experimento.
  * **modelpkl_path ==**obrigatório**==**: O caminho para o arquivo pickle do modelo.
  * **requirements_path ==**obrigatório**==**: O caminho para o arquivo de requisitos.
  * **tags:** O parametro tags é utilizado para facilitar o processo de busca de execuções para um determinado experimento
* **Retorna:**
  * Um **dict** com os seguintes valores:
    * **run_id** : id de execução do run 
    * **model_uri**:  model_uri que sera utilizado para criar um modelo para esse run executado
* **Exemplo:**

  ```python
    experiment_run = dhuolib_client.execute_run_for_experiment(
          type_model="lightgbm",
          experiment_name="iris-classification",
          tags={"version": "v2", "priority": "P2"},
          modelpkl_path="{path}/iris.pkl",
          requirements_path="{path}/requirements.txt"
      )
  ```

### **create_model(self, model_params: dict) -> dict**

Cria um novo modelo com os parâmetros especificados.

* **Parâmetros:**
  * **modelname ==**obrigatório**==:  Nome que sera dado para identificar o modelo**
  * **stage ==**obrigatório** ==**:  O estado do modelo podendo ser **STAGING** e **PRODUCTION**
  * **run_id ==**obrigatório**==**: O run id  da execução do experimento 
  * **model_uri==**obrigatório**==**: O model path da execução do experimento 
  * **tags:**  O parametro tags é utilizado para facilitar o processo de busca de modelos 
* **Retorna:**
  * Um dicionário contendo os detalhes do modelo criado ou uma mensagem de erro.
    * **model_version**:  O numero que identifica a versão do modelo
    * **model_version_name**: O nome dessa versão do modelo
    * **run_id**: O identificador unico da execução do experimento para um pkl especifico
    * **previous_stage**: O estado anterior do modelo 
    * **current_stage**: O estado atual do modelo
    * **last_updated_timestamp:** data demontrando o tempo da ultima alteração do modelo

**Exemplo:**

```python
dhuolib_client.create_model(modelname="iris-classification",
                           stage="Production",
                           run_id=experiment_run["run_id"],
                           model_uri=experiment_run["model_uri"],
                           tags={"type_model": "lightgbm"})
```

### **search_experiments(filter_string: str , max_results: int = 10, page_token: str ) -> dict:**

### Busca por experimentos atraves de um filtro passada por parametro

* **Parâmetros**:
  * **max_results:**  Quantidade de experimentos que são retornados . Valor default é 10
  * **page_token:**  Token code que deve ser passado para buscar novos valores paginados
  * **filter_string**: **==**obrigatório**==** String de consulta de filtro (por exemplo, "name = 'my_experiment'"), por padrão, busca todos os experimentos. Os seguintes identificadores, comparadores e operadores lógicos são suportados.
    * **Identificadores:**
      * **name:** Nome do experimento.
      * **creation_time:** Hora de criação do experimento.
      * **last_update_time:** Hora da última atualização do experimento.
      * **tags.<tag_key>:** Tag do experimento. Se tag_key contiver espaços, deve ser envolvida por crases (por exemplo, "tags.`extra key`").

      **Comparadores para atributos de string e tags:**
      * **=:** Igual a.
      * **!=:** Diferente de.
      * **LIKE:** Correspondência de padrão sensível a maiúsculas e minúsculas.
      * **ILIKE:** Correspondência de padrão insensível a maiúsculas e minúsculas.

      **Comparadores para atributos numéricos:**
      * **=:** Igual a.
      * **!=:** Diferente de.
      * **<:** Menor que.
      * **<=:** Menor ou igual a.
      * **>:** Maior que.
      * **>=:** Maior ou igual a.

      **Operadores Lógicos:**
      * **AND:** Combina duas subconsultas e retorna True se ambas forem True.
* **Retorna uma lista de experimentos com os seguintes parâmetros:**
  * **experiment_id:** Identificador do experimento.
  * **experiment_name:** Nome do experimento.
  * **lifecycle_stage:** Estágio do ciclo de vida do experimento.
  * **creation_time:** Hora de criação do experimento.
  * **last_update_time:** Hora da última atualização do experimento.
  * **tags:** Tags associadas ao experimento.

```python
 results = dhuolib_client.search_experiments(
     filter_string="tags.version LIKE 'v%'", max_results=10
    )

 results = dhuolib_client.search_experiments(
     filter_string="tags.version='v1'", max_results=2
 )

 print("All Experiments:")
 for result in results["experiments"]:
     print(result)
```

### **search_runs(filter_string: str, max_results: int = 10, page_token: str, experiment_name: str) -> dict:**

### Busca por execuções através de um filtro passado por parâmetro. Por padrão filter_string=* busca todos os runs.

* **Parâmetros:**
  * **max_results:** Número máximo de resultados a serem retornados.
  * **page_token:** Token code que deve ser passado para buscar novos valores paginados.
  * **experiment_name:** Nome do experimento para filtrar as execuções.
  * **filter_string ==**obrigatório**==**:
    * **Comparadores para atributos de string e tags:**
      * **=:** Igual a.
      * **!=:** Diferente de.
      * **LIKE:** Correspondência de padrão sensível a maiúsculas e minúsculas.
      * **ILIKE:** Correspondência de padrão insensível a maiúsculas e minúsculas.

      **Comparadores para atributos numéricos:**
      * **=:** Igual a.
      * **!=:** Diferente de.
      * **<:** Menor que.
      * **<=:** Menor ou igual a.
      * **>:** Maior que.
      * **>=:** Maior ou igual a.

      **Operadores Lógicos:**
      * **AND:** Combina duas subconsultas e retorna True se ambas forem True.
* **Retorna uma lista de execuções com os seguintes parâmetros:**
  * **run_id:**  Identificador da execução.
  * **experiment_id:**  Identificador do experimento.
  * **status:**  Status da execução.
  * **start_time:**  Hora de início da execução.
  * **end_time:**  Hora de término da execução.
  * **metrics:**  Métricas da execução.
  * **params:**  Parâmetros da execução.
  * **tags:**  Tags da execução.

```python
 dholib_client = DhuolibExperimentMLClient(service_uri)
 print("Runs:")
 results = dhuolib_client.search_runs(
        experiment_name="wine-regression",
        filter_string="tags.type_model='keras'",
        max_results=2,
    )
 for result in results["runs"]:
     print(result)
```

### **search_models(filter_string: str , max_results: int = 10, page_token: str) -> dict:**

### Busca por modelos através de um filtro passado por parâmetro

* **Parâmetros:**
  * **max_results:** Número máximo de resultados a serem retornados.
  * **page_token:** Token da página para busca paginada.
  * **filter_string ==**obrigatório**==**:  String de consulta de filtro (por exemplo, "name = 'a_model_name' and tag.key = 'value1'"), por padrão, busca todas as versões de modelos. Os seguintes identificadores, comparadores e operadores lógicos são suportados.

    **Identificadores:**
    * **name:** Nome do modelo.
    * **source_path:** Caminho da fonte da versão do modelo.
    * **run_id:** ID da execução do mlflow que gerou a versão do modelo.
    * **tags.<tag_key>:** Tag da versão do modelo. Se tag_key contiver espaços, deve ser envolvida por crases (por exemplo, "tags.`extra key`").

    **Comparadores:**
    * **=:** Igual a.
    * **!=:** Diferente de.
    * **LIKE:** Correspondência de padrão sensível a maiúsculas e minúsculas.
    * **ILIKE:** Correspondência de padrão insensível a maiúsculas e minúsculas.
    * **IN:** Em uma lista de valores. Apenas o identificador run_id suporta o comparador IN.

    **Operadores Lógicos:**
    * **AND:** Combina duas subconsultas e retorna True se ambas forem True.
* **Retorna uma lista de modelos com os seguintes parâmetros:**
  * **model_id:** Identificador do modelo.
  * **model_name:** Nome do modelo.
  * **creation_time:** Hora de criação do modelo.
  * **last_update_time:** Hora da última atualização do modelo.
  * **tags:** Tags associadas ao modelo.

```python
results = dhuolib_client.search_models(
        filter_string="tags.version='v1'", max_results=2
    )
results = dhuolib_client.search_models(max_results=2, filter_string="name = 'iris-classification'")
```

### **transition_model(self, model_name: str, version: str, stage: str) -> dict:**

Faz a transição dos modelos para diferentes ambientes  por padrão o valor é None. Existem outros ambientes tambem **Production, Staging ou Archived.**

* **Parâmetros**:
  * **model_name ==**obrigatório**==**: O nome do modelo
  * **version ==**obrigatório**==**: A versão do modelo que se deseja modar de ambiente
  * **stage ==**obrigatório**==**: Qual ambiente que se quer transicionar
* **Retorna**:
  * Uma messagem  indicando que o modelo foi transicionado ou uma mensagem de erro.

### **download_pkl(self, batch_params: dict) -> model**

Faz o download de um determinado pkl.

* **Parâmetros:**
  * **batch_params ==obrigatório==**: Um dicionário contendo os parâmetros do modelo ou run.
* **Retorna:**
  * O load do pkl que foi baixado do servidor.

**Exemplo:**

```python
batch_params = {
        "modelname": "iris-classification-lightgbm",
        "stage": "Production",
        "experiment_name": "iris-classification",
        "type_model": "lightgbm",
        "run_id": "",
        "batch_model_dir": "iris.pkl",
}
response = client.download_pkl(batch_params)
```

### **prediction_batch_with_dataframe(self, batch_params: dict, dataframe: pd.DataFrame) -> dict**

Faz uma previsão em lote usando um DataFrame do pandas.

* **Parâmetros:**
  * **batch_params ==**obrigatório**==**: Um dicionário contendo os parâmetros da previsão em lote.
  * **df ==**obrigatório**==**: Um DataFrame do pandas contendo os dados para a previsão.
* **Retorna:**
  * Um dicionário contendo os resultados da previsão em lote ou uma mensagem de erro.

**Exemplo:**

```python
batch_params = {
        "modelname": "iris-classification-lightgbm",
        "stage": "Production",
        "experiment_name": "iris-classification",
        "type_model": "lightgbm",
        "run_id": "",
        "batch_model_dir": "iris.pkl",
}
response = client.prediction_batch_with_dataframe(batch_params, dataframe)
```

## **Exemplo de Uso**

```python
import pickle
import lightgbm as lgb

from dhuolib.clients.experiment import DhuolibExperimentMLClient
from dhuolib.repository import DatabaseConnection, GenericRepository


def get_repository(config_file_name):
    if not config_file_name:
        raise ValueError("config_file_name is required")

    db = DatabaseConnection(config_file_name=config_file_name)
    repository = GenericRepository(db_connection=db)

    return repository


def train():
    service_uri = "https://dhuo-data-api-data-service-stg.br.engineering"

    dhuolib_client = DhuolibExperimentMLClient(
        service_uri=service_uri,
        token="{token}"
    )
    repository = get_repository(
        config_file_name="{path}/config/database.json"
    )
    df_iris_train = repository.to_dataframe(table_name="IRIS_TRAIN")

    print(df_iris_train.columns)

    X = df_iris_train[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = df_iris_train["class"]
    clf = lgb.LGBMClassifier()
    clf.fit(X, y)
    with open("iris.pkl", "wb") as f:
        pickle.dump(clf, f)

    dhuolib_client.create_experiment(
        experiment_name="lightgbm-iris", experiment_tags={"tag": "iris"}
    )

    experiment_run = dhuolib_client.execute_run_for_experiment(
        type_model="lightgbm",
        experiment_name="lightgbm-iris",
        tags={"version": "v2", "priority": "P2"},
        modelpkl_path="{path}/iris.pkl",
        requirements_path="{path}/requirements.txt",
    )
    print(experiment_run)

    result = dhuolib_client.create_model(
        modelname="iris-classification",
        stage="Production",
        run_id=experiment_run["run_id"],
        model_uri=experiment_run["model_uri"],
        tags={"type_model": "lightgbm"},
    )
    print(result)


if __name__ == "__main__":
    train()
```

## **Class: DhuolibPlatformClient**

DhuolibPlatformClient interage com o serviço Dhuolib para gerenciar projetos em lote, implantar scripts, verificar o status do pipeline, criar clusters e executar pipelines em lote.

### **__init__(self, service_uri: str,  project_name:str)**

Inicializa o cliente com um endpoint de serviço e um nome de projeto opcional.

* **Parâmetros:**
  * **service_endpoint==**obrigatório**==**: O endpoint do serviço Dhuolib.
  * **project_name**: Nome opcional do projeto.
  * **token ==**obrigatório**==**:  token de autenticação
* **Lança:**
  * ValueError:  Se o projeto já existir.
  * ConnectionError: Se houver um erro de conexão.

### **create_batch_project(self, project_name: str)**

Cria um novo projeto em lote com o nome especificado.

* **Parâmetros:**
  * **project_name ==**obrigatório**==**: O nome do projeto.
* **Retorna:**
  * Um dicionário contendo os detalhes do projeto criado ou uma mensagem de erro.
* **Lança:**
  * `ValueError`: Se o projeto já existir.
  * `ConnectionError`: Se houver um erro de conexão.
* **Exemplo:**

  ```python
  response = dhuolib_platform.create_batch_project("MeuProjeto")
  ```

### **deploy_batch_project(self, script_filename: str, requirements_filename: str)**

Implanta um projeto em lote com o script e requisitos especificados.

* **Parâmetros:**
  * **script_filename ==**obrigatório**==**: O nome do arquivo do script.
  * **project_name ==**Não é obrigatório se o project_name for passado no construtor**==**: O nome do projeto.
  * **requirements_filename ==**obrigatório**==**: O nome do arquivo de requisitos.
* **Retorna:**
  * A resposta do serviço Dhuolib ou uma mensagem de erro.
* **Lança:**
  * ValueError: Se project_name, script_filename ou requirements_filename não foram fornecidos
  * FileNotFoundError: Se os arquivos especificados não forem encontrados.

**Exemplo:**

```python
 response = dhuolib_platform.deploy_batch_project(
        script_filename="{path}/script.py",
        requirements_filename="{path}/requirements.txt"
    )
```

### **pipeline_status_report(self)**

Gera um relatório de status do pipeline para o projeto em lote.

* **Parâmetros:**
  * **project_name ==**Não é obrigatório se o project_name for passado no construtor**==**: O nome do projeto.
* **Retorna:**
  * Uma lista de dicionários contendo a data, etapa e status de cada log do pipeline.
* **Lança:**
  * ValueError: Se project_name não for fornecido
* **Exemplo:**

  ```python
  status_report = dhuolib_platform.pipeline_status_report()
  ```

### **create_cluster(self, cluster_size: int)**

Cria um cluster com o tamanho especificado para o projeto em lote.

* **Parâmetros:**
  * **cluster_size**: O tamanho do cluster (1, 2 ou 3).
  * **project_name ==**Não é obrigatório se o project_name for passado no construtor**==**: O nome do projeto.
* **Retorna:**
  * A resposta do serviço Dhuolib.
* **Lança:**
  * ValueError: Se project_name ou cluster_size não forem fornecidos ou se cluster_size não for 1, 2 ou 3.
* **Exemplo:**

  ```python
  response = dhuolib_platform.create_cluster(2)
  ```

### **batch_run(self)**

Executa o pipeline em lote para o projeto.

* **Parâmetros:**
  * **project_name ==**Não é obrigatório se o project_name for passado no construtor**==**: O nome do projeto.
* **Retorna:**
  * A resposta do serviço Dhuolib.
* **Lança:**
  * ValueError: Se project_name não for fornecido.
* **Exemplo:**

  ```python
  response = dhuolib_platform.batch_run()
  ```

**schedule_batch_run(self, project_name: str, schedule_interval: str):**

Cria o agendamento de execução de um processamento em batch

* **Parâmetros**:
  * **project_name ==**obrigatório**==**: O nome do projeto que foi utilizado anteriormente
  * **schedule_interval ==**obrigatório**==**: O padrão de schedule a ser atribuido para o projeto ==schedule_interval="*/5 * * * *"==
* **Lança:**
  * **ValueError**: Se o project_name não for fornecido.


* **Retorna:**
  * Retorna um json com uma mensagem indicando se a schedule foi ou não criada
* **Exemplo**:

```python
dhuolib_platform.schedule_batch_run(
            project_name="lightgbm-iris",
            schedule_interval="*/5 * * * *"
        )
```

### **remove_schedule(self, project_name: str):**

Deleta o agendamento de execução de um determinado projeto

* **Parâmetros**:
  * **project_name ==**obrigatório**==**: O nome do projeto que foi utilizado anteriormente
* **Lança:**
  * **ValueError**: Se o project_name não for fornecido.


* **Retorna:**
  * Retorna um json com uma mensagem indicando se a schedule foi ou não criada

```python
dhuolib_platform.remove_schedule(project_name="lightgbm-iris")
```


```
print(dholib_platform.schedule_batch_run(project_name="lightgbm-iris-stg", schedule_interval="*/5 * * * *"))
```

