# Distribuição de Protocolos de Transporte (Transport Layer Distribution)
set terminal pngcairo size 1342,863 enhanced font "Verdana,22"
set output 'grafico_distribuicao_protocolos.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 12
set bmargin 5

set title "Distribuição de Protocolos de Transporte no Tráfego IBR"
set xlabel "Protocolo"
set ylabel "Porcentagem do Tráfego (%)"
set yrange [0:100]
set format y "%.0f%%"

plot 'protocol_breakdown.dat' using 2:xtic(1) with histograms, \
     '' using 0:($2+3):(sprintf("%.1f%%", $2)) with labels notitle

print "Gráfico 'grafico_distribuicao_protocolos.png' gerado com sucesso!"
