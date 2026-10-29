import json
import math

# Deve ser igual ao GEO_BIN_SIZE definido em 3_summarize_radiation.py,
# pois é usado só para reconstruir o centro de cada célula a partir da chave "lat:lon".
GEO_BIN_SIZE = 5

def write_topn_dat(filename, data_dict, n=20, header="# Categoria Contagem"):
    """Escreve as N categorias de maior contagem em ordem decrescente."""
    with open(filename, 'w') as f:
        f.write(header + "\n")
        sorted_items = sorted(data_dict.items(), key=lambda item: int(item[1]), reverse=True)
        for category, count in sorted_items[:n]:
            # Categorias com espaço (ex.: "North Charleston") precisam de aspas,
            # senão o gnuplot separa a categoria em múltiplas colunas por whitespace.
            label = f'"{category}"' if ' ' in str(category) else category
            f.write(f"{label} {count}\n")
    print(f"Arquivo '{filename}' gerado com sucesso.")

def write_powerlaw_dat(filename, data_dict, num_bins=25, header="# valor_por_chave num_chaves"):
    """Histograma log-binado (mesmo padrão de source_ip_powerlaw.dat) da distribuição de contagens."""
    values = [int(v) for v in data_dict.values() if int(v) > 0]
    if not values:
        return
    log_min, log_max = math.log10(min(values)), math.log10(max(values))
    if log_min == log_max:
        log_max = log_min + 1
    edges = [10 ** (log_min + (log_max - log_min) * i / num_bins) for i in range(num_bins + 1)]
    counts = [0] * num_bins
    for v in values:
        idx = min(int((math.log10(v) - log_min) / (log_max - log_min) * num_bins), num_bins - 1)
        counts[idx] += 1
    with open(filename, 'w') as f:
        f.write(header + "\n")
        for i in range(num_bins):
            if counts[i] > 0:
                center = math.sqrt(edges[i] * edges[i + 1])
                f.write(f"{center:.4f} {counts[i]}\n")
    print(f"Arquivo '{filename}' gerado com sucesso.")

def write_protocol_grouped_dat(filename, tcp_dict, udp_dict, icmp_dict, n=20):
    """Formato 'categoria,TCP,UDP,ICMP' (mesmo layout de aws_region_protocol_heatmap.dat), Top-N por total."""
    totals = {}
    for d in (tcp_dict, udp_dict, icmp_dict):
        for key, count in d.items():
            totals[key] = totals.get(key, 0) + int(count)
    sorted_keys = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:n]

    with open(filename, 'w') as f:
        f.write(",TCP,UDP,ICMP\n")
        for key, _ in sorted_keys:
            tcp = int(tcp_dict.get(key, 0))
            udp = int(udp_dict.get(key, 0))
            icmp = int(icmp_dict.get(key, 0))
            f.write(f"{key},{tcp},{udp},{icmp}\n")
    print(f"Arquivo '{filename}' gerado com sucesso.")

def write_protocol_colored_dat(filename, tcp_dict, udp_dict, icmp_dict, highlight, n=20):
    """Mesmo formato de write_protocol_grouped_dat, com coluna extra ColorCode
    (0 = demais categorias, 1..N = ordem de 'highlight'). Linhas ficam ordenadas
    por ColorCode crescente para que as destacadas sejam desenhadas por cima
    das outras (usado pelo gráfico de eixos paralelos, lc palette)."""
    totals = {}
    for d in (tcp_dict, udp_dict, icmp_dict):
        for key, count in d.items():
            totals[key] = totals.get(key, 0) + int(count)
    sorted_keys = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:n]

    rows = []
    for key, _ in sorted_keys:
        tcp = int(tcp_dict.get(key, 0))
        udp = int(udp_dict.get(key, 0))
        icmp = int(icmp_dict.get(key, 0))
        code = highlight.index(key) + 1 if key in highlight else 0
        rows.append((key, tcp, udp, icmp, code))
    rows.sort(key=lambda r: r[4])

    with open(filename, 'w') as f:
        f.write(",TCP,UDP,ICMP,ColorCode\n")
        for key, tcp, udp, icmp, code in rows:
            f.write(f"{key},{tcp},{udp},{icmp},{code}\n")
    print(f"Arquivo '{filename}' gerado com sucesso.")

