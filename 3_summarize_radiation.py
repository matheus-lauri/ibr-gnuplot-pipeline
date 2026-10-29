import sys
import os
import json
import math
# import seaborn as sns
# import pandas as pd

count_ipsrc={}
count_ipdst={}
count_tcpdstport={}
count_tcpdstflags={}
count_udpdstport={}
count_icmptype={}
count_source_country_iso_code={}
count_source_country_name={}
count_source_city_name={}
count_aws_country_code={}
count_aws_country_name={}
count_aws_city_name={}
count_aws_region={}

count_source_country_tcp={}
count_source_country_udp={}
count_source_country_icmp={}

count_aws_country_code_tcp={}
count_aws_country_code_udp={}
count_aws_country_code_icmp={}

count_aws_region_tcp={}
count_aws_region_udp={}
count_aws_region_icmp={}

count_source_geo_bin={}
GEO_BIN_SIZE = 5  # graus de latitude/longitude por célula do grid
GEO_SENTINEL = -99  # valor de fallback do 2_enrich_csv.py quando o GeoIP falha

count_daily_total={}
count_daily_tracked_port={}
TRACKED_PORTS = {'10000', '10001', '10002'}  # portas do Ensaio 1 (série temporal)

unknowndstport=0

count_global_stats_transport={}
count_global_stats_ip_sources={}
count_global_stats_ip_destinations={}

# Novos subconjuntos (extensão do script original)
count_ipsrc_country={}            # ipsrc -> país de origem
count_source_country_top_ports={} # país de origem -> {porta TCP: contagem} (Subconjunto B)

try:
    total_bytes = os.fstat(sys.stdin.fileno()).st_size
except OSError:
    total_bytes = 0

bytes_read = 0
last_pct = -1

