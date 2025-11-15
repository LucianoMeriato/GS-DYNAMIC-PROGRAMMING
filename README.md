# Dynamic Programming – Global Solution 2025
## Otimização de Competências para o Futuro do Trabalho

### INTEGRANTES

 Eric Darakjian - RM557082
 
 Luciano Henrique Meriato Junior - RM554546

---

A proposta é usar **Programação Dinâmica** para apoiar decisões de **upskilling/reskilling**:
dado um conjunto de competências importantes para 2030+ e um limite de horas de estudo,
o algoritmo escolhe automaticamente quais habilidades priorizar para maximizar o impacto
no futuro do trabalho.

As estruturas pedidas em aula foram implementadas com:
- ordenação recursiva (merge sort);
- uso de recursão + memoização;
- modelagem do problema como **mochila 0/1**;
- estrutura de saída com apresentação dos resultados em formato tabular.

---

## 1. Formulação do Problema (entrada, saída, objetivo)

### Entrada

- Lista de competências, cada uma contendo:
  - `Competencia` – nome da habilidade (ex.: IA Generativa, Cibersegurança, etc.);
  - `Horas` – carga horária estimada para estudar aquela competência;
  - `Custo` – custo financeiro (não utilizado na otimização principal, mas previsto na estrutura);
  - `Impacto` – impacto esperado daquela competência no futuro do trabalho (0 a 10);
  - `Area` – área temática (Tecnologia, Human Skills, Sustentabilidade etc.).
- Capacidade máxima de horas de estudo (limite da "mochila").

### Saída

- Conjunto de competências recomendadas para estudo dentro do limite de horas;
- Horas totais utilizadas;
- Impacto total obtido;
- Relatório textual com:
  - ranking completo das competências ordenadas por impacto;
  - lista final de competências escolhidas pela mochila;
  - resumo da solução (horas e impacto).

### Objetivo

Maximizar o impacto total das competências escolhidas **sem ultrapassar o limite de horas**
que o profissional tem disponível para estudar.

Este é exatamente o **Problema da Mochila (Knapsack 0/1)**, em que:
- o peso é a quantidade de **horas**;
- o valor é o **impacto** da competência no futuro do trabalho.

---

## 2. Visão Geral da Solução

1. As competências são representadas em uma **estrutura tabular** simples
   (lista de tuplas), contendo todos os campos relevantes;
2. Essa lista é ordenada por impacto utilizando **merge sort recursivo**
   (estrutura de ordenação pedida na disciplina);
3. O problema da mochila é resolvido usando **recursão + memoização
   (`functools.lru_cache`)**, maximizando o impacto dentro do limite de horas;
4. O resultado é apresentado em um relatório no console, com:
   - “tabela” completa ordenada por impacto;
   - “tabela” com as competências selecionadas;
   - resumo com horas e impacto total.

Não há dependência de bibliotecas externas (como `pandas`), o que facilita a execução
em qualquer ambiente com Python 3 instalado (inclusive o ambiente do professor).

---

## 3. Arquitetura do Projeto

Estrutura de arquivos:

```text
.
├── main.py
└── README.md
```

- `main.py` – contém todo o código da solução:
  - construção do dataset de competências;
  - implementação do merge sort recursivo;
  - implementação da mochila com recursão + memoização;
  - função auxiliar para impressão em formato tabular;
  - geração do relatório de saída;
  - função `main()` que orquestra a execução.
- `README.md` – documentação da solução (este arquivo).

---

## 4. Estruturas de Programação Dinâmica Utilizadas

### 4.1. Ordenação com Merge Sort (recursivo)

O merge sort foi escolhido por ser um algoritmo classicamente recursivo
(divide and conquer). Ele é aplicado sobre a lista de competências para
produzir um **ranking ordenado por impacto**.

Em vez de um DataFrame, o projeto utiliza uma lista de registros (tuplas),
mas a ideia é a mesma: trabalhar com uma estrutura de dados tabular
e aplicar um algoritmo de ordenação sobre ela.

### 4.2. Mochila (Knapsack) com Recursão + Memoização

O problema central é modelado como mochila 0/1:

- cada competência **entra ou não entra** no plano de estudo;
- não é permitido "meia competência" (0/1);
- a função recursiva `dp(indice, capacidade)` usa **recursão e memoização** para
  garantir boa performance mesmo com várias combinações possíveis.

O uso de `functools.lru_cache` implementa a memoização automaticamente,
guardando resultados já calculados da função recursiva e evitando recomputações
para o mesmo par `(indice, capacidade)`.

---

## 5. Funções Implementadas e Explicação

A seguir, uma descrição objetiva das principais funções criadas,
para deixar clara a função de cada parte do código.

### 5.1. `construir_dataset_competencias()`

- Constrói a lista de competências ligadas ao **futuro do trabalho**;
- Cada elemento é uma tupla com:
  `Competencia`, `Horas`, `Custo`, `Impacto`, `Area`;
- Retorna essa lista, que serve como base para ordenação e otimização.

### 5.2. `merge_listas_por_impacto(esq, dir)`

