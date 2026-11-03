# Top 20 Códigos de País de Destino da Radiação IBR (Região AWS), bolhas proporcionais à contagem
set terminal pngcairo size 1263,632 enhanced font "Verdana,22"
set output 'grafico_aws_country_code_bolhas.png'

stats 'top_20_aws_country_code.dat' using 2 nooutput
max_count = STATS_max

unset key
unset ytics
unset ylabel
set yrange [-1:1.5]
set xrange [-1:20]
set xtics rotate by -45
set bmargin 7
set tmargin 3

set title "Top 20 Códigos de País de Destino da Radiação IBR (Região AWS)"
set xlabel "Código de País (ISO)"

plot 'top_20_aws_country_code.dat' using 0:(0):(0.42*sqrt($2/max_count)):xtic(1) with circles lc rgb '#3182bd' fs solid 0.65 border -1 notitle, \
     '' using 0:(0.42*sqrt($2/max_count)+0.12):(sprintf("%.1f×10^{%d}", $2/(10**floor(log10($2))), floor(log10($2)))) with labels left rotate by 55 font ",15" notitle

print "Gráfico 'grafico_aws_country_code_bolhas.png' gerado com sucesso!"
