# Distribuição de Tipos de Pacote ICMP no Tráfego IBR (gráfico de setores)
set terminal pngcairo size 1105,978 enhanced font "Verdana,22"
set output 'grafico_icmp_tipos_pizza.png'

stats 'icmp_types_sectors.dat' using 4 nooutput
total = STATS_sum

set angles degrees
unset key
unset border
unset xtics
unset ytics
set size square
set xrange [-1.6:1.6]
set yrange [-1.6:1.6]

set title "Distribuição de Tipos de Pacote ICMP no Tráfego IBR"

set palette defined (0 '#3182bd', 1 '#6baed6', 2 '#9ecae1', 3 '#fd8d3c', 4 '#e6550d', 5 '#31a354', 6 '#74c476', 7 '#756bb1')
set cbrange [0:7]
unset colorbox
set style fill solid 1.0 border -1

plot 'icmp_types_sectors.dat' using 2:(0):($3-$2):(1):($0) with sectors lc palette notitle, \
     '' using (1.25*cos(($2+$3)/2)):(1.25*sin(($2+$3)/2)):($4/total*100 >= 1 ? sprintf("%s\n%.1f%%", stringcolumn(1), $4/total*100) : "") with labels font ",19" notitle, \
     '' using (0):(-1.5):(sprintf("Tipos com participação < 1%% omitidos do rótulo")) with labels font ",16" notitle

print "Gráfico 'grafico_icmp_tipos_pizza.png' gerado com sucesso!"
