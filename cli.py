#!/usr/bin/env python3
import sqlite3
import sys
import os
import json
import subprocess
import tempfile
from datetime import datetime
import platform
import shutil

def get_application_path():
    """Get the absolute path to the application directory."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as Python script
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path


def find_resource(name):
    """Find a resource file (like base.db or base.json) in a sensible order:

    When running as a frozen executable:
    1. Directory specified by `SINT_BASE_DIR` environment variable (if set)
    2. Application directory (executable location) - prioritized for executables
    3. Parent of application directory

    When running as Python script:
    1. Directory specified by `SINT_BASE_DIR` environment variable (if set)
    2. Current working directory (if it has the file)
    3. Application directory (script location) - this will be used as fallback
    4. Parent of application directory

    Returns an absolute path (may not exist). Prefer existing files if found.
    """
    app_dir = get_application_path()
    is_frozen = getattr(sys, 'frozen', False)
    
    # 1) env override (always first)
    env_dir = os.getenv('SINT_BASE_DIR')
    if env_dir:
        p = os.path.join(env_dir, name)
        if os.path.exists(p):
            return os.path.abspath(p)

    # 2) For frozen executables, prioritize app dir to work from any CWD
    if is_frozen:
        p = os.path.join(app_dir, name)
        if os.path.exists(p):
            return os.path.abspath(p)
    else:
        # For scripts, check CWD only if it actually has the file
        p = os.path.join(os.getcwd(), name)
        if os.path.exists(p):
            return os.path.abspath(p)

    # 3) application directory (script location) - fallback for both cases
    p = os.path.join(app_dir, name)
    if os.path.exists(p):
        return os.path.abspath(p)

    # 4) parent of application directory
    parent = os.path.dirname(app_dir)
    p = os.path.join(parent, name)
    if os.path.exists(p):
        return os.path.abspath(p)

    # Fallback: return application dir path (even if it doesn't exist)
    return os.path.abspath(os.path.join(app_dir, name))

def get_database_path():
    """
    Get the absolute path to base.db relative to the executable/script location.
    
    This ensures the database is found whether running as:
    - A PyInstaller executable (from any directory)
    - A Python script (from any directory)
    """
    return find_resource('base.db')

def get_json_path():
    """Get the absolute path to base.json."""
    return find_resource('base.json')

def press_enter_prompt():
    try:
        input("Novo aluno? PRESS ENTER TO CONTINUE")
    except KeyboardInterrupt:
        sys.exit(0)

def ask_gender():
    while True:
        v = input("Qual o género do aluno (M/F): ").strip().upper()
        if v in ("M", "F"):
            return v
        print("Resposta inválida — escreva M ou F.")

def ask_yesno(prompt):
    while True:
        v = input(prompt + " (s/n): ").strip().lower()
        if v in ("y", "yes", "s", "sim"):
            return 1
        if v in ("n", "no"):
            return 0
        print("Resposta inválida — escreva s ou n.")

def copy_to_clipboard(text):
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        pass
    # Fallback to tkinter (standard on most Python Windows installs)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return True
    except Exception:
        return False

def build_and_run_query(db_path, genero, assid, punt, part, inter, empen, diff):
    where = []
    params = []
    if genero:
        where.append("Genero = ?")
        params.append(genero)
    where.append("Assiduidade = ?")
    params.append(assid)
    where.append("Pontualidade = ?")
    params.append(punt)
    where.append("Participacao = ?")
    params.append(part)
    where.append("Interesse = ?")
    params.append(inter)
    where.append("Empenho = ?")
    params.append(empen)
    where.append("Dificuldades = ?")
    params.append(diff)

    where_sql = " AND ".join(where) if where else "1"
    sql = f"SELECT Texto FROM sinteses WHERE {where_sql} LIMIT 1;"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def backup_json():
    """Create a timestamped backup of base.json."""
    json_path = get_json_path()
    if not os.path.exists(json_path):
        print(f"✗ base.json não encontrado em: {json_path}")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{json_path}.backup.{timestamp}"

    try:
        # Use shutil.copy2 to preserve metadata and handle binary-safe copying
        shutil.copy2(json_path, backup_path)
        print(f"✓ Backup criado: {os.path.basename(backup_path)}")
        return True
    except Exception as e:
        # Provide a clearer message for troubleshooting
        print(f"✗ Erro ao criar backup: {e}")
        return False


def backup_db():
    """Create a timestamped backup of base.db."""
    db_path = get_database_path()
    if not os.path.exists(db_path):
        print(f"✗ base.db não encontrado em: {db_path}")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.backup.{timestamp}"

    try:
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup criado: {os.path.basename(backup_path)}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar backup do DB: {e}")
        return False

def open_text_in_editor(text):
    """
    Open text in an editor (VSCode -> notepad -> nano) and return the edited text.
    Returns None if user cancels or validation fails.
    """
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
        tmp.write(text)
        tmp_path = tmp.name
    
    try:
        # Try VSCode first
        try:
            result = subprocess.run(['code', '--wait', tmp_path], capture_output=True, timeout=300)
            if result.returncode == 0:
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback to notepad on Windows
        if platform.system() == 'Windows':
            try:
                subprocess.run(['notepad', tmp_path], check=False)
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                pass
        
        # Fallback to nano on Linux/Mac
        if platform.system() in ('Linux', 'Darwin'):
            try:
                subprocess.run(['nano', tmp_path], check=False)
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                pass
        
        print("✗ Nenhum editor disponível (VSCode, notepad ou nano)")
        return None
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass

def validate_text(text):
    """Validate edited text. Returns (valid, message)."""
    text = text.strip()
    if not text:
        return False, "✗ Texto não pode estar vazio."
    if len(text) < 10:
        return False, "✗ Texto demasiado curto. Mínimo 10 caracteres."
    return True, "✓ Texto validado com sucesso."

def ask_edit_confirmation():
    """Ask if user wants to edit the text."""
    return bool(ask_yesno("Deseja editar este texto?"))

def ask_satisfaction():
    """Ask if user is satisfied with the edited text."""
    return bool(ask_yesno("Satisfeito com a edição?"))

def update_entry_in_json_and_db(db_path, json_path, criteria, new_text):
    """
    Update an entry in both JSON and database.
    criteria = {Genero, Assiduidade, Pontualidade, Participacao, Interesse, Empenho, Dificuldades}
    """
    # Update JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Find and update the entry
        found = False
        for item in data:
            # Check if all criteria match (handle both Participacao and Participação)
            participacao_val = item.get("Participacao") if item.get("Participacao") is not None else item.get("Participação")
            if (item.get("Genero") == criteria["Genero"] and
                item.get("Assiduidade") == criteria["Assiduidade"] and
                item.get("Pontualidade") == criteria["Pontualidade"] and
                participacao_val == criteria["Participacao"] and
                item.get("Interesse") == criteria["Interesse"] and
                item.get("Empenho") == criteria["Empenho"] and
                item.get("Dificuldades") == criteria["Dificuldades"]):
                item["Texto"] = new_text
                found = True
                break
        
        if not found:
            print("✗ Entrada não encontrada em base.json")
            return False
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    except Exception as e:
        print(f"✗ Erro ao atualizar JSON: {e}")
        return False
    
    # Update Database
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        where_clause = (
            "Genero = ? AND Assiduidade = ? AND Pontualidade = ? AND "
            "Participacao = ? AND Interesse = ? AND Empenho = ? AND Dificuldades = ?"
        )
        params = [
            new_text,
            criteria["Genero"],
            criteria["Assiduidade"],
            criteria["Pontualidade"],
            criteria["Participacao"],
            criteria["Interesse"],
            criteria["Empenho"],
            criteria["Dificuldades"]
        ]
        
        cur.execute(f"UPDATE sinteses SET Texto = ? WHERE {where_clause}", params)
        conn.commit()
        rows_updated = cur.rowcount
        conn.close()
        
        if rows_updated > 0:
            print("✓ Texto atualizado com sucesso em base.json e base.db")
            return True
        else:
            print("✗ Entrada não encontrada na base de dados")
            return False
    
    except Exception as e:
        print(f"✗ Erro ao atualizar base de dados: {e}")
        return False


def update_entry_in_db(db_path, criteria, new_text):
    """Update the Texto field in the database only (no JSON changes)."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        where_clause = (
            "Genero = ? AND Assiduidade = ? AND Pontualidade = ? AND "
            "Participacao = ? AND Interesse = ? AND Empenho = ? AND Dificuldades = ?"
        )
        params = [
            new_text,
            criteria["Genero"],
            criteria["Assiduidade"],
            criteria["Pontualidade"],
            criteria["Participacao"],
            criteria["Interesse"],
            criteria["Empenho"],
            criteria["Dificuldades"]
        ]

        cur.execute(f"UPDATE sinteses SET Texto = ? WHERE {where_clause}", params)
        conn.commit()
        rows_updated = cur.rowcount
        conn.close()

        if rows_updated > 0:
            print("✓ Texto atualizado com sucesso em base.db")
            return True
        else:
            print("✗ Entrada não encontrada na base de dados")
            return False

    except Exception as e:
        print(f"✗ Erro ao atualizar base de dados: {e}")
        return False

