````markdown
# Consultar o texto por metadados

Este pequeno guia mostra como obter o campo `Texto` da tabela `sinteses` em `base.db` filtrando pelos metadados (ex.: `Genero`, `Assiduidade`, `Pontualidade`, `Participacao`, `Interesse`, `Empenho`, `Dificuldades`).

Colunas disponíveis: `Texto`, `Genero`, `Assiduidade`, `Pontualidade`, `Participacao`, `Interesse`, `Empenho`, `Dificuldades`.

Exemplos rápidos

- Usando o cliente `sqlite3` (CLI):

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='F' AND Assiduidade=1;"
```

- Obter apenas a primeira correspondência:

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='M' AND Empenho=1 LIMIT 1;"
```

- Usando Python (recomendado para filtros dinâmicos e segurança):

```python
import sqlite3

def get_texts(db_path, filters):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    where_clauses = []
    params = []
    for key, value in filters.items():
        where_clauses.append(f"{key} = ?")
        params.append(value)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1"
    sql = f"SELECT Texto FROM sinteses WHERE {where_sql};"

    cur.execute(sql, params)
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

# Exemplo de uso:
texts = get_texts("base.db", {"Genero": "F", "Assiduidade": 1})
for t in texts:
    print(t)
```

Notas

- Use os nomes exatos das colunas ao construir `filters` no Python.
- Para consultas com intervalos ou condições diferentes (ex.: `>=`, `LIKE`), adapte o trecho que gera `where_clauses` e passe os parâmetros adequados.
- O exemplo Python usa parâmetros (`?`) para evitar injeção SQL.

- SQL que concatena todos os metadados numa única descrição (exemplo quando `Genero='F'` e todos os flags = 1):

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='F' AND Assiduidade=1 AND Pontualidade=1 AND Participacao=1 AND Interesse=1 AND Empenho=1 AND Dificuldades=1 LIMIT 1;"
```

# Consultar o texto por metadados

Este pequeno guia mostra como obter o campo `Texto` da tabela `sinteses` em `base.db` filtrando pelos metadados (ex.: `Genero`, `Assiduidade`, `Pontualidade`, `Participacao`, `Interesse`, `Empenho`, `Dificuldades`).

Colunas disponíveis: `Texto`, `Genero`, `Assiduidade`, `Pontualidade`, `Participacao`, `Interesse`, `Empenho`, `Dificuldades`.

Exemplos rápidos

- Usando o cliente `sqlite3` (CLI):

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='F' AND Assiduidade=1;"
```

- Obter apenas a primeira correspondência:

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='M' AND Empenho=1 LIMIT 1;"
```

- Usando Python (recomendado para filtros dinâmicos e segurança):

```python
import sqlite3

def get_texts(db_path, filters):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    where_clauses = []
    params = []
    for key, value in filters.items():
        where_clauses.append(f"{key} = ?")
        params.append(value)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1"
    sql = f"SELECT Texto FROM sinteses WHERE {where_sql};"

    cur.execute(sql, params)
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

# Exemplo de uso:
texts = get_texts("base.db", {"Genero": "F", "Assiduidade": 1})
for t in texts:
    print(t)
```

Notas

- Use os nomes exatos das colunas ao construir `filters` no Python.
- Para consultas com intervalos ou condições diferentes (ex.: `>=`, `LIKE`), adapte o trecho que gera `where_clauses` e passe os parâmetros adequados.
- O exemplo Python usa parâmetros (`?`) para evitar injeção SQL.
