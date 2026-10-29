import subprocess
from pathlib import Path

# Diretório onde estão os scripts .plt (mesmo diretório deste script)
SCRIPT_DIR = Path(__file__).parent

def run_gnuplot(plt_file: Path) -> bool:
    """Executa um script Gnuplot. Retorna True se bem-sucedido."""
    try:
        result = subprocess.run(
            ["gnuplot", str(plt_file)],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"  [ERRO] {plt_file.name}")
            if result.stderr:
                print(f"         {result.stderr.strip()}")
            return False
        print(f"  [OK]   {plt_file.name}")
        return True
    except FileNotFoundError:
        print("Erro: 'gnuplot' não encontrado. Verifique se está instalado e no PATH.")
        raise

def main():
    plt_files = sorted(SCRIPT_DIR.glob("*.plt"))

    if not plt_files:
        print("Nenhum arquivo .plt encontrado em:", SCRIPT_DIR)
        return

    print(f"Gerando gráficos — {len(plt_files)} script(s) encontrado(s)...\n")

    sucesso = sum(run_gnuplot(f) for f in plt_files)
    falhas = len(plt_files) - sucesso

    print(f"\nConcluído: {sucesso} gerado(s), {falhas} falha(s).")

if __name__ == "__main__":
    main()
