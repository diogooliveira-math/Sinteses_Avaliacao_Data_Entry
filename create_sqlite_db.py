import json
import sqlite3
import os

BASE_JSON = "base.json"
DB_FILE = "base.db"

def main():
    root = os.path.dirname(__file__)
    json_path = os.path.join(root, BASE_JSON)
    db_path = os.path.join(root, DB_FILE)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sinteses (
            id INTEGER PRIMARY KEY,
            Texto TEXT,
            Genero TEXT,
            Assiduidade INTEGER,
            Pontualidade INTEGER,
            Participacao INTEGER,
            Interesse INTEGER,
            Empenho INTEGER,
            Dificuldades INTEGER
        )
        """
    )

    inserted = 0
    for item in data:
        texto = item.get("Texto")
        genero = item.get("Genero")
        ass = item.get("Assiduidade")
        pont = item.get("Pontualidade")
        # JSON may use 'Participação' with accent; try both keys
        particip = item.get("Participacao") if item.get("Participacao") is not None else item.get("Participação")
        interesse = item.get("Interesse")
        empenho = item.get("Empenho")
        dificuldades = item.get("Dificuldades")

        cur.execute(
            "INSERT INTO sinteses (Texto,Genero,Assiduidade,Pontualidade,Participacao,Interesse,Empenho,Dificuldades) VALUES (?,?,?,?,?,?,?,?)",
            (texto, genero, ass, pont, particip, interesse, empenho, dificuldades),
        )
        inserted += 1

    conn.commit()
    conn.close()

    print(f"Created SQLite DB: {db_path}")
    print(f"Inserted rows: {inserted}")


if __name__ == "__main__":
    main()
