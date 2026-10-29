# Top 20 Portas UDP Mais Frequentes no Tráfego IBR
set terminal pngcairo size 1500,950 enhanced font "Verdana,22"
set output 'grafico_top_20_portas_udp.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 13
set bmargin 5

set title "Top 20 Portas UDP Mais Frequentes no Tráfego IBR"
set xlabel "Porta de Destino UDP"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"
set xtics rotate by -45

plot 'top_20_udp_ports.dat' using 2:xtic(1) with histograms

print "Gráfico 'grafico_top_20_portas_udp.png' gerado com sucesso!"
