# Top 20 Códigos de País de Origem da Radiação IBR, bolhas proporcionais à contagem
set terminal pngcairo size 1600,800 enhanced font "Verdana,22"
set output 'grafico_source_country_iso_bolhas.png'

stats 'top_20_source_country_iso_code.dat' using 2 nooutput
max_count = STATS_max

unset key
unset ytics
unset ylabel
set yrange [-1:1.5]
set xrange [-1:20]
set xtics rotate by -45
set bmargin 7
set tmargin 3

set title "Top 20 Códigos de País de Origem da Radiação IBR"
set xlabel "Código de País (ISO)"

plot 'top_20_source_country_iso_code.dat' using 0:(0):(0.42*sqrt($2/max_count)):xtic(1) with circles lc rgb '#e6550d' fs solid 0.65 border -1 notitle, \
     '' using 0:(0.42*sqrt($2/max_count)+0.12):(sprintf("%.1f×10^{%d}", $2/(10**floor(log10($2))), floor(log10($2)))) with labels left rotate by 55 font ",15" notitle

print "Gráfico 'grafico_source_country_iso_bolhas.png' gerado com sucesso!"
