# Perfil TCP/UDP/ICMP por País de Origem (Top 20, eixos paralelos - cada linha é um país)
set terminal pngcairo size 1148,954 enhanced font "Verdana,20"
set output 'grafico_source_country_paralelo.png'

set title "Perfil de Protocolo por País de Origem (Eixos Paralelos, Top 20)"

set datafile separator comma
set style data parallelaxes
set paxis 1 label "TCP"
set paxis 2 label "UDP"
set paxis 3 label "ICMP"
set paxis 1 range [0:158000000]
set paxis 2 range [0:11000000]
set paxis 3 range [0:34000000]
set for [p=1:3] paxis p tics format "%.1t×10^{%T}" font ",14"
unset key
unset ytics
set xtics ("TCP" 1, "UDP" 2, "ICMP" 3)
set tmargin 5

set palette defined (0 '#cccccc', 1 '#3182bd', 2 '#e6550d', 3 '#31a354')
unset colorbox
set cbrange [0:3]

# Legenda manual (labels coloridos), já que o estilo parallelaxes não aceita
# múltiplos grupos de linhas com key própria no mesmo "plot".
set label 1 "Estados Unidos" at screen 0.20,0.985 tc rgb '#3182bd' font ",16"
set label 2 "China" at screen 0.46,0.985 tc rgb '#e6550d' font ",16"
set label 3 "Singapura" at screen 0.63,0.985 tc rgb '#31a354' font ",16"

plot 'source_country_paralelo_colored.dat' using 2:5 with parallelaxes lc palette notitle, \
     '' using 3:5 with parallelaxes lc palette notitle, \
     '' using 4:5 with parallelaxes lc palette notitle

set datafile separator

print "Gráfico 'grafico_source_country_paralelo.png' gerado com sucesso!"
