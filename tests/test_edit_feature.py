#!/usr/bin/env python3
"""
Test script for the edit feature without user interaction.
Tests all the new functions added to cli.py
"""

import os
import json
import sqlite3
from cli import (
    validate_text,
    get_database_path,
    update_entry_in_db
)

def test_validate_text():
    """Test text validation"""
    print("\n=== Teste: Validação de Texto ===")
    
    tests = [
        ("", False, "Texto vazio"),
        ("abc", False, "Texto curto (<10 caracteres)"),
        ("Este é um texto válido com mais de dez caracteres.", True, "Texto válido")
    ]
    
    for text, expected_valid, description in tests:
        valid, message = validate_text(text)
        status = "✓" if valid == expected_valid else "✗"
        print(f"{status} {description}: {message}")

# Backup-related functionality removed: tests no longer create backups.

def test_update_entry():
    """Test updating an entry in JSON and database"""
    print("\n=== Teste: Atualização de Entrada ===")
    
    db_path = get_database_path()
    # json_path = get_json_path()  # no longer used; we operate on DB only
    
    # Read current entry from database to get real data
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT Genero, Assiduidade, Pontualidade, Participacao, Interesse, Empenho, Dificuldades, Texto FROM sinteses LIMIT 1")
    row = cur.fetchone()
    conn.close()
    
    if not row:
        print("✗ Nenhuma entrada encontrada na base de dados")
        return
    
    genero, assid, pont, part, inter, empen, diff, original_text = row
    
    print(f"Entrada original:")
    print(f"  Texto: {original_text[:60]}...")
    print(f"  Critérios: G={genero}, A={assid}, P={pont}, Pa={part}, I={inter}, E={empen}, D={diff}")
    
    # Create a test update with new text
    new_text = "TEXTO EDITADO PARA TESTE - Validação da funcionalidade de edição no VSCode"
    
    criteria = {
        "Genero": genero,
        "Assiduidade": assid,
        "Pontualidade": pont,
        "Participacao": part,
        "Interesse": inter,
        "Empenho": empen,
        "Dificuldades": diff
    }
    
    # No backup step (feature removed)

    # Attempt update (DB only)
    result = update_entry_in_db(db_path, criteria, new_text)
    
    if result:
        print(f"\n✓ Entrada atualizada com sucesso")
        
        # Verify the update in database only
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT Texto FROM sinteses WHERE Genero=? AND Assiduidade=? AND Pontualidade=? AND Participacao=? AND Interesse=? AND Empenho=? AND Dificuldades=?",
            (genero, assid, pont, part, inter, empen, diff)
        )
        db_row = cur.fetchone()
        conn.close()
        
        if db_row and db_row[0] == new_text:
            print("  ✓ Texto atualizado em base.db")
        else:
            print("  ✗ Texto NÃO atualizado em base.db")
        
        # Restore original text in DB
        print("\n⚠ Revertendo para texto original no DB...")
        update_entry_in_db(db_path, criteria, original_text)
        print("✓ Texto restaurado no DB")
    else:
        print("✗ Falha ao atualizar entrada")

def main():
    print("=" * 60)
    print("TESTES - NOVA FUNCIONALIDADE DE EDIÇÃO")
    print("=" * 60)
    
    test_validate_text()
    def test_backup():
        """Test backup creation for base.db"""

        print("\n=== Teste: Backup de base.db ===")

        result = backup_db()
        if result:
            db_path = get_database_path()
            # Count backup files
            import glob
            backups = glob.glob(f"{db_path}.backup.*")
            print(f"✓ Backup criado com sucesso")
            print(f"  Total de backups: {len(backups)}")
            if backups:
                print(f"  Último backup: {os.path.basename(backups[-1])}")
        else:
            print("✗ Falha ao criar backup do DB")
