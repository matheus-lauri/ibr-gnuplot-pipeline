# Mapa de Calor: País de Origem x Protocolo de Transporte (Top 20)
set terminal pngcairo size 1600,1150 enhanced font "Verdana,21"
set output 'grafico_heatmap_fontes_protocolo.png'

set title "Top 20 Países de Origem da Radiação IBR por Protocolo"
set xlabel "Protocolo"
set ylabel "País de Origem"

unset key
set palette defined ( 0 '#fff5eb', 0.5 '#fd8d3c', 1 '#7f2704' )
set cblabel "Contagem de Pacotes" offset 2,0
set format cb "%.1t×10^{%T}"

set lmargin 22
set rmargin 12
set tmargin 3
set bmargin 5

set datafile separator comma
plot 'source_country_protocol_heatmap.dat' matrix rowheaders columnheaders using 1:2:3 with image
set datafile separator

print "Gráfico 'grafico_heatmap_fontes_protocolo.png' gerado com sucesso!"
