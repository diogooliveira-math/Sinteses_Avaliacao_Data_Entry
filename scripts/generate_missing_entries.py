"""
Script para gerar todas as combinações em falta na base de dados de sínteses.
"""
import json
from itertools import product

def generate_text(genero, assiduidade, pontualidade, participacao, interesse, empenho, dificuldades):
    """Gera texto de síntese baseado nos parâmetros."""
    
    # Definir artigos e pronomes
    if genero == 'F':
        artigo = "A aluna"
        pron_fem = "a"
    else:
        artigo = "O aluno"
        pron_fem = "o"
    
    # Construir primeira parte (assiduidade e pontualidade)
    primeira_parte = []
    
    if assiduidade and pontualidade:
        primeira_parte.append(f"{artigo} é assídu{pron_fem} e pontual")
    elif assiduidade and not pontualidade:
        primeira_parte.append(f"{artigo} é assídu{pron_fem}, mas pouco pontual")
    elif not assiduidade and pontualidade:
        primeira_parte.append(f"{artigo} é pouco assídu{pron_fem}, embora pontual")
    else:
        primeira_parte.append(f"{artigo} é pouco assídu{pron_fem} e pouco pontual")
    
    # Adicionar participação à primeira parte
    if participacao:
        primeira_parte.append(" e participativ" + pron_fem)
    else:
        # Se já tem "mas" na frase (não pontual ou não assíduo mas o outro sim)
        if (assiduidade and not pontualidade) or (not assiduidade and pontualidade):
            primeira_parte.append(" e pouco participativ" + pron_fem)
        else:
            primeira_parte.append(", mas pouco participativ" + pron_fem)
    
    primeira_parte_texto = "".join(primeira_parte) + "."
    
    # Construir segunda parte (interesse e empenho)
    segunda_parte = []
    
    if interesse and empenho:
        segunda_parte.append("Revela interesse e empenho nas atividades propostas.")
    elif interesse and not empenho:
        segunda_parte.append("Revela interesse nas atividades propostas, mas o empenho não foi satisfatório.")
    elif not interesse and empenho:
        segunda_parte.append("Deverá demonstrar interesse pelas atividades propostas. Revela empenho nas tarefas.")
    else:
        segunda_parte.append("Deverá demonstrar interesse pelas atividades propostas e o empenho não foi satisfatório.")
    
    # Adicionar dificuldades
    if dificuldades:
        if interesse and empenho:
            segunda_parte[0] = segunda_parte[0].replace("nas atividades propostas.", "nas atividades propostas. Apresenta algumas dificuldades.")
        else:
            segunda_parte.append(" Apresenta algumas dificuldades.")
    
    segunda_parte_texto = "".join(segunda_parte)
    
    # Juntar tudo
    texto_final = primeira_parte_texto + " " + segunda_parte_texto
    
    return texto_final


def main():
    # Carregar dados existentes
    with open('base.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # Criar conjunto de combinações existentes
    existing_combinations = set()
    for item in existing_data:
        combo = (
            item.get('Genero'),
            item.get('Assiduidade'),
            item.get('Pontualidade'),
            item.get('Participacao', item.get('Participação')),
            item.get('Interesse'),
            item.get('Empenho'),
            item.get('Dificuldades')
        )
        existing_combinations.add(combo)
    
    # Gerar todas as combinações possíveis
    all_combinations = list(product(['M', 'F'], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]))
    
    # Identificar combinações em falta
    missing_combinations = [c for c in all_combinations if c not in existing_combinations]
    
    print(f"Total de combinações possíveis: {len(all_combinations)}")
    print(f"Combinações existentes: {len(existing_combinations)}")
    print(f"Combinações em falta: {len(missing_combinations)}")
    
    # Gerar novas entradas
    new_entries = []
    for combo in missing_combinations:
        genero, ass, pont, part, inter, emp, dif = combo
        texto = generate_text(genero, ass, pont, part, inter, emp, dif)
        
        entry = {
            "Texto": texto,
            "Genero": genero,
            "Assiduidade": ass,
            "Pontualidade": pont,
            "Participação": part,
            "Interesse": inter,
            "Empenho": emp,
            "Dificuldades": dif
        }
        new_entries.append(entry)
    
    # Combinar com dados existentes
    complete_data = existing_data + new_entries
    
    # Ordenar por Genero e depois pelos outros campos
    complete_data.sort(key=lambda x: (
        x['Genero'],
        x['Assiduidade'],
        x['Pontualidade'],
        x.get('Participacao', x.get('Participação')),
        x['Interesse'],
        x['Empenho'],
        x['Dificuldades']
    ))
    
    # Salvar em novo arquivo
    with open('base_complete.json', 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nArquivo 'base_complete.json' criado com {len(complete_data)} entradas.")
    print(f"Novas entradas adicionadas: {len(new_entries)}")
    
    # Mostrar algumas das novas entradas geradas
    print("\nExemplos de novas entradas geradas:")
    for i, entry in enumerate(new_entries[:5], 1):
        print(f"\n{i}. Genero={entry['Genero']}, Ass={entry['Assiduidade']}, "
              f"Pont={entry['Pontualidade']}, Part={entry.get('Participação')}, "
              f"Int={entry['Interesse']}, Emp={entry['Empenho']}, Dif={entry['Dificuldades']}")
        print(f"   Texto: {entry['Texto']}")
    
    # Verificar se a combinação problemática foi adicionada
    problema_combo = ('F', 1, 0, 0, 0, 0, 0)
    encontrada = any(
        (e['Genero'], e['Assiduidade'], e['Pontualidade'], 
         e.get('Participacao', e.get('Participação')), e['Interesse'], 
         e['Empenho'], e['Dificuldades']) == problema_combo
        for e in complete_data
    )
    print(f"\nCombinação problemática (F,1,0,0,0,0,0) foi adicionada: {encontrada}")


if __name__ == "__main__":
    main()
