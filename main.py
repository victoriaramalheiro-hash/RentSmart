import csv
import os
from abc import ABC, abstractmethod


class Imovel(ABC):
    def __init__(self, quartos: int, vagas: int):
        self.quartos = quartos
        self.vagas = vagas

    @abstractmethod
    def calcular_aluguel_bruto(self) -> float:
        pass

    def calcular_aluguel_mensal(self, possui_criancas: bool) -> float:
        return round(self.calcular_aluguel_bruto(), 2)


class Apartamento(Imovel):
    VALOR_BASE = 700.00
    ADICIONAL_QUARTO_2 = 200.00
    VALOR_VAGA = 300.00
    DESCONTO_SEM_CRIANCA = 0.05

    def calcular_aluguel_bruto(self) -> float:
        total = self.VALOR_BASE
        if self.quartos == 2:
            total += self.ADICIONAL_QUARTO_2
        total += self.vagas * self.VALOR_VAGA
        return round(total, 2)

    def calcular_aluguel_mensal(self, possui_criancas: bool) -> float:
        valor = self.calcular_aluguel_bruto()
        if not possui_criancas:
            valor *= (1 - self.DESCONTO_SEM_CRIANCA)
        return round(valor, 2)


class Casa(Imovel):
    VALOR_BASE = 900.00
    ADICIONAL_QUARTO_2 = 250.00
    VALOR_VAGA = 300.00

    def calcular_aluguel_bruto(self) -> float:
        total = self.VALOR_BASE
        if self.quartos == 2:
            total += self.ADICIONAL_QUARTO_2
        total += self.vagas * self.VALOR_VAGA
        return round(total, 2)


class Estudio(Imovel):
    VALOR_BASE = 1200.00
    PACOTE_2_VAGAS = 250.00
    VAGA_ADICIONAL = 60.00

    def calcular_aluguel_bruto(self) -> float:
        total = self.VALOR_BASE
        if self.vagas > 0:
            total += self.PACOTE_2_VAGAS
            if self.vagas > 2:
                total += (self.vagas - 2) * self.VAGA_ADICIONAL
        return round(total, 2)


class OrcamentoLocacao:
    TAXA_CONTRATUAL = 2000.00

    def __init__(self, imovel: Imovel, parcelas_taxa: int, possui_criancas: bool = True):
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa
        self.possui_criancas = possui_criancas

    @property
    def aluguel_bruto(self) -> float:
        return self.imovel.calcular_aluguel_bruto()

    @property
    def desconto_aplicado(self) -> float:
        if isinstance(self.imovel, Apartamento) and not self.possui_criancas:
            return round(self.aluguel_bruto * Apartamento.DESCONTO_SEM_CRIANCA, 2)
        return 0.00

    @property
    def valor_mensal_aluguel(self) -> float:
        return self.imovel.calcular_aluguel_mensal(self.possui_criancas)

    @property
    def valor_parcela_taxa(self) -> float:
        return round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)

    def exibir_resumo(self) -> None:
        tipo_nome = type(self.imovel).__name__
        print("\n" + "=" * 48)
        print("RENTSMART - RESUMO DO ORÇAMENTO DE LOCAÇÃO")
        print("=" * 48)
        print(f"Categoria do imóvel : {tipo_nome}")
        print(f"Quantidade de quartos: {self.imovel.quartos}")
        print(f"Quantidade de vagas  : {self.imovel.vagas}")
        if isinstance(self.imovel, Apartamento):
            print(f"Possui crianças     : {'Sim' if self.possui_criancas else 'Não'}")
        print("-" * 48)
        print(f"Aluguel bruto       : R$ {self.aluguel_bruto:.2f}")
        print(f"Desconto aplicado   : R$ {self.desconto_aplicado:.2f}")
        print(f"ALUGUEL MENSAL      : R$ {self.valor_mensal_aluguel:.2f}")
        print("-" * 48)
        print("TAXA CONTRATUAL (COBRANÇA SEPARADA)")
        print(f"Taxa total          : R$ {self.TAXA_CONTRATUAL:.2f}")
        print(f"Parcelamento        : {self.parcelas_taxa}x de R$ {self.valor_parcela_taxa:.2f}")
        print("=" * 48)

    def exportar_projecao_csv(self, nome_arquivo: str = "projecao_12_meses.csv") -> None:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(pasta_atual, nome_arquivo)
        aluguel = self.valor_mensal_aluguel
        with open(caminho_completo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow([
                "Mes",
                "Aluguel_Mensal_R$",
                "Parcela_Taxa_Contratual_R$",
                "Total_Previsto_Mes_R$",
            ])
            for mes in range(1, 13):
                parcela_mes = self.valor_parcela_taxa if mes <= self.parcelas_taxa else 0.00
                total_mes = round(aluguel + parcela_mes, 2)
                writer.writerow([
                    f"Mes {mes:02d}",
                    f"{aluguel:.2f}",
                    f"{parcela_mes:.2f}",
                    f"{total_mes:.2f}",
                ])
        print(f"\nArquivo '{caminho_completo}' gerado com sucesso!")


def ler_inteiro(mensagem: str, minimo: int, maximo: int | None = None) -> int:
    while True:
        valor_str = input(mensagem).strip()
        try:
            valor = int(valor_str)
            if valor < minimo:
                print(f"Digite um número maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um número entre {minimo} e {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite apenas um número inteiro.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim", "SIM", "S"):
            return True
        if resposta in ("n", "nao", "não", "NÃO", "N"):
            return False
        print("Responda com 'S' (sim) ou 'N' (não).")


def main() -> None:
    print("=== RentSmart — R.M Imóveis ===")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    print(" " * 30)
    opcao = ler_inteiro("Escolha a categoria do imóvel (1 a 3): ", 1, 3)
    print(" " * 30)

    if opcao in (1, 2):
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        print(" " * 30)
    else:
        quartos = 1

    vagas = ler_inteiro("Quantidade de vagas de estacionamento (0 ou mais): ", 0)
    print(" " * 30)

    possui_criancas = True
    if opcao == 1:
        possui_criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
        print(" " * 30)

    parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ", 1, 5)
    print(" " * 30)

    if opcao == 1:
        imovel: Imovel = Apartamento(quartos=quartos, vagas=vagas)
    elif opcao == 2:
        imovel = Casa(quartos=quartos, vagas=vagas)
    else:
        imovel = Estudio(quartos=quartos, vagas=vagas)

    orcamento = OrcamentoLocacao(
        imovel=imovel,
        parcelas_taxa=parcelas,
        possui_criancas=possui_criancas,
    )
    orcamento.exibir_resumo()
    orcamento.exportar_projecao_csv()


if __name__ == "__main__":
    main()