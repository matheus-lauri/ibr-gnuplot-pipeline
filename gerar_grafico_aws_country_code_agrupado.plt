# Distribuição de Protocolos de Transporte por Código de País de Destino AWS (Top 20, barras agrupadas)
set terminal pngcairo size 2000,1000 enhanced font "Verdana,20"
set output 'grafico_aws_country_code_agrupado.png'

set title "Distribuição de Protocolos de Transporte por País de Destino AWS (Top 20)"
set xlabel "Código de País (Região AWS)"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"

set style data histograms
set style histogram clustered gap 1
set style fill solid 0.85 border -1
set boxwidth 0.9

set key outside top center horizontal
set lmargin 14
set rmargin 16
set bmargin 9
set xtics rotate by -45

set datafile separator comma
plot 'aws_country_code_protocol_grouped.dat' using 2:xtic(1) title 'TCP' lc rgb '#3182bd', \
     '' using 3 title 'UDP' lc rgb '#fd8d3c', \
     '' using 4 title 'ICMP' lc rgb '#31a354'
set datafile separator

print "Gráfico 'grafico_aws_country_code_agrupado.png' gerado com sucesso!"
