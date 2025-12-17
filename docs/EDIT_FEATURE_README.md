# Edição Automática com VSCode - Implementação Completa

## Resumo das Alterações

O sistema foi atualizado para permitir edição automática de textos de avaliação após cada consulta, com sincronização bidirecional entre `base.json` e `base.db`.

## Novas Funcionalidades em `cli.py`

### 1. **Edição após Consulta**
Após encontrar um texto, o utilizador é automaticamente perguntado:
```
Deseja editar este texto? (s/n):
```

### 2. **Suporte Multi-Editor**
Tenta abrir o editor na seguinte ordem:
- **VSCode** (com `code --wait`)
- **Notepad** (fallback para Windows)
- **Nano** (fallback para Linux/macOS)

### 3. **Validação de Texto**
- ✓ Texto não pode estar vazio
- ✓ Texto mínimo de 10 caracteres
- ✓ Espaços em branco automaticamente removidos

### 4. **Loop de Reedição**
Após edição, pergunta: "Satisfeito com a edição? (s/n)"
- **Sim**: Cria backup automático → Atualiza JSON + BD → Termina
- **Não**: Reabre o editor para continuar editando

### 5. **Backup Automático**
Antes de qualquer atualização, cria backup com timestamp:
```
base.json.backup.YYYYMMDD_HHMMSS
```

### 6. **Sincronização Bidirecional**
Cada edição atualiza simultaneamente:
- ✓ `base.json` (fonte de verdade)
- ✓ `base.db` (para queries imediatas)

## Funções Adicionadas

| Função | Descrição |
|--------|-----------|
| `get_application_path()` | Localiza diretório da app |
| `get_json_path()` | Retorna caminho de base.json |
| `backup_json()` | Cria backup com timestamp |
| `open_text_in_editor(text)` | Abre editor e retorna texto editado |
| `validate_text(text)` | Valida tamanho mínimo |
| `ask_edit_confirmation()` | Pergunta se deseja editar |
| `ask_satisfaction()` | Pergunta se está satisfeito |
| `update_entry_in_json_and_db()` | Atualiza JSON e DB simultaneamente |

## Fluxo de Execução

```
1. Consulta normal (genero + 6 critérios)
   ↓
2. Texto encontrado e copiado para clipboard
   ↓
3. "Deseja editar este texto? (s/n)"
   ├─ NÃO → Termina
   └─ SIM:
      ↓
4. Abre editor (VSCode/notepad/nano)
   ↓
5. Valida texto (não vazio, >10 caracteres)
   ├─ INVÁLIDO → Repete editor
   └─ VÁLIDO:
      ↓
6. Mostra texto editado
   ↓
7. "Satisfeito com a edição? (s/n)"
   ├─ NÃO → Volta ao passo 4 com novo texto
   └─ SIM:
      ↓
8. Cria backup: base.json.backup.20251217_HHMMSS
   ↓
9. Atualiza base.json (encontra por 7 critérios)
   ↓
10. Atualiza base.db (UPDATE sinteses SET Texto=? WHERE ...)
    ↓
11. Confirma sucesso e termina
```

## Critérios de Correspondência

Cada entrada é localizada pela combinação única de 7 atributos:
1. `Genero` (M/F)
2. `Assiduidade` (0/1)
3. `Pontualidade` (0/1)
4. `Participacao` (0/1) - também tenta `Participação`
5. `Interesse` (0/1)
6. `Empenho` (0/1)
7. `Dificuldades` (0/1)

Isto garante que cada combinação é única e atualiza apenas a entrada desejada.

## Testes Implementados

Ver `test_edit_feature.py` com testes para:
- ✓ Validação de texto (vazio, curto, válido)
- ✓ Criação de backups com timestamp
- ✓ Atualização em JSON
- ✓ Atualização em base de dados
- ✓ Reversão a texto original

Todos os testes passaram com sucesso.

## Utilização Prática

```bash
# Executa a aplicação normalmente
python cli.py
# ou
s  # alias do PowerShell

# Responde às perguntas de género e critérios
# Copia o texto para clipboard
# Se desejar editar:
#   - VSCode abre automaticamente
#   - Edita o texto
#   - Guarda (Ctrl+S) e fecha (Ctrl+W)
#   - Valida o texto
#   - Confirma satisfação
#   - Backup criado e BD atualizada
```

## Compatibilidade

- ✓ Windows (VSCode ou Notepad)
- ✓ Linux/macOS (VSCode ou Nano)
- ✓ Mantém compatibilidade com executável PyInstaller
- ✓ Funciona de qualquer diretório
