# RentSmart — Sistema de Orçamento de Locação 
R.M Imóveis

Aplicação desenvolvida em Python utilizando Programação Orientada a Objetos (POO) para automatizar o cálculo de orçamentos de locação da **R.M Imóveis**, aplicar regras comerciais e gerar a projeção de pagamentos dos primeiros 12 meses em arquivo CSV.

## Funcionalidades
- Cálculo de aluguel mensal para **Apartamento**, **Casa** e **Estúdio**.
- Aplicação automática de adicionais por quantidade de quartos e vagas de estacionamento.
- Desconto de 5% para clientes de apartamento que não possuem crianças (aplicado após os adicionais).
- Cálculo separado da taxa contratual de R$ 2.000,00 com parcelamento de 1x a 5x.
- Validação de todas as entradas do usuário no terminal.
- Exportação automática do arquivo `projecao_12_meses.csv` com a projeção detalhada do primeiro ano.

## Estrutura do Projeto
- `main.py`: código-fonte principal com as classes (`Imovel`, `Apartamento`, `Casa`, `Estudio` e `OrcamentoLocacao`), validações e interface via terminal.
- `projecao_12_meses.csv`: arquivo gerado após a execução contendo a projeção mensal dos 12 meses.

## Como Executar
1. Certifique-se de ter o **Python 3.10+** instalado em sua máquina.
2. Clone ou baixe este repositório e abra a pasta no terminal.
3. Execute o comando:
   ```bash
   python main.py

R.M Imóveis