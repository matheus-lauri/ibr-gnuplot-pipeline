# Distribuição de Protocolos de Transporte por País de Origem (Top 20, barras agrupadas)
set terminal pngcairo size 1432,716 enhanced font "Verdana,21"
set output 'grafico_source_country_agrupado.png'

set title "Distribuição de Protocolos de Transporte por País de Origem (Top 20)"
set xlabel "País de Origem"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"

set style data histograms
set style histogram clustered gap 1
set style fill solid 0.85 border -1
set boxwidth 0.9

set key outside top center horizontal
set lmargin 14
set bmargin 9
set xtics rotate by -45

set datafile separator comma
plot 'source_country_protocol_grouped.dat' using 2:xtic(1) title 'TCP' lc rgb '#3182bd', \
     '' using 3 title 'UDP' lc rgb '#fd8d3c', \
     '' using 4 title 'ICMP' lc rgb '#31a354'
set datafile separator

print "Gráfico 'grafico_source_country_agrupado.png' gerado com sucesso!"
