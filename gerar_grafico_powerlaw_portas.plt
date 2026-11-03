# Distribuição de Pacotes por Porta TCP de Destino (cauda pesada, escala log-log, bins logarítmicos)
set terminal pngcairo size 1342,959 enhanced font "Verdana,22"
set output 'grafico_powerlaw_portas.png'

set title "Distribuição de Pacotes Recebidos por Porta TCP de Destino"
set xlabel "Pacotes Recebidos por Porta TCP"
set ylabel "Quantidade de Portas TCP"

set logscale xy
set format x "10^{%T}"
set format y "10^{%T}"

set lmargin 14
set bmargin 6
set grid xtics ytics

plot 'tcp_port_powerlaw.dat' using 1:2 with points pt 7 ps 1.2 lc rgb '#31a354' notitle

print "Gráfico 'grafico_powerlaw_portas.png' gerado com sucesso!"
