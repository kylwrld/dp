# REST API - Nerve

REST API feita para o trabalho de final de ano, projeto integrador, do terceiro ano do ensino médio integrado ao técnico do SENAC.

#### Retorna todos os itens de um usuário

```http
  GET /api/task/
```

| Headers     | Descrição                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Obrigatório**. Token JWT de autorização do usuário |

#### Cria um item para um usuário

```http
  POST /api/task/
```

| Headers     | Descrição                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Obrigatório**. Token JWT de autorização do usuário |

#### Atualiza um item

```http
  PUT /api/task/${id}/
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `string` | **Obrigatório**. O ID do item que você quer |

| Headers     | Descrição                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Obrigatório**. Token JWT de autorização do usuário |

#### Deleta um item

```http
  DELETE /api/task/${id}/
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `string` | **Obrigatório**. O ID do item que você quer |

| Headers     | Descrição                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Obrigatório**. Token JWT de autorização do usuário |
