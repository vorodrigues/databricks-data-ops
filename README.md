# Databricks Data Ops

O projeto 'databricks_data_ops' foi gerado usando o template `default-python` do [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html).
```
databricks bundle init default-python --profile <nome>
```

## Como usar

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
   * Aguarde odeploy dos ativos e a execução dos testes na `STAGING`

1. **Aprove** o PR em caso de sucesso
   * O processo de CD será iniciado automaticamente
   * Aguarde o deploy dos ativos em `PROD`

## Notas

1. Em `PROD`, recomendamos:
   * Usar um *service principal* ao invés de um usuário pessoal
   * Usar um diretório específico para o projeto (ao invés de um diretório pessoal)
   * No `databricks.yml`, usem o `mode: production`. Dessa forma, essas boas práticas serão validadas automaticamente durante o processo de CI

1. Recomendamos usar um *service principal* no processo de CI/CD

1. No momento, os testes unitários estão desabilitados. Caso necessário, configure o Databricks Connect na workflow de CI ou altere os testes para usar uma sessão local do Spark

