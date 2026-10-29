# --- SCRIPT GNUPLOT CORRIGIDO ---

# Define o terminal de saída como uma imagem PNG de alta qualidade
set terminal pngcairo size 1500,950 enhanced font "Verdana,22"

# Define o nome do arquivo de imagem que será gerado
set output 'grafico_top_20_portas_tcp.png'

# --- Estilo do Gráfico ---
set grid ytics
set style fill solid 0.6 border -1
unset key
set lmargin 13
set bmargin 5

# --- Títulos e Rótulos dos Eixos ---
set title "Top 20 Portas TCP Mais Frequentes no Tráfego IBR"
set xlabel "Porta de Destino TCP"
set ylabel "Contagem de Pacotes"

# Notação científica de base 10 (ex.: 5×10^7), padrão para todos os gráficos
set format y "%.1t×10^{%T}"

# Gira os rótulos do eixo X para evitar sobreposição
set xtics rotate by -45

# --- Comando de Plotagem ---
plot 'top_20_tcp_ports.dat' using 2:xtic(1) with histograms

print "Gráfico 'grafico_top_20_portas_tcp.png' gerado com sucesso!"