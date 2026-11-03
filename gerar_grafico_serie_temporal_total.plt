# Série temporal: total de pacotes de radiação IBR por dia

set terminal pngcairo size 1500,750 enhanced font "Verdana,22"
set output 'grafico_serie_temporal_total.png'

set title "Pacotes de Radiação IBR por Dia (Total)"
set xlabel "Data"
set ylabel "Contagem de Pacotes"
set grid ytics

set xdata time
set timefmt "%Y-%m-%d"
set format x "%b/%y"
set xtics rotate by -45
set lmargin 13
set rmargin 6
set bmargin 6

set format y "%.1t×10^{%T}"

unset key
plot 'daily_total.dat' using 1:2 with lines lw 2 lc rgb '#b2182b'

print "Gráfico 'grafico_serie_temporal_total.png' gerado com sucesso!"
