# Pipeline Gnuplot para Análise de Radiação de Fundo da Internet (IBR)

Ramificação de geração automatizada de visualizações do *pipeline* de análise de IBR do projeto
Cloud Telescope, desenvolvida como parte do Trabalho de Conclusão de Curso de Matheus Baron
Lauritzen (Ciência da Computação, UNIVALI), sob orientação do Prof. Fabricio Bortoluzzi.

Este repositório estende as etapas 3 a 5 do *pipeline* original
([bortoluzzi/ibr-etl](https://github.com/bortoluzzi/ibr-etl)): a etapa de sumarização
(`3_summarize_radiation.py`) passa a exportar também os dados agregados em JSON, e as etapas 4 e 5
(antes dedicadas a geração de consultas Cypher e importação em MySQL) são reaproveitadas para
converter esse JSON em arquivos `.dat` e renderizá-los automaticamente com o Gnuplot, produzindo o
conjunto completo de 25 visualizações sem qualquer intervenção manual.

## Requisitos

- Python 3 com as dependências listadas em `requirements.txt` (`pip install -r requirements.txt`)
- [Gnuplot](http://www.gnuplot.info/) 6.x com o terminal `pngcairo`
- Um arquivo `output.csv` enriquecido, produzido pelas etapas 1 e 2 do
  [pipeline original](https://github.com/bortoluzzi/ibr-etl) (captura via TShark e enriquecimento
  geográfico/AWS)

## Como executar

```bash
# 1-2. Captura e enriquecimento: ver bortoluzzi/ibr-etl
#      (produz o output.csv consumido pela etapa 3 abaixo)

# 3. Sumarização, gera summaries.json e tabelas em LaTeX
python3 3_summarize_radiation.py < output.csv > output.tex

# 4. Converte summaries.json nos arquivos .dat esperados pelos scripts Gnuplot
python3 4_generate_gnuplot_dat.py

# 5. Executa todos os scripts .plt e gera o conjunto completo de PNGs
python3 5_generate_graphics.py
```

Cada etapa é independente e desacoplada: o conjunto de gráficos pode ser regenerado a qualquer
momento a partir de `summaries.json`, sem reprocessar o `output.csv` original.

## Estrutura do repositório

- `3_summarize_radiation.py`, `4_generate_gnuplot_dat.py`, `5_generate_graphics.py` — as três
  etapas do *pipeline* modificado
- `mask_geo_points.py` — filtra pontos geográficos sobre o oceano antes da renderização do mapa de
  calor (invocado automaticamente pelo Gnuplot via `system()`)
- `gerar_grafico_*.plt` — os 25 *scripts* Gnuplot, um por visualização
- `*.png` — exemplo do resultado de cada *script*, gerado sobre o Dataset~3 do Cloud Telescope
- `world_50m.dat`, `ne_50m_admin_0_countries.geojson` — dados geográficos de referência (contorno
  continental), usados pelo mapa de calor geográfico

## Contexto acadêmico

A descrição completa da metodologia, o critério de seleção dos 25 gráficos entre os estilos
oferecidos pelo Gnuplot, e a discussão de cada resultado estão documentados no TCC correspondente:

> LAURITZEN, Matheus Baron. **Desenvolvimento de um Pipeline Gnuplot para Análise de Eventos em
> Radiação de Fundo da Internet**. Trabalho de Conclusão de Curso (Graduação em Ciência da
> Computação) — Universidade do Vale do Itajaí, Itajaí, 2026. Disponível em:
> [`TCC_Matheus_Baron_Lauritzen.pdf`](./TCC_Matheus_Baron_Lauritzen.pdf).
