# Mapa de Calor: Região AWS x Protocolo de Transporte
set terminal pngcairo size 1432,1030 enhanced font "Verdana,21"
set output 'grafico_heatmap_regiao_aws.png'

set title "Distribuição de Tráfego IBR por Região AWS e Protocolo"
set xlabel "Protocolo"
set ylabel "Região AWS (Alvo da Radiação)"

unset key
set palette defined ( 0 '#f7fbff', 0.5 '#6baed6', 1 '#08306b' )
set cblabel "Contagem de Pacotes" offset 2,0
set format cb "%.1t×10^{%T}"

set lmargin 20
set rmargin 12
set tmargin 3
set bmargin 5

set datafile separator comma
plot 'aws_region_protocol_heatmap.dat' matrix rowheaders columnheaders using 1:2:3 with image
set datafile separator

print "Gráfico 'grafico_heatmap_regiao_aws.png' gerado com sucesso!"
