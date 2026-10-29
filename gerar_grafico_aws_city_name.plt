# Top 20 Cidades de Destino da Radiação IBR (localização AWS do IP de destino)
set terminal pngcairo size 1500,950 enhanced font "Verdana,22"
set output 'grafico_top_20_aws_city_name.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 14
set bmargin 6

set title "Top 20 Cidades de Destino da Radiação IBR (Região AWS)"
set xlabel "Cidade (Localização do IP de Destino)"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"
set xtics rotate by -45

plot 'top_20_aws_city_name.dat' using 2:xtic(1) with histograms

print "Gráfico 'grafico_top_20_aws_city_name.png' gerado com sucesso!"
