import numpy as np
import os

def obter_matriz_rotacao(n: int, m: int) -> np.ndarray:
    """Calcula a matriz de rotação baseada nos índices m e n do TBG."""
    # cos(theta) = (n^2 + 4nm + m^2) / (2 * (n^2 + nm + m^2))
    numerador = n**2 + 4*n*m + m**2
    denominador = 2 * (n**2 + n*m + m**2)
    
    # CORREÇÃO AQUI: 'numerador' estava escrito errado
    cos_theta = numerador / denominador
    
    # Garante precisão numérica dentro de [-1, 1]
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    sin_theta = np.sqrt(1 - cos_theta**2)
    
    return np.array([[cos_theta, -sin_theta], 
                     [sin_theta, cos_theta]])

def ler_coordenadas_vasp(filepath: str) -> np.ndarray:
    """Lê as coordenadas atômicas de um arquivo VASP (pulando o cabeçalho)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    # Pula as 8 linhas de cabeçalho padrão do VASP
    return np.loadtxt(filepath, skiprows=8, usecols=(0, 1, 2))

def ler_vetores_base(filepath: str) -> np.ndarray:
    """Lê os 3 vetores de base da rede de um arquivo VASP."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Template '{filepath}' não encontrado. Necessário para ler os vetores de base.")
        
    with open(filepath, 'r') as f:
        # Pula as 2 primeiras linhas (Comentário e Fator de escala)
        next(f)
        next(f)
        # Lê as próximas 3 linhas como vetores
        vetores = np.loadtxt(f, max_rows=3)
    return vetores

def esta_dentro_da_celula(ponto, origem, v1, v2, v3, v4):
    """
    Verifica se um ponto está dentro da região delimitada pelos vetores
    usando produto vetorial (regra da mão direita).
    """
    # Vetores relativos à origem da célula de recorte
    r = -ponto + origem
    
    # Produtos vetoriais
    cp1 = np.cross(r, v1)
    cp2 = np.cross(-ponto + (origem + v1), v2)
    cp3 = np.cross(-ponto + (origem + v1 + v2), v3)
    cp4 = np.cross(-ponto + (origem + v1 + v2 + v3), v4)
    
    # Verifica se a componente Z de todos os produtos vetoriais é positiva
    return cp1[2] > 0 and cp2[2] > 0 and cp3[2] > 0 and cp4[2] > 0

def main():
    # --- Configurações ---
    ARQUIVO_ENTRADA = 'POSCAR_13_10_10.vasp'
    ARQUIVO_TEMPLATE = 'POSCAR_13.vasp' # Usado para ler os vetores de base da célula unitária
    ARQUIVO_SAIDA = 'POSCAR.vasp'
    
    N, M = 3, 2  # Índices de torção
    W_OFFSET = 7.0 # Posição inicial de recorte
    Z_CORTE = 3.0  # Altura para separar as camadas (Angstroms)

    print(f"--- Processando TBG ({N}, {M}) ---")

    # 1. Leitura dos dados
    print(f"Lendo {ARQUIVO_ENTRADA}...")
    coords = ler_coordenadas_vasp(ARQUIVO_ENTRADA)
    
    # 2. Separação de camadas e Rotação
    # Máscaras booleanas para separar camadas
    mask_top = coords[:, 2] > Z_CORTE
    mask_bottom = coords[:, 2] <= Z_CORTE
    
    coords_top = coords[mask_top].copy()
    coords_bottom = coords[mask_bottom].copy()

    print("Aplicando rotação na camada inferior...")
    rot_m = obter_matriz_rotacao(N, M)
    
    # Aplica rotação apenas nas colunas X e Y (índices 0 e 1) da camada inferior
    # Transpomos (.T) para multiplicar corretamente: (2x2) @ (2xN)
    coords_bottom[:, :2] = (rot_m @ coords_bottom[:, :2].T).T

    # 3. Preparação para Filtragem (Recorte)
    print(f"Lendo vetores de base de {ARQUIVO_TEMPLATE}...")
    vetores_base = ler_vetores_base(ARQUIVO_TEMPLATE)
    v1, v2 = vetores_base[0], vetores_base[1]
    v3, v4 = -v1, -v2 # Vetores opostos para fechar o paralelogramo

    # Identifica limites de Z para definir os planos de corte
    z_top_ref = np.max(coords[:, 2])
    z_bottom_ref = np.min(coords[:, 2])

    # Pontos de origem para o recorte (W, W, Z)
    p_origem_top = np.array([W_OFFSET, W_OFFSET, z_top_ref])
    p_origem_bot = np.array([W_OFFSET, W_OFFSET, z_bottom_ref])

    atomos_finais = []

    # 4. Filtragem dos Átomos
    print("Recortando célula unitária (pode levar alguns segundos)...")
    
    # Verificando camada superior
    for atomo in coords_top:
        if esta_dentro_da_celula(atomo, p_origem_top, v1, v2, v3, v4):
            atomos_finais.append(atomo)
            
    # Verificando camada inferior (rotacionada)
    for atomo in coords_bottom:
        if esta_dentro_da_celula(atomo, p_origem_bot, v1, v2, v3, v4):
            atomos_finais.append(atomo)

    atomos_finais = np.array(atomos_finais)
    num_atomos_final = len(atomos_finais)

    print(f"Recorte concluído. Átomos na célula unitária: {num_atomos_final}")

    # 5. Escrita do Arquivo Final
    print(f"Gerando {ARQUIVO_SAIDA}...")
    with open(ARQUIVO_SAIDA, 'w') as f:
        f.write('13_rotated_graphene_generated\n')
        f.write('1.0\n')
        # Escreve os vetores de base lidos do template
        np.savetxt(f, vetores_base, fmt='%12.11f', delimiter='\t')
        f.write('\tC\n')
        f.write(f'\t{num_atomos_final}\n')
        f.write('Cartesian\n')
        np.savetxt(f, atomos_finais, fmt='%12.11f', delimiter='\t')

    print("Concluído com sucesso.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