for line in sys.stdin:
    bytes_read += len(line)
    if total_bytes > 0:
        pct = int(bytes_read * 100 / total_bytes)
        if pct > last_pct:
            print(f"\rProcessando: {pct}%", end='', file=sys.stderr, flush=True)
            last_pct = pct

    line=line.rstrip()
    line=line.split(',')
    date=str(line[0]).split(' ')[0]
    ipsrc=str(line[1])
    ipdst=str(line[2])
    tcpdstport=str(line[3])
    tcpdstflags=str(line[4])
    udpdstport=str(line[5])
    icmptype=str(line[6])
    source_country_iso_code=str(line[7])
    source_country_name=str(line[8])
    source_city_name=str(line[9])
    try:
        source_latitude=float(line[10])
        source_longitude=float(line[11])
    except (ValueError, IndexError):
        source_latitude=None
        source_longitude=None
    aws_country_code=str(line[12])
    aws_country_name=str(line[13])
    aws_city_name=str(line[14])
    aws_region=str(line[17])

    if date in count_daily_total:
        count_daily_total[date] += 1
    else:
        count_daily_total[date] = 1

    if ipsrc in count_ipsrc:
        count_ipsrc[ipsrc] += 1
    else:
        count_ipsrc[ipsrc] = 1

    count_ipsrc_country[ipsrc] = source_country_name

    if ipdst in count_ipdst:
        count_ipdst[ipdst] += 1
    else:
        count_ipdst[ipdst] = 1

    if tcpdstport:
        if tcpdstport in count_tcpdstport:
            count_tcpdstport[tcpdstport] += 1
        else:
            count_tcpdstport[tcpdstport] = 1
        if source_country_name in count_source_country_tcp:
            count_source_country_tcp[source_country_name] += 1
        else:
            count_source_country_tcp[source_country_name] = 1
        if aws_country_name in count_aws_country_code_tcp:
            count_aws_country_code_tcp[aws_country_name] += 1
        else:
            count_aws_country_code_tcp[aws_country_name] = 1
        if aws_region in count_aws_region_tcp:
            count_aws_region_tcp[aws_region] += 1
        else:
            count_aws_region_tcp[aws_region] = 1

        country_ports = count_source_country_top_ports.setdefault(source_country_name, {})
        country_ports[tcpdstport] = country_ports.get(tcpdstport, 0) + 1

        if tcpdstflags:
            if tcpdstflags in count_tcpdstflags:
                count_tcpdstflags[tcpdstflags] += 1
            else:
                count_tcpdstflags[tcpdstflags] = 1

        if tcpdstport in TRACKED_PORTS:
            daily_port_key = f"{date}:{tcpdstport}"
            if daily_port_key in count_daily_tracked_port:
                count_daily_tracked_port[daily_port_key] += 1
            else:
                count_daily_tracked_port[daily_port_key] = 1
    elif udpdstport:
        if udpdstport in count_udpdstport:
            count_udpdstport[udpdstport] += 1
        else:
            count_udpdstport[udpdstport] = 1
        if source_country_name in count_source_country_udp:
            count_source_country_udp[source_country_name] += 1
        else:
            count_source_country_udp[source_country_name] = 1
        if aws_country_name in count_aws_country_code_udp:
            count_aws_country_code_udp[aws_country_name] += 1
        else:
            count_aws_country_code_udp[aws_country_name] = 1
        if aws_region in count_aws_region_udp:
            count_aws_region_udp[aws_region] += 1
        else:
            count_aws_region_udp[aws_region] = 1
    elif icmptype:
        if icmptype in count_icmptype:
            count_icmptype[icmptype] += 1
        else:
            count_icmptype[icmptype] = 1
        if source_country_name in count_source_country_icmp:
            count_source_country_icmp[source_country_name] += 1
        else:
            count_source_country_icmp[source_country_name] = 1
        if aws_country_name in count_aws_country_code_icmp:
            count_aws_country_code_icmp[aws_country_name] += 1
        else:
            count_aws_country_code_icmp[aws_country_name] = 1
        if aws_region in count_aws_region_icmp:
            count_aws_region_icmp[aws_region] += 1
        else:
            count_aws_region_icmp[aws_region] = 1
    else:
        unknowndstport += 1

    if source_country_iso_code in count_source_country_iso_code:
        count_source_country_iso_code[source_country_iso_code] += 1
    else:
        count_source_country_iso_code[source_country_iso_code] = 1

    if source_country_name in count_source_country_name:
        count_source_country_name[source_country_name] += 1
    else:
        count_source_country_name[source_country_name] = 1

    if source_city_name in count_source_city_name:
        count_source_city_name[source_city_name] += 1
    else:
        count_source_city_name[source_city_name] = 1

    if aws_country_code in count_aws_country_code:
        count_aws_country_code[aws_country_code] += 1
    else:
        count_aws_country_code[aws_country_code] = 1

    if aws_country_name in count_aws_country_name:
        count_aws_country_name[aws_country_name] += 1
    else:
        count_aws_country_name[aws_country_name] = 1

    if aws_city_name in count_aws_city_name:
        count_aws_city_name[aws_city_name] += 1
    else:
        count_aws_city_name[aws_city_name] = 1

    if aws_region in count_aws_region:
        count_aws_region[aws_region] += 1
    else:
        count_aws_region[aws_region] = 1

    if (source_latitude is not None and source_longitude is not None
            and source_latitude != GEO_SENTINEL and source_longitude != GEO_SENTINEL):
        lat_bin = int(source_latitude // GEO_BIN_SIZE) * GEO_BIN_SIZE
        lon_bin = int(source_longitude // GEO_BIN_SIZE) * GEO_BIN_SIZE
        geo_key = f"{lat_bin}:{lon_bin}"
        if geo_key in count_source_geo_bin:
            count_source_geo_bin[geo_key] += 1
        else:
            count_source_geo_bin[geo_key] = 1

if total_bytes > 0:
    print(file=sys.stderr)

count_global_stats_transport['TCP'] = sum(count_tcpdstport.values())
count_global_stats_transport['UDP'] = sum(count_udpdstport.values())
count_global_stats_transport['ICMP'] = sum(count_icmptype.values())

count_global_stats_transport['Unknown'] = unknowndstport
count_global_stats_ip_sources['IP Sources'] = len(count_ipsrc)
count_global_stats_ip_destinations['IP Destinations'] = len(count_ipdst)

def compute_powerlaw_bins(data_dict, num_bins=25):
    """Histograma log-binado (mesma lógica de write_powerlaw_dat em 4_generate_gnuplot_dat.py),
    calculado aqui para não precisar exportar o dict inteiro (pode ter milhões de chaves) no JSON —
    só os ~25 pontos do histograma final saem para summaries.json."""
    values = [v for v in data_dict.values() if v > 0]
    if not values:
        return []
    log_min, log_max = math.log10(min(values)), math.log10(max(values))
    if log_min == log_max:
        log_max = log_min + 1
    edges = [10 ** (log_min + (log_max - log_min) * i / num_bins) for i in range(num_bins + 1)]
    counts = [0] * num_bins
    for v in values:
        idx = min(int((math.log10(v) - log_min) / (log_max - log_min) * num_bins), num_bins - 1)
        counts[idx] += 1
    bins = []
    for i in range(num_bins):
        if counts[i] > 0:
            center = math.sqrt(edges[i] * edges[i + 1])
            bins.append([round(center, 4), counts[i]])
    return bins

count_ipsrc_powerlaw_bins = compute_powerlaw_bins(count_ipsrc)

def percentage(part, whole):
    if whole == 0:
        return 0
    else:
        res = (float(part)) / float(whole)
        return "{:.2%}".format(res)

def genout(d,cname,caption,ranking):
    print("\\newpage")
    label=str(caption)
    label=label.replace(" ","")
    label=label.lower()
    print("The " + caption + " are shown on Table " + "\\ref{tab:" + label + "}" + ":")
    print("\\begin{table}[!h]")
    print("\\begin{center}")
    print("\\caption{" + str(caption) + "}")
    print("\\label{tab:" + str(label) + "}")
    print("\\begin{tabular}{ |r|c|c| }")    
    print("\\hline")
    print("\\centering " + cname + " & " + "Count"+ " & " + "\\%" + "  \\\\")
    print("\\hline")
    result = sorted(d.items(), key=lambda x: x[1], reverse=True)
    total=sum(d.values())
    subtotal=0
    for key,value in result:
        #print(key + "," + str(value) + "," + percentage(value,total))
        print(key + " & " + f"{value:,}" + " & " + str(percentage(value,total)).replace("%","") + "  \\\\")
        subtotal+=value
        ranking-=1
        if ranking == 0:
            break
    #print("Sub-total" + "," + str(subtotal) + "," + percentage(subtotal,total))
    print("\\hline")
    print("Sub-total" + " & " + f"{subtotal:,}" + " & " + str(percentage(subtotal,total)).replace("%","") + "  \\\\")
    #print("Total" + "," + str(total) + "," + percentage(total,total))
    print("\\hline")
    print("Total" + " & " + f"{total:,}" + " & " + str(percentage(total,total)).replace("%","") + "  \\\\")
    print("\\hline")    
    print("\\end{tabular}")
    print("\\end{center}")
    print("\\end{table}")
    print()

# Global statistics
genout(count_global_stats_transport,"Protocol","Transport Layer Distribution",len(count_global_stats_transport))

# Unique IP sources and destinations
genout(count_global_stats_ip_sources,"Count","Unique Radiation Sources",len(count_global_stats_ip_sources))
genout(count_global_stats_ip_destinations,"Count","Unique Radiation Destinations",len(count_global_stats_ip_destinations))

# Traffic destined to each AWS region
genout(count_aws_region,"AWS Region","Radiation Targets (AWS Region)",26)

# Traffic destined to each country, by code, name and city name
genout(count_aws_country_code,"ISO Code","Top 20 Radiation Targets (ISO Code)",20)
genout(count_aws_country_name,"Country","Top 20 Radiation Targets (Country)",20)
genout(count_aws_city_name,"City","Top 20 Radiation Targets (City)",20)

# Traffic per source country, by code, name and city name
genout(count_source_country_iso_code,"ISO Code","Top 20 Radiation Sources (ISO Code)",20)
genout(count_source_country_name,"Country","Top 20 Radiation Sources (Country)",20)
genout(count_source_city_name,"City","Top 20 Radiation Sources (City)",20)

# TCP, UDP and ICMP rankings
genout(count_tcpdstport,"TCP Port","Top 20 TCP ports",20)
genout(count_tcpdstflags,"TCP Flags","Top 20 TCP flags combinations",20)
genout(count_udpdstport,"UDP Port","Top 20 UDP ports",20)
genout(count_icmptype,"ICMP Type","Top 5 ICMP message types",5)

genout(count_aws_region_tcp,"AWS Region","TCP Radiation Targets",26)
genout(count_aws_region_udp,"AWS Region","UDP Radiation Targets",26)
genout(count_aws_region_icmp,"AWS Region","ICMP Radiation Targets",26)

genout(count_source_country_tcp,"Country","Top 20 TCP Radiation Sources",20)
genout(count_source_country_udp,"Country","Top 20 UDP Radiation Sources",20)
genout(count_source_country_icmp,"Country","Top 20 ICMP Radiation Sources",20)

genout(count_aws_country_code_tcp,"Country","Top 20 TCP Radiation Destination",20)
genout(count_aws_country_code_udp,"Country","Top 20 UDP Radiation Destination",20)
genout(count_aws_country_code_icmp,"Country","Top 20 ICMP Radiation Destination",20)

# --- Subconjunto A: estatísticas globais unificando região AWS x protocolo ---

merged_aws_region_transport_layer = {}
for key in count_aws_region:
    tcp = count_aws_region_tcp.get(key, 0)
    udp = count_aws_region_udp.get(key, 0)
    icmp = count_aws_region_icmp.get(key, 0)
    merged_aws_region_transport_layer[key] = [tcp, udp, icmp]

print("\\newpage")
print("The Global Stats by AWS Region and Protocol are shown on Table \\ref{tab:globalstatsbyawsregionandprotocol}:")
print("\\begin{table}[!h]")
print("\\begin{center}")
print("\\caption{Global Stats by AWS Region and Protocol}")
print("\\label{tab:globalstatsbyawsregionandprotocol}")
print("\\begin{tabular}{ |r|c|c|c|c| }")
print("\\hline")
print("\\centering AWS Region & TCP & UDP & ICMP & Total  \\\\")
print("\\hline")
for key, (tcp, udp, icmp) in sorted(merged_aws_region_transport_layer.items(), key=lambda x: sum(x[1]), reverse=True):
    print(f"{key} & {tcp:,} & {udp:,} & {icmp:,} & {tcp+udp+icmp:,}  \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\end{center}")
print("\\end{table}")
print()

# --- Subconjunto B: top países de origem com as principais portas TCP ---

print("\\newpage")
print("The Top 10 Radiation Sources with Top TCP Ports are shown on Table \\ref{tab:top10radiationsourceswithtoptcpports}:")
print("\\begin{table}[!h]")
print("\\begin{center}")
print("\\caption{Top 10 Radiation Sources with Top TCP Ports}")
print("\\label{tab:top10radiationsourceswithtoptcpports}")
print("\\begin{tabular}{ |l|c|l|c| }")
print("\\hline")
print("\\centering Country & Count & Top TCP Ports & \\%  \\\\")
print("\\hline")
top10_source_country = sorted(count_source_country_name.items(), key=lambda x: x[1], reverse=True)[:10]
total_source_country = sum(count_source_country_name.values())
for key, value in top10_source_country:
    top_ports = sorted(count_source_country_top_ports.get(key, {}).items(), key=lambda x: x[1], reverse=True)[:5]
    top_ports_str = ", ".join(p for p, _ in top_ports)
    print(key + " & " + f"{value:,}" + " & " + top_ports_str + " & " + str(percentage(value, total_source_country)).replace("%","") + "  \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\end{center}")
print("\\end{table}")
print()

# Subconjunto C (comportamento de varredura) foi descartado: as estruturas
# count_scan_pairs/count_scanners causavam risco de OOM sobre os 90GB completos
# e não tinham nenhum pedido de orientação por trás. Ver memória do projeto.


# for i in count_source_country_tcp.keys():
#     merged_source_country_transport_layer[i] = {'TCP',count_source_country_tcp[i]}
# for i in count_source_country_udp.keys():
#     merged_source_country_transport_layer[i] = ['UDP',count_source_country_udp[i]]
# for i in count_source_country_icmp.keys():
#     merged_source_country_transport_layer[i] = ['ICMP',count_source_country_icmp[i]]

# print(merged_source_country_transport_layer)

#### Graph/Chart/Visualization attempts

merged_source_country_transport_layer={}

for key,value in count_source_country_name.items():
    if key in count_source_country_tcp:
        tcp = count_source_country_tcp[key]
    else:
        tcp = 0
    if key in count_source_country_udp:
        udp = count_source_country_udp[key]
    else:
        udp = 0
    if key in count_source_country_icmp:
        icmp = count_source_country_icmp[key]
    else:
        icmp = 0
    merged_source_country_transport_layer[key]=[tcp, udp, icmp]
print(merged_source_country_transport_layer)



### Graph/Chart/Visualization attempts


# data = pd.DataFrame(merged_source_country_transport_layer)
# # data = pd.DataFrame({'eu-central-2': 337, 'ap-northeast-1': 246, 'ap-south-2': 263})

# heatmap = sns.heatmap(data)
# fig = heatmap.get_figure()
# fig.savefig("heatmap_source_country_transport_layer_protocols.png")

# merged_aws_region_transport_layer={}

# for key,value in count_aws_region.items():
#     if key in count_aws_region_tcp:
#         tcp = count_aws_region_tcp[key]
#     else:
#         tcp = 0
#     if key in count_aws_region_udp:
#         udp = count_aws_region_udp[key]
#     else:
#         udp = 0
#     if key in count_aws_region_icmp:
#         icmp = count_aws_region_icmp[key]
#     else:
#         icmp = 0
#     merged_aws_region_transport_layer[key]=[tcp, udp, icmp]
# print(merged_aws_region_transport_layer)
# print(count_aws_region_tcp)
# data = pd.DataFrame(merged_aws_region_transport_layer)
# # data = pd.DataFrame({'eu-central-2': 337, 'ap-northeast-1': 246, 'ap-south-2': 263})

# heatmap = sns.heatmap(data)
# fig = heatmap.get_figure()
# fig.savefig("heatmap_aws_region_transport_layer_protocols.png")


### Dump raw variables to a dumpfile

file="summarize_radiation_dict_dump.txt"

def dumpdict(d,dn):
    with open(file, 'a') as f:
        #f.readlines
        #eof = f.tell()
        #f.seek(eof)
        f.write('\n')
        f.write('Dumping: ' + dn + '\n')
        result = sorted(d.items(), key=lambda x: x[1], reverse=True)
        total=sum(d.values())
        subtotal=0
        for key,value in result:
            #print(key + "," + str(value) + "," + percentage(value,total))
            f.write(key + " & " + f"{value:,}" + " & " + str(percentage(value,total)).replace("%","") + "  \n")
            subtotal+=value
        print("Sub-total" + " & " + f"{subtotal:,}" + " & " + str(percentage(subtotal,total)).replace("%","") + "  \n")
        print("Total" + " & " + f"{total:,}" + " & " + str(percentage(total,total)).replace("%","") + "  \n")
    f.close


dumpdict(count_ipsrc, 'count_ipsrc')
dumpdict(count_ipdst, 'count_ipdst')
dumpdict(count_tcpdstport, 'count_tcpdstport')
dumpdict(count_udpdstport, 'count_udpdstport')
dumpdict(count_icmptype, 'count_icmptype')
dumpdict(count_source_country_iso_code, 'count_source_country_iso_code')
dumpdict(count_source_country_name, 'count_source_country_name')
#dumpdict(count_source_city_name, 'count_source_city_name')
dumpdict(count_aws_country_code, 'count_aws_country_code')
dumpdict(count_aws_country_name, 'count_aws_country_name')
dumpdict(count_aws_city_name, 'count_aws_city_name')
dumpdict(count_aws_region, 'count_aws_region')

dumpdict(count_source_country_tcp, 'count_source_country_tcp')
dumpdict(count_source_country_udp, 'count_source_country_udp')
dumpdict(count_source_country_icmp, 'count_source_country_icmp')

dumpdict(count_aws_country_code_tcp, 'count_aws_country_code_tcp')
dumpdict(count_aws_country_code_udp, 'count_aws_country_code_udp')
dumpdict(count_aws_country_code_icmp, 'count_aws_country_code_icmp')

#dumpdict(unknowndstport, 'unknowndstport')

dumpdict(count_global_stats_transport, 'count_global_stats_transport')
dumpdict(count_global_stats_ip_sources, 'count_global_stats_ip_sources')
dumpdict(count_global_stats_ip_destinations, 'count_global_stats_ip_destinations')

# --- INICIO DA MODIFICAÇÃO - SALVAR DICIONÁRIOS PARA PASSO SEGUINTE ---

def save_summaries_to_json():
    """
    Salva os principais dicionários de contagem em um arquivo JSON.
    """
    print("Salvando sumarizações em formato JSON...")
    
    # Agrupa todos os dicionários que queremos salvar em um único objeto
    all_summaries = {
        "count_tcpdstport": count_tcpdstport,
        "count_tcpdstflags": count_tcpdstflags,
        "count_udpdstport": count_udpdstport,
        "count_icmptype": count_icmptype,
        "count_source_country_iso_code": count_source_country_iso_code,
        "count_source_country_name": count_source_country_name,
        "count_source_city_name": count_source_city_name,
        "count_aws_country_code": count_aws_country_code,
        "count_aws_country_name": count_aws_country_name,
        "count_aws_city_name": count_aws_city_name,
        "count_aws_region": count_aws_region,
        "count_aws_region_tcp": count_aws_region_tcp,
        "count_aws_region_udp": count_aws_region_udp,
        "count_aws_region_icmp": count_aws_region_icmp,
        "count_source_country_tcp": count_source_country_tcp,
        "count_source_country_udp": count_source_country_udp,
        "count_source_country_icmp": count_source_country_icmp,
        "count_aws_country_code_tcp": count_aws_country_code_tcp,
        "count_aws_country_code_udp": count_aws_country_code_udp,
        "count_aws_country_code_icmp": count_aws_country_code_icmp,
        "count_source_geo_bin": count_source_geo_bin,
        "count_daily_total": count_daily_total,
        "count_daily_tracked_port": count_daily_tracked_port,
        "count_global_stats_transport": count_global_stats_transport,
        "count_global_stats_ip_sources": count_global_stats_ip_sources,
        "count_global_stats_ip_destinations": count_global_stats_ip_destinations,
        "merged_aws_region_transport_layer": merged_aws_region_transport_layer,
        "count_source_country_top_ports": count_source_country_top_ports,
        "count_ipsrc_powerlaw_bins": count_ipsrc_powerlaw_bins,
    }
    
    # Define o nome do arquivo de saída
    filename = 'summaries.json'
    
    try:
        with open(filename, 'w') as f:
            json.dump(all_summaries, f, indent=4)
        print(f"Arquivo '{filename}' salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

# --- Chamada da função para salvar o JSON ---
save_summaries_to_json()

# --- FIM DA MODIFICAÇÃO ---