# Distribuição de Pacotes por Região AWS (rosa adaptada - 26 "pétalas" radiais, uma por região)
set terminal pngcairo size 1077,1077 enhanced font "Verdana,20"
set output 'grafico_regiao_aws_windrose.png'

set angles degrees
unset key
unset border
unset xtics
unset ytics
set size square

stats 'aws_region_total.dat' using 2 nooutput
rmax = STATS_max * 1.15
plot_range = rmax * 1.45

set xrange [-plot_range:plot_range]
set yrange [-plot_range:plot_range]

set title "Distribuição da Radiação IBR por Região AWS (Rosa Adaptada)"

set palette defined (0 '#08306b', 0.5 '#3182bd', 1 '#9ecae1')
set cbrange [0:25]
unset colorbox
set style fill solid 0.85 border -1

petal_width = 360.0/26.0*0.82

plot 'aws_region_total.dat' using ($0*360.0/26.0 - petal_width/2):(0):(petal_width):2:($0) with sectors lc palette notitle, \
     '' using (($0*360.0/26.0 > 90 && $0*360.0/26.0 < 270) ? 1/0 : ($2+rmax*0.09)*cos($0*360.0/26.0)):(($0*360.0/26.0 > 90 && $0*360.0/26.0 < 270) ? 1/0 : ($2+rmax*0.09)*sin($0*360.0/26.0)):1:($0*360.0/26.0) with labels left rotate variable font ",20" notitle, \
     '' using (($0*360.0/26.0 > 90 && $0*360.0/26.0 < 270) ? ($2+rmax*0.09)*cos($0*360.0/26.0) : 1/0):(($0*360.0/26.0 > 90 && $0*360.0/26.0 < 270) ? ($2+rmax*0.09)*sin($0*360.0/26.0) : 1/0):1:($0*360.0/26.0-180) with labels right rotate variable font ",20" notitle

print "Gráfico 'grafico_regiao_aws_windrose.png' gerado com sucesso!"
