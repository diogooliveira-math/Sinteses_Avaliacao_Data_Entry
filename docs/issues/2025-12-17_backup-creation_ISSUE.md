# 2025-12-17: Falha na criação de backup de `base.json`

## 1. Problem Summary

Ao tentar salvar uma edição de um texto, o fluxo cancela porque a função de backup retorna `False` e o programa imprime:

```
Satisfeito com a edição? (s/n): s
⚠ Aviso: Não foi possível criar backup. Operação cancelada.
```

## 2. Error Message

O aviso acima é exibido quando `backup_json()` falha. Não há stacktrace guardado no output original.

## 3. Root Cause Analysis

A implementação anterior fazia leitura/escrita manuais do ficheiro (`open/read` e `open/write`) o que, em alguns cenários (locks, permissões, diferenças de encoding ou caminhos), pode falhar. A função também não apresentava uma mensagem clara sobre a inexistência de `base.json`.

Possíveis causas:
- `base.json` não está no caminho esperado relativo ao executável/script
- A operação de I/O falha por lock/perm/encoding

## 4. Reproduction Steps

1. Execute a funcionalidade de edição normalmente (por exemplo, via `python cli.py`).
2. Aceite a edição (`s`) para forçar a criação de backup antes da gravação.
3. Observar a mensagem de aviso e operação cancelada.

## 5. Impact

- O utilizador perde a capacidade de guardar edições quando o backup falha.
- Fluxo de edição fica menos tolerante a erros.

## 6. Testing Evidence

- Há um teste manual (`test_edit_feature.py`) que chama `backup_json()`; em ambientes onde a cópia falhava o teste imprimia falha.

## 7. Solution Plan

Substituir a cópia manual por `shutil.copy2()` para uma operação de cópia mais robusta e adicionar uma mensagem clara quando `base.json` não existir. Atualizar documentação e adicionar resumo de fix.

Files to change:
- `cli.py` (backup_json)
