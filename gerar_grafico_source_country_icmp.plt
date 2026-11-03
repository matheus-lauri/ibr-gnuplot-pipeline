# Top 20 Países de Origem da Radiação IBR, isolando somente pacotes ICMP
set terminal pngcairo size 1364,750 enhanced font "Verdana,20"
set output 'grafico_top_20_source_country_icmp.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 14
set rmargin 14
set bmargin 9

set title "Top 20 Países de Origem da Radiação IBR (Somente ICMP)"
set xlabel "País (Localização do IP de Origem)"
set ylabel "Contagem de Pacotes ICMP"
set format y "%.1t×10^{%T}"
set xtics rotate by -45

plot 'top_20_source_country_icmp.dat' using 2:xtic(1) with histograms lc rgb '#31a354'

print "Gráfico 'grafico_top_20_source_country_icmp.png' gerado com sucesso!"
