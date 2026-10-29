# Distribuição de Pacotes por IP de Origem (cauda pesada, escala log-log, bins logarítmicos)
set terminal pngcairo size 1400,1000 enhanced font "Verdana,22"
set output 'grafico_powerlaw_fontes.png'

set title "Distribuição de Pacotes Enviados por IP de Origem"
set xlabel "Pacotes Enviados por IP"
set ylabel "Quantidade de IPs de Origem"

set logscale xy
set format x "10^{%T}"
set format y "10^{%T}"

set lmargin 14
set bmargin 6
set grid xtics ytics

plot 'source_ip_powerlaw.dat' using 1:2 with points pt 7 ps 1.2 lc rgb '#7f2704' notitle

print "Gráfico 'grafico_powerlaw_fontes.png' gerado com sucesso!"
