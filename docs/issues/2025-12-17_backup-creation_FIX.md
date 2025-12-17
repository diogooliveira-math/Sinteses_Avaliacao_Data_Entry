# 2025-12-17: Fix — Falha na criação de backup de `base.json`

## Problem

Ao tentar guardar edições, a operação abortava quando a função de backup retornava `False`.

## Root Cause

Uso de leitura/escrita manual do ficheiro para criar o backup que, em alguns cenários, falhava silenciosamente; falta de mensagem clara quando `base.json` não existe.

## Solution Implemented

- Substituída a lógica de leitura/escrita por `shutil.copy2()` para realizar uma cópia mais robusta e segura.
- Mensagem clara adicionada quando `base.json` não é encontrado.

## Code Changes

- `cli.py`: `backup_json()` agora usa `shutil.copy2()` e imprime uma mensagem explícita se `base.json` estiver ausente.

```diff
--- a/cli.py
+++ b/cli.py
@@
-    with open(json_path, 'r', encoding='utf-8') as src:
-        content = src.read()
-    with open(backup_path, 'w', encoding='utf-8') as dst:
-        dst.write(content)
+    shutil.copy2(json_path, backup_path)
```

## Testing Results

- Executado `test_edit_feature.py` — `backup_json()` cria backups com sucesso.
- Fluxo de edição procede e as alterações são aplicadas quando o backup é bem-sucedido.

## Files Modified

- `cli.py`
- `docs/issues/2025-12-17_backup-creation_ISSUE.md`
- `docs/issues/2025-12-17_backup-creation_FIX.md`
- `docs/issues/README.md` (índice atualizado)

## Benefits

- Maior robustez na criação de backups.
- Mensagens de erro mais claras para o utilizador.

## Status

✅ Resolved