- Responsável pela etapa de **merge** do merge sort;
- Recebe duas listas de competências **já ordenadas por impacto**;
- Compara elemento a elemento (campo `Impacto`) e monta uma única lista
  ordenada do maior impacto para o menor;
- É chamada repetidamente pela função recursiva do merge sort.

### 5.3. `merge_sort_por_impacto(registros)`

- Implementa o **merge sort recursivo**:
  - caso base: lista com 0 ou 1 elemento já está ordenada;
  - caso recursivo: divide a lista ao meio, ordena cada parte e depois mescla;
- Trabalha sobre a lista de tuplas (`RegistroCompetencia`);
- Retorna uma nova lista de registros ordenada por impacto.

### 5.4. `resolver_mochila_otimizacao_tempo(itens_ordenados, capacidade_horas)`

- Função principal de **programação dinâmica**;
- Modela o problema da mochila em que:
  - peso = horas da competência;
  - valor = impacto no futuro do trabalho;
- Declara uma função interna recursiva `dp(indice, capacidade)` (decorada com `@lru_cache`):
  - se `capacidade <= 0` ou `indice` chegou ao fim da lista: retorna 0;
  - se a competência atual não cabe na capacidade restante, pula o item;
  - caso contrário, compara:
    - impacto incluindo a competência;
    - impacto sem incluir a competência;
  - retorna o **máximo** entre as duas opções;
- Depois da chamada principal `dp(0, capacidade_horas)`, faz a
  **reconstrução da solução**, percorrendo a lista ordenada e verificando
  quais itens efetivamente entraram na mochila;
- Retorna:
  - impacto total;
  - lista de competências selecionadas;
  - horas totais utilizadas.

### 5.5. Função interna `dp(indice, capacidade)`

- Representa a **transição de estado** da programação dinâmica:
  - o estado é definido pelo par `(indice, capacidade)`;
  - a decisão é incluir ou não incluir a competência atual;
- A memoização garante que cada estado é calculado apenas uma vez,
  reaproveitando resultados em chamadas futuras.

### 5.6. `imprimir_tabela(registros, colunas)`

- Função auxiliar para a **estrutura de saída**;
- Recebe uma lista de registros e os nomes das colunas;
- Calcula larguras de coluna automaticamente;
- Imprime cabeçalho, linha de separação e os valores, simulando uma
  visualização tabular semelhante a um dataframe.

### 5.7. `gerar_relatorio_console(...)`

- Responsável pela **saída do programa**;
- Imprime no console:
  - ranking completo das competências ordenadas por impacto;
  - competências selecionadas pela mochila (plano recomendado);
  - resumo com horas totais e impacto total;
  - pequena interpretação do resultado.

### 5.8. `main()`

- Função de orquestração geral;
- Etapas:
  1. monta o dataset de competências;
  2. ordena a lista por impacto usando merge sort recursivo;
  3. resolve a mochila com recursão + memoização;
  4. chama o relatório para exibir a saída no console;
- Facilita a leitura e a execução do projeto em um único ponto.

---

## 6. Tamanho da Amostra (Dataset)

O dataset foi construído com **20 competências diferentes**, cobrindo áreas como:

- Tecnologia (IA Generativa, Machine Learning, Cibersegurança, Cloud, DevOps, etc.);
- Human Skills (Liderança Humanizada, Comunicação Avançada, Ética Digital, etc.);
- Sustentabilidade (Economia Verde, Sustentabilidade ESG);
- Inovação e Indústria 4.0 (Automação Robótica, Low-Code, Realidade Virtual).

Isso atende à exigência de trabalhar com uma amostra maior, evitando
testes com apenas 5 ou 6 informações.

---

## 7. Como Executar o Projeto

### 7.1. Pré-requisitos

- Python 3.10+ instalado

Não há necessidade de instalar bibliotecas externas (`pip`, `pandas`, etc.).

### 7.2. Execução

No diretório do projeto, execute:

```bash
python main.py
```

ou, em alguns ambientes:

```bash
python3 main.py
```

A saída do programa será exibida diretamente no console/terminal.

---

## 8. Estrutura de Saída (Relatórios)

O programa gera um relatório textual com três blocos principais:

1. **Ranking completo das competências**  
   Lista ordenada por impacto, do maior para o menor.

2. **Competências selecionadas pela mochila**  
   Lista apenas com as habilidades recomendadas para estudo,
   respeitando o limite de horas definido.

3. **Resumo da solução**  
   - horas totais utilizadas;
   - impacto total acumulado;
   - breve interpretação do resultado.

Exemplo simplificado de parte da saída:

```text
FUTURO DO TRABALHO – PLANO DE UPSKILLING OTIMIZADO
======================================================
Capacidade de horas disponível (mochila): 40h

RANKING COMPLETO DE COMPETÊNCIAS (ordenado por impacto):
...

COMPETÊNCIAS SELECIONADAS PELA MOCHILA (PLANO RECOMENDADO):
...

RESUMO DA SOLUÇÃO:
- Horas totais utilizadas: 39h
- Impacto total estimado: 40 pontos
```

---