def generate_dat_files_from_json():
    """
    Lê o arquivo summaries.json e gera os arquivos .dat para o Gnuplot.
    """
    print("Iniciando a geração de arquivos .dat a partir do JSON...")
    
    try:
        # Carrega os dados do arquivo JSON gerado pelo script anterior
        with open('summaries.json', 'r') as f:
            all_summaries = json.load(f)
        print("Arquivo 'summaries.json' lido com sucesso.")
    except FileNotFoundError:
        print("Erro: O arquivo 'summaries.json' não foi encontrado. Execute o script '3_summarize_radiation.py' primeiro.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return

    # --- Gráfico 1: Top 20 Portas TCP ---
    try:
        filename = 'top_20_tcp_ports.dat'
        data_dict = all_summaries.get("count_tcpdstport", {})
        
        with open(filename, 'w') as f:
            f.write("# PortaTCP Contagem\n")
            sorted_items = sorted(data_dict.items(), key=lambda item: int(item[1]), reverse=True)
            
            for i, (port, count) in enumerate(sorted_items):
                if i < 20:
                    f.write(f"{port} {count}\n")
                else:
                    break
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados para as portas TCP: {e}")

    # --- Gráfico 2: Distribuição de Protocolos de Transporte ---
    try:
        filename = 'protocol_breakdown.dat'
        data_dict = all_summaries.get("count_global_stats_transport", {})
        total = sum(int(v) for v in data_dict.values())

        with open(filename, 'w') as f:
            f.write("# Protocolo Porcentagem\n")
            for protocol, count in data_dict.items():
                if protocol.lower() == 'unknown':
                    continue
                pct = (int(count) / total * 100) if total > 0 else 0
                f.write(f"{protocol} {pct:.2f}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados de protocolos: {e}")

    # --- Gráfico 3: Fontes vs Destinos Únicos de Radiação ---
    try:
        filename = 'ip_sources_destinations.dat'
        sources = all_summaries.get("count_global_stats_ip_sources", {}).get("IP Sources", 0)
        destinations = all_summaries.get("count_global_stats_ip_destinations", {}).get("IP Destinations", 0)

        with open(filename, 'w') as f:
            f.write("# Categoria Contagem\n")
            f.write(f"Sources {sources}\n")
            f.write(f"Destinations {destinations}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados de fontes/destinos: {e}")

    # --- Gráfico 4: Mapa de Calor - Região AWS x Protocolo ---
    try:
        filename = 'aws_region_protocol_heatmap.dat'
        total_dict = all_summaries.get("count_aws_region", {})
        tcp_dict = all_summaries.get("count_aws_region_tcp", {})
        udp_dict = all_summaries.get("count_aws_region_udp", {})
        icmp_dict = all_summaries.get("count_aws_region_icmp", {})

        # Ordena as regiões pela contagem total (descendente) e mantém somente
        # as 26 primeiras (mesmo corte usado pelo genout() para count_aws_region).
        # Isso descarta valores espúrios de geolocalização (ex: longitudes como
        # "-119.7257") que vazam para o campo aws_region quando o IP de destino
        # não tem uma região AWS válida mapeada — volume irrisório (1-55 pacotes)
        # frente às regiões reais (milhões), mas que o with image exibiria como
        # linhas extras no eixo Y por não haver corte de ranking nesse dicionário.
        sorted_regions = sorted(total_dict.items(), key=lambda item: int(item[1]), reverse=True)[:26]

        with open(filename, 'w') as f:
            f.write(",TCP,UDP,ICMP\n")
            for region, _ in sorted_regions:
                tcp = int(tcp_dict.get(region, 0))
                udp = int(udp_dict.get(region, 0))
                icmp = int(icmp_dict.get(region, 0))
                f.write(f"{region},{tcp},{udp},{icmp}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados do mapa de calor de região AWS: {e}")

    # --- Gráfico 5: Mapa de Calor Geográfico - Origem da Radiação (lat/lon) ---
    try:
        filename = 'source_geo_heatmap.dat'
        data_dict = all_summaries.get("count_source_geo_bin", {})

        with open(filename, 'w') as f:
            f.write("# lon lat count\n")
            for key, count in data_dict.items():
                lat_bin_str, lon_bin_str = key.split(':')
                # Centro da célula, não o canto inferior-esquerdo, para o dgrid3d
                # interpolar a partir de pontos representativos de cada bin.
                lat_center = int(lat_bin_str) + GEO_BIN_SIZE / 2
                lon_center = int(lon_bin_str) + GEO_BIN_SIZE / 2
                f.write(f"{lon_center} {lat_center} {count}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados do mapa de calor geográfico: {e}")

    # --- Gráfico 6: Série Temporal - Pacotes Totais por Dia ---
    try:
        filename = 'daily_total.dat'
        data_dict = all_summaries.get("count_daily_total", {})

        with open(filename, 'w') as f:
            f.write("# Data Contagem\n")
            for date in sorted(data_dict.keys()):
                f.write(f"{date} {data_dict[date]}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados da série temporal diária: {e}")

    # --- Gráfico 7: Série Temporal - Portas TCP 10000/10001/10002 por Dia (Ensaio 1) ---
    try:
        filename = 'daily_tracked_ports.dat'
        data_dict = all_summaries.get("count_daily_tracked_port", {})
        tracked_ports = ['10000', '10001', '10002']

        by_date = {}
        for key, count in data_dict.items():
            date, port = key.split(':')
            by_date.setdefault(date, {})[port] = int(count)

        with open(filename, 'w') as f:
            f.write("# Data Porta10000 Porta10001 Porta10002\n")
            for date in sorted(by_date.keys()):
                counts = by_date[date]
                row = [str(counts.get(p, 0)) for p in tracked_ports]
                f.write(f"{date} {' '.join(row)}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar o arquivo de dados das portas rastreadas por dia: {e}")

    # --- Gráficos 8-16: Grupo 1 - Rankings simples (Top-N genéricos) ---
    topn_specs = [
        ('top_20_aws_country_code.dat', 'count_aws_country_code', 20, '# ISOCode Contagem'),
        ('top_20_aws_city_name.dat', 'count_aws_city_name', 20, '# City Contagem'),
        ('top_20_source_country_iso_code.dat', 'count_source_country_iso_code', 20, '# ISOCode Contagem'),
        ('top_20_source_city_name.dat', 'count_source_city_name', 20, '# City Contagem'),
        ('top_20_source_country_icmp.dat', 'count_source_country_icmp', 20, '# Country Contagem'),
        ('top_20_tcp_flags.dat', 'count_tcpdstflags', 20, '# TCPFlags Contagem'),
        ('top_20_udp_ports.dat', 'count_udpdstport', 20, '# PortaUDP Contagem'),
        ('icmp_types.dat', 'count_icmptype', 8, '# ICMPType Contagem'),
    ]
    for filename, key, n, header in topn_specs:
        try:
            write_topn_dat(filename, all_summaries.get(key, {}), n=n, header=header)
        except Exception as e:
            print(f"Erro ao gerar '{filename}': {e}")

    # --- Gráfico 16b: Tipos ICMP - setores pré-computados (ângulos para 'with sectors') ---
    try:
        filename = 'icmp_types_sectors.dat'
        data_dict = all_summaries.get('count_icmptype', {})
        total = sum(int(v) for v in data_dict.values())
        sorted_items = sorted(data_dict.items(), key=lambda item: int(item[1]), reverse=True)

        with open(filename, 'w') as f:
            f.write("# ICMPType StartAngle EndAngle Contagem\n")
            angle = 0.0
            for icmp_type, count in sorted_items:
                span = (int(count) / total * 360) if total > 0 else 0
                f.write(f"{icmp_type} {angle:.3f} {angle + span:.3f} {count}\n")
                angle += span
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar 'icmp_types_sectors.dat': {e}")

    # --- Gráfico 17: Distribuição Lei de Potência - Portas TCP ---
    try:
        write_powerlaw_dat(
            'tcp_port_powerlaw.dat',
            all_summaries.get('count_tcpdstport', {}),
            header='# pacotes_por_porta num_portas'
        )
    except Exception as e:
        print(f"Erro ao gerar 'tcp_port_powerlaw.dat': {e}")

    # --- Gráfico 17b: Distribuição Lei de Potência - IPs de Origem ---
    # Bins já pré-computados em 3_summarize_radiation.py (count_ipsrc não vai pro JSON inteiro).
    try:
        filename = 'source_ip_powerlaw.dat'
        bins = all_summaries.get('count_ipsrc_powerlaw_bins', [])
        with open(filename, 'w') as f:
            f.write("# pacotes_por_ip num_ips\n")
            for center, count in bins:
                f.write(f"{center} {count}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar 'source_ip_powerlaw.dat': {e}")

    # --- Gráfico 18: Região AWS - Total (Grupo 2: radar/rosa) ---
    try:
        write_topn_dat('aws_region_total.dat', all_summaries.get('count_aws_region', {}), n=26, header='# Region Contagem')
    except Exception as e:
        print(f"Erro ao gerar 'aws_region_total.dat': {e}")

    # --- Gráficos 19-20: Grupo 3 - Trincas de protocolo (formato agrupado) ---
    try:
        write_protocol_grouped_dat(
            'source_country_protocol_grouped.dat',
            all_summaries.get('count_source_country_tcp', {}),
            all_summaries.get('count_source_country_udp', {}),
            all_summaries.get('count_source_country_icmp', {}),
            n=20
        )
    except Exception as e:
        print(f"Erro ao gerar 'source_country_protocol_grouped.dat': {e}")

    try:
        write_protocol_colored_dat(
            'source_country_paralelo_colored.dat',
            all_summaries.get('count_source_country_tcp', {}),
            all_summaries.get('count_source_country_udp', {}),
            all_summaries.get('count_source_country_icmp', {}),
            highlight=['United States', 'China', 'Singapore'],
            n=20
        )
    except Exception as e:
        print(f"Erro ao gerar 'source_country_paralelo_colored.dat': {e}")

    try:
        write_protocol_grouped_dat(
            'source_country_protocol_heatmap.dat',
            all_summaries.get('count_source_country_tcp', {}),
            all_summaries.get('count_source_country_udp', {}),
            all_summaries.get('count_source_country_icmp', {}),
            n=20
        )
    except Exception as e:
        print(f"Erro ao gerar 'source_country_protocol_heatmap.dat': {e}")

    try:
        write_protocol_grouped_dat(
            'aws_country_code_protocol_grouped.dat',
            all_summaries.get('count_aws_country_code_tcp', {}),
            all_summaries.get('count_aws_country_code_udp', {}),
            all_summaries.get('count_aws_country_code_icmp', {}),
            n=20
        )
    except Exception as e:
        print(f"Erro ao gerar 'aws_country_code_protocol_grouped.dat': {e}")


    # --- Novo Subconjunto A: estatísticas globais unificadas Região AWS x Protocolo ---
    try:
        filename = 'aws_region_global_stats.dat'
        data_dict = all_summaries.get('merged_aws_region_transport_layer', {})
        sorted_items = sorted(data_dict.items(), key=lambda item: sum(int(v) for v in item[1]), reverse=True)[:26]

        with open(filename, 'w') as f:
            f.write(",TCP,UDP,ICMP\n")
            for region, (tcp, udp, icmp) in sorted_items:
                f.write(f"{region},{tcp},{udp},{icmp}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar 'aws_region_global_stats.dat': {e}")

    # --- Novo Subconjunto B: Top 10 Países de Origem com Top 5 Portas TCP ---
    try:
        filename = 'top10_countries_top_ports.dat'
        country_totals = all_summaries.get('count_source_country_name', {})
        country_ports = all_summaries.get('count_source_country_top_ports', {})
        top10_countries = sorted(country_totals.items(), key=lambda item: int(item[1]), reverse=True)[:10]

        # Formato CSV (não espaço) porque nomes de país têm espaço (ex: "United States"),
        # e o gnuplot separa colunas por qualquer whitespace por padrão.
        with open(filename, 'w') as f:
            f.write("Country,TotalCount,Port1,Port1Count,Port2,Port2Count,Port3,Port3Count,Port4,Port4Count,Port5,Port5Count\n")
            for country, total in top10_countries:
                ports = country_ports.get(country, {})
                top5 = sorted(ports.items(), key=lambda item: int(item[1]), reverse=True)[:5]
                while len(top5) < 5:
                    top5.append(('-', 0))
                row = ",".join(f"{port},{count}" for port, count in top5)
                f.write(f"{country},{total},{row}\n")
        print(f"Arquivo '{filename}' gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar 'top10_countries_top_ports.dat': {e}")

    # Subconjunto C (comportamento de varredura) foi descartado: risco de OOM
    # sobre os 90GB completos e sem pedido de orientação por trás.


# --- Ponto de entrada do script ---
if __name__ == "__main__":
    generate_dat_files_from_json()