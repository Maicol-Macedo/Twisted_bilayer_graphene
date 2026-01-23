# Twisted Bilayer Graphene (TBG) Generation Tools

![Python Version](https://img.shields.io/badge/python-3.x-blue?style=flat-square)
![VASP](https://img.shields.io/badge/VASP-Compatible-red?style=flat-square)
![Numpy](https://img.shields.io/badge/python-numpy-blue?style=flat-square)

Este repositório contém ferramentas computacionais para a modelagem e geração de estruturas de **Grafeno de Camada Dupla Torcida** (TBG).

O projeto é organizado para facilitar o estudo de diferentes ângulos de torção. Atualmente, o foco é a estrutura com ângulo $\theta \approx 13.17^\circ$ (índices $m=3, n=2$), localizada no diretório dedicado `TBG_13`.

## 📋 Funcionalidades

* **Cálculo de Parâmetros Moiré**: Determinação teórica do ângulo, tamanho da supercélula e número de átomos.
* **Geração de Célula Unitária**: Scripts específicos para recortar a célula primitiva a partir de supercélulas expandidas.
* **Compatibilidade VASP**: Geração automática de arquivos `POSCAR` prontos para simulação.

## 📂 Estrutura do Projeto

    .
    ├── condições.py          # Calculadora geral de parâmetros (ângulo, rede, átomos)
    ├── README.md             # Documentação do projeto
    └── TBG_13/               # Estudo de caso: Teta = 13.17° (m=3, n=2)
        ├── TBG_13.py            # Script de processamento geométrico específico
        ├── POSCAR_13_10_10.vasp  # Supercélula base (Input, ~7600 átomos)
        └── POSCAR_13.vasp        # Célula unitária final (Output de referência)

## 🛠 Pré-requisitos

Para executar os scripts, é necessário ter instalado:

* **Python 3.8+**
* **NumPy**

Instalação das dependências:

        pip install numpy

## 🚀 Como Utilizar

### 1. Determinação dos Parâmetros (`condições.py`)
Utilize o script na raiz para calcular as propriedades teóricas de qualquer par $(m, n)$.

        python condições.py

*Entrada Interativa:*
* **m**: Inteiro (ex: `3`)
* **n**: Inteiro (ex: `2`)
* **a**: Parâmetro de rede (ex: `2.46`)

### 2. Geração da Estrutura 13.17° (`TBG_13`)
Para gerar a célula unitária deste caso específico, você deve acessar o diretório correspondente para garantir que o script encontre os arquivos de entrada.

1.  Execute o script de processamento:

        python TBG_13.py

2.  O script lerá o `POSCAR_13_10_10.vasp`, aplicará a rotação e salvará o resultado como `POSCAR.vasp` dentro desta pasta.

> **Nota:** O script também gera um arquivo `rotacionado.xyz` para visualização rápida da estrutura recortada.

## 🔬 Fundamentação Teórica

O ângulo de torção $\theta$ é definido pelos índices inteiros $(m, n)$:

$$\cos(\theta) = \frac{m^2 + n^2 + 4mn}{2(m^2 + n^2 + mn)}$$

Para o diretório `TBG_13` ($m=3, n=2$), obtemos uma célula comensurável contendo **76 átomos**, tornando viável a aplicação de cálculos de primeiros princípios (DFT).

## 🤝 Contribuição

Sinta-se à vontade para abrir *Issues* ou enviar *Pull Requests*. Para adicionar novos ângulos, recomenda-se criar novos diretórios seguindo o padrão `TBG_XX`.

