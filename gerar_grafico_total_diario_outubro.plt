# Total diário de pacotes de radiação IBR em outubro de 2023, no mesmo estilo
# do gráfico manual do grupo de pesquisa (barras, eixo Y em números simples)
set terminal pngcairo size 1800,600 enhanced font "Verdana,22"
set output 'grafico_total_diario_outubro.png'

set xdata time
set timefmt "%Y-%m-%d"
set xrange ["2023-10-01":"2023-11-01"]
set format x "%Y-%m-%d"
set xtics "2023-10-01", 86400*4
set xtics rotate by 0
set format y "%.0f"
set yrange [0:*]

set title "Total Diário de Pacotes de Radiação IBR — Outubro de 2023"
set xlabel "Dia"
set ylabel "Qtd. de pacotes"

set style fill solid 0.9 border -1
set boxwidth 70000 absolute
unset key
set grid ytics
set lmargin 13
set bmargin 5

plot 'daily_total.dat' using 1:2 with boxes lc rgb '#1f77b4'

print "Gráfico 'grafico_total_diario_outubro.png' gerado com sucesso!"
