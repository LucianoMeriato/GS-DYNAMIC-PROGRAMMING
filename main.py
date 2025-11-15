from functools import lru_cache
from typing import List, Tuple


RegistroCompetencia = Tuple[str, int, float, int, str]


def construir_dataset_competencias() -> List[RegistroCompetencia]:
    dados: List[RegistroCompetencia] = [
        ("IA Generativa",        12, 0.0, 10, "Tecnologia"),
        ("Cibersegurança",       20, 0.0,  9, "Tecnologia"),
        ("Análise de Dados",     18, 0.0,  9, "Tecnologia"),
        ("Automação Robótica",   16, 0.0,  8, "Indústria 4.0"),
        ("Cloud Computing",      22, 0.0,  9, "Tecnologia"),
        ("UX Research",          10, 0.0,  7, "Design"),
        ("Machine Learning",     24, 0.0, 10, "Tecnologia"),
        ("Gestão Ágil",           8, 0.0,  6, "Gestão"),
        ("Liderança Humanizada",  6, 0.0,  8, "Human Skills"),
        ("Comunicação Avançada",  5, 0.0,  8, "Human Skills"),
        ("Design Thinking",       7, 0.0,  7, "Inovação"),
        ("DevOps",               16, 0.0,  8, "Tecnologia"),
        ("Blockchain",           20, 0.0,  7, "Tecnologia"),
        ("Realidade Virtual",    12, 0.0,  7, "XR"),
        ("Sustentabilidade ESG", 14, 0.0,  8, "Sustentabilidade"),
        ("Economia Verde",       11, 0.0,  7, "Sustentabilidade"),
        ("Soft Skills para IA",   9, 0.0,  8, "Human Skills"),
        ("Automação Low-Code",   10, 0.0,  7, "Indústria 4.0"),
        ("Cyber Forense",        18, 0.0,  8, "Tecnologia"),
        ("Ética Digital",         6, 0.0,  7, "Human Skills"),
    ]
    return dados


def merge_listas_por_impacto(
    esq: List[RegistroCompetencia],
    dir: List[RegistroCompetencia],
) -> List[RegistroCompetencia]:
    i = j = 0
    resultado: List[RegistroCompetencia] = []

    while i < len(esq) and j < len(dir):
        if esq[i][3] >= dir[j][3]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1

    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado


def merge_sort_por_impacto(registros: List[RegistroCompetencia]) -> List[RegistroCompetencia]:
    if len(registros) <= 1:
        return registros

    meio = len(registros) // 2
    esquerda = merge_sort_por_impacto(registros[:meio])
    direita = merge_sort_por_impacto(registros[meio:])
    return merge_listas_por_impacto(esquerda, direita)


def resolver_mochila_otimizacao_tempo(
    itens_ordenados: List[RegistroCompetencia],
    capacidade_horas: int,
):
    itens = itens_ordenados
    n = len(itens)

    @lru_cache(maxsize=None)
    def dp(indice: int, capacidade: int) -> int:
        if indice == n or capacidade <= 0:
            return 0

        nome, horas, custo, impacto, area = itens[indice]

        if horas > capacidade:
            return dp(indice + 1, capacidade)

        incluir = impacto + dp(indice + 1, capacidade - horas)
        excluir = dp(indice + 1, capacidade)

        return max(incluir, excluir)

    melhor_impacto = dp(0, capacidade_horas)
    selecionados: List[RegistroCompetencia] = []
    capacidade_restante = capacidade_horas

    for indice in range(n):
        if capacidade_restante <= 0:
            break

        nome, horas, custo, impacto, area = itens[indice]

        if horas > capacidade_restante:
            continue

        impacto_sem = dp(indice + 1, capacidade_restante)
        impacto_com = impacto + dp(indice + 1, capacidade_restante - horas)

        if impacto_com >= impacto_sem:
            selecionados.append(itens[indice])
            capacidade_restante -= horas

    horas_totais = sum(item[1] for item in selecionados)
    return melhor_impacto, selecionados, horas_totais


def imprimir_tabela(registros: List[RegistroCompetencia], colunas: List[str]) -> None:
    if not registros:
        print("(nenhum registro para exibir)")
        return

    linhas = []
    for comp, horas, custo, impacto, area in registros:
        linhas.append([
            str(comp),
            str(horas),
            f"{custo:.1f}",
            str(impacto),
            str(area),
        ])

    larguras = [len(nome) for nome in colunas]
    for linha in linhas:
        for i, valor in enumerate(linha):
            larguras[i] = max(larguras[i], len(valor))

    def formatar_linha(valores):
        return "  ".join(v.ljust(larguras[i]) for i, v in enumerate(valores))

    print(formatar_linha(colunas))
    print("  ".join("-" * larguras[i] for i in range(len(colunas))))

    for linha in linhas:
        print(formatar_linha(linha))


def gerar_relatorio_console(
    itens_ordenados: List[RegistroCompetencia],
    selecionados: List[RegistroCompetencia],
    capacidade_horas: int,
    horas_totais: int,
    impacto_total: int,
) -> None:
    colunas = ["Competencia", "Horas", "Custo", "Impacto", "Area"]

    print("=" * 70)
    print("FUTURO DO TRABALHO – PLANO DE UPSKILLING OTIMIZADO")
    print("=" * 70)
    print(f"Capacidade de horas disponível (mochila): {capacidade_horas}h\n")

    print("RANKING COMPLETO DE COMPETÊNCIAS (ordenado por impacto):\n")
    imprimir_tabela(itens_ordenados, colunas)

    print("\n" + "-" * 70)
    print("COMPETÊNCIAS SELECIONADAS PELA MOCHILA (PLANO RECOMENDADO):")
    print("-" * 70)
    if selecionados:
        imprimir_tabela(selecionados, colunas)
    else:
        print("Nenhuma competência foi selecionada dentro da capacidade definida.")

    print("\nRESUMO DA SOLUÇÃO:")
    print(f"- Horas totais utilizadas: {horas_totais}h")
    print(f"- Impacto total estimado: {impacto_total} pontos")
    print("-" * 70)
    print("Interpretação:")
    print("O algoritmo escolheu o conjunto de competências que maximiza o impacto")
    print("para o futuro do trabalho, sem ultrapassar o limite de horas disponível.")
    print("=" * 70)


def main() -> None:
    capacidade_horas = 40
    itens = construir_dataset_competencias()
    itens_ordenados = merge_sort_por_impacto(itens)

    impacto_total, selecionados, horas_totais = resolver_mochila_otimizacao_tempo(
        itens_ordenados, capacidade_horas
    )

    gerar_relatorio_console(
        itens_ordenados=itens_ordenados,
        selecionados=selecionados,
        capacidade_horas=capacidade_horas,
        horas_totais=horas_totais,
        impacto_total=impacto_total,
    )


if __name__ == "__main__":
    main()
