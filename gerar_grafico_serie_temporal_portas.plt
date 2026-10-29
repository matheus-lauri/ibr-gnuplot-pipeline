# Série temporal: pacotes por dia nas portas TCP 10000/10001/10002

set terminal pngcairo size 1800,900 enhanced font "Verdana,22"
set output 'grafico_serie_temporal_portas.png'

set title "Pacotes de Radiação IBR por Dia - Portas TCP 10000/10001/10002"
set xlabel "Data"
set ylabel "Contagem de Pacotes"
set grid ytics
set key top right

set xdata time
set timefmt "%Y-%m-%d"
set format x "%b/%y"
set xtics rotate by -45
set lmargin 13
set bmargin 6

set format y "%.1t×10^{%T}"

plot 'daily_tracked_ports.dat' using 1:2 with lines lw 2 lc rgb '#1a9850' title 'Porta 10000', \
     '' using 1:3 with lines lw 2 lc rgb '#fee08b' title 'Porta 10001', \
     '' using 1:4 with lines lw 2 lc rgb '#d73027' title 'Porta 10002'

print "Gráfico 'grafico_serie_temporal_portas.png' gerado com sucesso!"
