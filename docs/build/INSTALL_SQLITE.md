# Instalar e configurar o sqlite3

Este guia rápido mostra como instalar o cliente `sqlite3` (CLI) e verificar a configuração no Windows, macOS e Linux. Nota: o módulo `sqlite3` já vem incluído no Python padrão, pelo que normalmente não é preciso instalar nada para usar SQLite a partir de scripts Python.

**Verificação rápida (Python)**

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Se isto imprimir uma versão (ex.: `3.39.2`), o suporte SQLite no Python está OK.

**Windows (CLI)**

- Opção 1 — `winget` (preferível se disponível):

```powershell
winget install SQLite.SQLite
```

- Opção 2 — Chocolatey:

```powershell
choco install sqlite
```

- Opção 3 — download manual:

1. Aceda a https://www.sqlite.org/download.html
2. Faça o download de `sqlite-tools-win32-x86-<versão>.zip`.
3. Extraia `sqlite3.exe` para uma pasta (ex.: `C:\tools\sqlite`).
4. Adicione essa pasta ao `PATH` do sistema:

    - Abra “Editar variáveis de ambiente do sistema”.
    - Em “Variáveis do sistema” selecione `Path` → Editar → Novo → cole `C:\tools\sqlite`.
    - Reinicie o terminal.x

Verifique:

```powershell
sqlite3 --version
sqlite3 base.db "SELECT count(*) FROM sqlite_master;"
```

**macOS**

- Usando Homebrew:

```bash
brew install sqlite
```

Verifique:

```bash
sqlite3 --version
```

**Linux (Debian/Ubuntu)**

```bash
sudo apt update
sudo apt install sqlite3
sqlite3 --version
```

Outras distribuições: use o gestor de pacotes correspondente (`dnf`, `pacman`, etc.).

**Notas sobre Python**

- O módulo `sqlite3` faz parte da biblioteca padrão do Python. Para confirmar:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

- Se precisar de uma versão recente isolada para Python, existe o pacote `pysqlite3-binary`, mas na maioria dos casos não é necessário:

```bash
pip install pysqlite3-binary
```

**Permissões e ficheiros DB**

- Coloque o ficheiro `.db` numa pasta onde o utilizador tenha permissões de leitura/escrita.
- Em ambientes de produção, considere backups regulares e travamento de ficheiros quando o DB for partilhado.

**Exemplo rápido de uso (CLI)**

```bash
sqlite3 base.db "SELECT Texto FROM sinteses WHERE Genero='F' AND Assiduidade=1;"
```

Se quiser, eu posso adicionar um pequeno script CLI em Python para consultar `base.db` com filtros dinâmicos.