def main():
    press_enter_prompt()
    db_path = get_database_path()
    json_path = get_json_path()
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"\n❌ ERRO: Base de dados não encontrada!")
        print(f"   Esperado em: {db_path}")
        print(f"\n💡 Solução:")
        print(f"   1. Certifique-se que 'base.db' está na mesma pasta que o executável")
        print(f"   2. Ou execute 'python create_sqlite_db.py' para criar a base de dados")
        sys.exit(1)
    
    genero = ask_gender()
    assid = ask_yesno("O aluno é assíduo?")
    punt = ask_yesno("O aluno é pontual?")
    part = ask_yesno("O aluno é participativo?")
    inter = ask_yesno("O aluno mostra interesse?")
    empen = ask_yesno("O aluno mostra empenho?")
    diff = ask_yesno("O aluno mostra dificuldades?")

    texto = build_and_run_query(db_path, genero, assid, punt, part, inter, empen, diff)
    if not texto:
        print("Nenhuma correspondência encontrada para os filtros definidos.")
        return

    print("\n--- Texto encontrado ---\n")
    print(texto)
    print("\n--- A tentar copiar para a área de transferência... ---")
    if copy_to_clipboard(texto):
        print("Texto copiado para a área de transferência.")
    else:
        print("Falha ao copiar automaticamente. Copie manualmente do ecrã se necessário.")
    
    # Editing loop
    if ask_edit_confirmation():
        criteria = {
            "Genero": genero,
            "Assiduidade": assid,
            "Pontualidade": punt,
            "Participacao": part,
            "Interesse": inter,
            "Empenho": empen,
            "Dificuldades": diff
        }
        
        while True:
            print("\n--- Abrindo editor... ---")
            edited_text = open_text_in_editor(texto)
            
            if edited_text is None:
                print("❌ Editor fechado sem guardar.")
                return
            
            # Validate the edited text
            valid, message = validate_text(edited_text)
            print(message)
            
            if not valid:
                print("Por favor, edite novamente.")
                continue
            
            # Show the edited text
            print("\n--- Texto editado ---\n")
            print(edited_text)
            
            # Ask if satisfied
            if ask_satisfaction():
                        # Backup DB before updating (we operate on DB only)
                        if not backup_db():
                            print("⚠ Aviso: Não foi possível criar backup do DB. Operação cancelada.")
                            return

                        # Copy to clipboard
                        copy_to_clipboard(edited_text)

                        print("\n--- Texto copiado para a área de transferência ---")
                        print("\n--- A tentar guardar alterações no DB... ---")

                        # Update database only
                        if update_entry_in_db(db_path, criteria, edited_text):
                            print("\n✓ Alterações guardadas com sucesso!")
                            return
                        else:
                            print("\n❌ Erro ao guardar alterações no DB.")
                            return
            else:
                # Continue editing
                texto = edited_text
                print("\nEditar novamente...")

if __name__ == '__main__':
    main()
