# Top 20 Combinações de Flags TCP no Tráfego IBR
set terminal pngcairo size 2000,1000 enhanced font "Verdana,22"
set output 'grafico_top_20_tcp_flags.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 14
set bmargin 9

set title "Top 20 Combinações de Flags TCP no Tráfego IBR"
set xlabel "Combinação de Flags TCP"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"
set xtics rotate by -45 font "Verdana,17"

plot 'top_20_tcp_flags.dat' using 2:xtic(1) with histograms

print "Gráfico 'grafico_top_20_tcp_flags.png' gerado com sucesso!"
