import random

# Funções geradoras
def gerar_particoes(qtd=10, min_tam=50, max_tam=500):
    """Gera uma lista de tamanhos de partições aleatórios."""
    return [random.randint(min_tam, max_tam) for _ in range(qtd)]

def gerar_processos(qtd=4, min_tam=10, max_tam=300):
    """Gera uma lista de tamanhos de processos aleatórios."""
    return [random.randint(min_tam, max_tam) for _ in range(qtd)]

# Função auxiliar para imprimir os resultados de um algoritmo
def executar_algoritmo(nome, particoes, processos):
    """
    Executa um algoritmo de alocação e imprime os resultados.
    Retorna a listagem final para manipulação caso necessário.
    """
    # Cópia das partições para controle de estado (Fixo: [lista de dicts])
    # Estrutura: {'size': tamanho, 'alocado_para': None ou indice_do_processo}
    estado_particoes = [{'size': s, 'alocado_para': None} for s in particoes]
    
    resultados_alocacao = [] # Guarda as linhas da tabela
    total_fragmentacao = 0
    
    # Variáveis de lógica dependendo do algoritmo
    ultimo_indice_alocado = 0 # Para Next-Fit

    # ------------------------------------
    # Lógica dos Algoritmos
    # ------------------------------------
    for idx_processo, tam_processo in enumerate(processos):
        alocado = False
        indice_particao_alocada = -1
        fragmentacao_gerada = 0
        tamanho_particao_alocada = 0

        # ========== FIRST-FIT ==========
        if nome == "FIRST-FIT":
            for i, part in enumerate(estado_particoes):
                if part['alocado_para'] is None and part['size'] >= tam_processo:
                    indice_particao_alocada = i
                    tamanho_particao_alocada = part['size']
                    fragmentacao_gerada = part['size'] - tam_processo
                    part['alocado_para'] = idx_processo
                    alocado = True
                    break

        # ========== BEST-FIT ==========
        elif nome == "BEST-FIT":
            melhor_indice = -1
            menor_diferenca = float('inf')
            
            for i, part in enumerate(estado_particoes):
                if part['alocado_para'] is None and part['size'] >= tam_processo:
                    diff = part['size'] - tam_processo
                    if diff < menor_diferenca:
                        menor_diferenca = diff
                        melhor_indice = i
            
            if melhor_indice != -1:
                part = estado_particoes[melhor_indice]
                indice_particao_alocada = melhor_indice
                tamanho_particao_alocada = part['size']
                fragmentacao_gerada = part['size'] - tam_processo
                part['alocado_para'] = idx_processo
                alocado = True

        # ========== NEXT-FIT ==========
        elif nome == "NEXT-FIT":
            inicio_busca = ultimo_indice_alocado
            n_particoes = len(estado_particoes)
            
            # Busca a partir do último índice
            for i in range(n_particoes):
                idx_real = (inicio_busca + i) % n_particoes
                part = estado_particoes[idx_real]
                if part['alocado_para'] is None and part['size'] >= tam_processo:
                    indice_particao_alocada = idx_real
                    tamanho_particao_alocada = part['size']
                    fragmentacao_gerada = part['size'] - tam_processo
                    part['alocado_para'] = idx_processo
                    alocado = True
                    ultimo_indice_alocado = (idx_real + 1) % n_particoes
                    break

        # ------------------------------------
        # Montagem dos resultados
        # ------------------------------------
        if alocado:
            total_fragmentacao += fragmentacao_gerada
            resultados_alocacao.append({
                'processo': f"P{idx_processo + 1}",
                'memoria_req': tam_processo,
                'index_particao': indice_particao_alocada + 1, # Índice legível (inicia em 1)
                'tam_particao': tamanho_particao_alocada,
                'fragmentacao': fragmentacao_gerada
            })
        else:
            resultados_alocacao.append({
                'processo': f"P{idx_processo + 1}",
                'memoria_req': tam_processo,
                'index_particao': "-",
                'tam_particao': "-",
                'fragmentacao': "-"
            })
    
    # ------------------------------------
    # SAÍDA DE DADOS (Tabela e Estatísticas)
    # ------------------------------------
    print(f"\nRESULTADO: {nome}")
    print("="*65)
    # Cabeçalho da tabela
    print(f"{'Processo':<10} {'Memória':<12} {'Partição':<10} {'Tam. Partição':<15} {'Fragmentação':<12}")
    print("-" * 65)

    for res in resultados_alocacao:
        print(f"{res['processo']:<10} {res['memoria_req']:<12} {res['index_particao']:<10} {res['tam_particao']:<15} {res['fragmentacao']:<12}")

    # Estatísticas finais
    processos_alocados = sum(1 for r in resultados_alocacao if r['index_particao'] != "-")
    processos_nao_alocados = len(processos) - processos_alocados
    
    print(f"\nFragmentação total: {total_fragmentacao} KB")
    print(f"Processos alocados: {processos_alocados}")
    print(f"Processos não alocados: {processos_nao_alocados}")
    
    print("Estado final das partições:")
    for idx, part in enumerate(estado_particoes, start=1):
        if part['alocado_para'] is not None:
            proc_idx = part['alocado_para']
            tam_proc = processos[proc_idx]
            frag = part['size'] - tam_proc
            print(f"Partição {idx} -> {part['size']} KB | P{proc_idx+1} | Fragmentação: {frag} KB")
        else:
            print(f"Partição {idx} -> {part['size']} KB | Livre")
    
    return resultados_alocacao

# ==========================================
# MAIN - Execução do Programa
# ==========================================
if __name__ == "__main__":
    # 1. Gerar listas conforme as regras
    particoes = gerar_particoes()
    processos = gerar_processos()

    # 2. Lista de partições geradas
    print("PARTIÇÕES GERADAS:")
    for i, p in enumerate(particoes, start=1):
        print(f"Partição {i} -> {p} KB")

    # 3. Lista de processos gerados
    print("\nPROCESSOS GERADOS:")
    for i, proc in enumerate(processos, start=1):
        print(f"Processo P{i} -> {proc} KB")

    # 4. Executar e mostrar o resultado de cada algoritmo separadamente
    executar_algoritmo("FIRST-FIT", particoes, processos)
    executar_algoritmo("BEST-FIT", particoes, processos)
    executar_algoritmo("NEXT-FIT", particoes, processos)
