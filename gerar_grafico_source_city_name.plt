# Top 20 Cidades de Origem da Radiação IBR (geolocalização do IP de origem)
set terminal pngcairo size 1900,1200 enhanced font "Verdana,22"
set output 'grafico_top_20_source_city_name.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 17
set rmargin 10
set bmargin 16
set ytics 4e7

set title "Top 20 Cidades de Origem da Radiação IBR"
set xlabel "Cidade (Localização do IP de Origem)"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"
set xtics rotate by -45 font "Verdana,20"
set xrange [-0.6:21.5]

plot 'top_20_source_city_name.dat' using 2:xtic(1) with histograms

print "Gráfico 'grafico_top_20_source_city_name.png' gerado com sucesso!"
