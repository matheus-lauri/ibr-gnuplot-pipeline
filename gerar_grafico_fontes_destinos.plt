# IPs Únicos: Origens vs. Destinos de Radiação (Unique Radiation Sources/Destinations)
set terminal pngcairo size 1105,723 enhanced font "Verdana,22"
set output 'grafico_fontes_destinos_unicos.png'

set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 14
set bmargin 5

stats 'ip_sources_destinations.dat' using 2 every ::0::0 nooutput
sources = STATS_max
stats 'ip_sources_destinations.dat' using 2 every ::1::1 nooutput
destinations = STATS_max
ratio = destinations > 0 ? sources / destinations : 0
ymax = sources > destinations ? sources : destinations

set title "IPs Únicos: Origens vs. Destinos de Radiação"
set xlabel "Categoria"
set ylabel "Quantidade de IPs Únicos"
set format y "%.1t×10^{%T}"
set yrange [0:ymax*1.3]

plot 'ip_sources_destinations.dat' using 2:xtic(1) with histograms, \
     '' using 0:($2 < ymax*0.02 ? ymax*0.04 : $2*1.03):(sprintf("%.1f×10^{%d}", $2/(10**floor(log10($2))), floor(log10($2)))) with labels notitle, \
     '' using (0.5):(ymax*1.15):(sprintf("Razão Origens/Destinos: %.2fx", ratio)) with labels font ",19" notitle

print "Gráfico 'grafico_fontes_destinos_unicos.png' gerado com sucesso!"
