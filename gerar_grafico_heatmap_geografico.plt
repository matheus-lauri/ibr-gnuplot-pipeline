# Mapa de Calor Geográfico: Origem da Radiação IBR (marcadores "X" sobre
# mapa político, com máscara terra/mar via Shapely para remover pontos no oceano)

set terminal pngcairo size 4800,3000 enhanced font "Verdana,28"
set output 'grafico_heatmap_geografico.png'

# Filtra os bins de source_geo_heatmap.dat que caem no oceano
system("python3 mask_geo_points.py")

set title "Mapa de Calor Geográfico: Origem da Radiação IBR"
set xlabel "Longitude"
set ylabel "Latitude"
set xrange [-180:180]
set yrange [-60:90]
set size ratio -1
unset key

set cbrange [0:6e7]
set palette defined ( 0 '#fee6ce', 0.05 '#b2182b', 1 '#67001f' )
set cblabel "Contagem de Pacotes (Aproximada)" offset 2,0
set format cb "%.1t×10^{%T}"

plot 'world_50m.dat' using 1:2 with lines lc rgb 'black' lw 0.6 notitle, \
     'source_geo_heatmap_land.dat' using 1:2:3 with points pt 2 ps 3 lw 4 lc palette z notitle

print "Gráfico 'grafico_heatmap_geografico.png' gerado com sucesso!"
