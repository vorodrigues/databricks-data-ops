# Databricks Data Ops

O projeto 'databricks-data-ops' foi gerado usando o template `default-python` do [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html).
```
databricks bundle init default-python --profile <nome>
```

## Introdução

Este repositório fornece um exemplo funcional de Data Ops baseado em boas práticas da Databricks.

Para isso, consideramos um job simples com três tarefas, que fornecem referências para os seguintes cenários: 
* Execução de notebooks
* Execução de pipelines do DLT
* Execução de módulos Python customizados (wheel)

## Como usar

![Fluxograma](https://github.com/vorodrigues/databricks-data-ops/blob/0d253c1baf76592087850ec2ae6de6e33f2a952c/img/data-ops.png?raw=true)

1. **Clone** este repositório na sua ferramenta de versionamento de código

1. Crie uma **branch** de desenvolvimento / feature

1. Crie os **secrets** abaixo na sua ferramenta de automação
   * `STAGING_WORKSPACE_TOKEN`
   * `PROD_WORKSPACE_TOKEN`

1. Crie um **Databricks Repo** a partir da branch de desenvolvimento / feature

1. **Customize** de acordo com o seu projeto

1. Faça o **commit** das alterações

1. Crie um **pull request**
   * O processo de CI será iniciado automaticamente
   * Aguarde o deploy dos ativos e a execução dos testes na `STAGING`

1. **Aprove** o PR em caso de sucesso
   * O processo de CD será iniciado automaticamente
   * Aguarde o deploy dos ativos em `PROD`

## Estrutura do Projeto

```
├── .github/workflows                        # Definição dos pipelines de CI/CD
|     ├── ci_lint_cicd_workflows.yml
|     ├── databricks_data_ops_cd.yml
|     └── databricks_data_ops_ci.yml
├── resources                                # Definição dos jobs, pipelines, clusters...
|     ├── databricks_data_ops_job.yml
|     └── databricks_data_ops_pipeline.yml
├── src                                      # Código do projeto
|     ├── databricks_data_ops                # Exemplo de módulo customizado
|     |     └── main.py
|     ├── dlt_pipeline.ipynb
|     └── notebook.ipynb
├── tests                                    # Código dos testes unitários
|     ├── main_test.py
|     └── requirements-test.txt
├── databricks.yml                           # Definição dos ambientes de desenvolvimento
├── pytest.ini                               # Configuração do pytest
├── requirements-dev.txt                     # Dependências do projeto
└── setup.py                                 # Configuração do setuptools
```

## Notas

1. Em `PROD`, recomendamos:
   * Usar um *service principal* ao invés de um usuário pessoal
   * Usar um diretório específico para o projeto (ao invés de um diretório pessoal)
   * No `databricks.yml`, usem o `mode: production`. Dessa forma, essas boas práticas serão validadas automaticamente durante o processo de CI

1. Recomendamos usar um *service principal* no processo de CI/CD

1. No momento, os testes unitários estão desabilitados. Caso necessário, configure o Databricks Connect na workflow de CI ou altere os testes para usar uma sessão local do Spark

