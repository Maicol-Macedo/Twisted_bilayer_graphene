import math  # Biblioteca usada para o cálculo do arco cosseno​

def calcular_parametros_tbg(m: int, n: int, a: float) -> tuple[float, int, float]:
    """
    Calcula os parâmetros cristalográficos do Grafeno de Camada Dupla Torcida (TBG).

    Baseado nos índices inteiros (m, n) e no parâmetro de rede do grafeno,
    calcula o ângulo de torção, número de átomos e tamanho da supercélula.

    Args:
        m (int): Primeiro índice inteiro da torção.
        n (int): Segundo índice inteiro da torção.
        a (float): Parâmetro de rede do grafeno (em Angstroms).

    Returns:
        tuple[float, int, float]: Uma tupla contendo:
            - angulo_graus (float): Ângulo de torção em graus.
            - num_atomos (int): Número total de átomos na célula unitária.
            - L (float): Parâmetro de rede da supercélula Moiré (em Angstroms).
    """
    
    # Termo comum nas fórmulas (m^2 + n^2 + mn)
    delta = m**2 + n**2 + m * n
    
    # 1. Cálculo do ângulo
    # Fórmula: cos(theta) = (m^2 + n^2 + 4mn) / (2 * delta)
    numerador_cos = m**2 + n**2 + 4 * m * n
    valor_cos = numerador_cos / (2 * delta)
    
    # Garante que o valor esteja no domínio [-1, 1] para evitar erros numéricos
    valor_cos = max(-1.0, min(1.0, valor_cos))
    
    theta_rad = math.acos(valor_cos)
    angulo_graus = math.degrees(theta_rad)

    # 2. Cálculo do número de átomos
    # Fórmula: N = 4 * delta
    num_atomos = 4 * delta

    # 3. Cálculo do parâmetro de rede da supercélula (L)
    # Simplificação: L = a * sqrt(delta)
    L = a * math.sqrt(delta)

    return angulo_graus, num_atomos, L

# Bloco de execução principal
if __name__ == "__main__":
    print("--- Calculadora de Parâmetros TBG ---")
    
    try:
        # Entradas do usuário
        m_in = int(input("Digite o valor inteiro para m (ex: 3): "))
        n_in = int(input("Digite o valor inteiro para n (ex: 2): "))
        a_in = float(input("Digite o parâmetro de rede 'a' em Å (ex: 2.46): "))

        # Chamada da função
        angulo, n_atomos, rede = calcular_parametros_tbg(m_in, n_in, a_in)

        # Exibição formatada
        print("-" * 40)
        print(f"Resultados para TBG ({m_in}, {n_in}):")
        print(f"  • Ângulo de torção (θ): {angulo:.6f}°")
        print(f"  • Número de átomos (N): {n_atomos}")
        print(f"  • Supercélula Moiré (L): {rede:.6f} Å")
        print("-" * 40)

    except ValueError:
        print("\n[Erro] Por favor, insira apenas números válidos (inteiros para m/n, decimal para a).")
    except Exception as e:
        print(f"\n[Erro] Ocorreu um erro inesperado: {e}")
