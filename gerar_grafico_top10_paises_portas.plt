# Top 10 Países de Origem da Radiação IBR, com Porta TCP Principal rotulada (Subconjunto B)
set terminal pngcairo size 1600,1000 enhanced font "Verdana,22"
set output 'grafico_top10_paises_portas.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 14
set bmargin 8

set title "Top 10 Países de Origem da Radiação IBR (Porta TCP Principal)"
set xlabel "País (Localização do IP de Origem)"
set ylabel "Contagem de Pacotes"
set format y "%.1t×10^{%T}"
set xtics rotate by -45

set datafile separator comma
stats 'top10_countries_top_ports.dat' using 2 nooutput
set yrange [0:STATS_max * 1.15]

plot 'top10_countries_top_ports.dat' using 2:xtic(1) with histograms lc rgb '#3182bd', \
     '' using 0:2:($2 > 0 ? stringcolumn(3) : "") with labels offset 0,1 font ",16" notitle
set datafile separator

print "Gráfico 'grafico_top10_paises_portas.png' gerado com sucesso!"
