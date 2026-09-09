"""
Módulo principal que gerencia diretórios e fluxo do programa,
manipula imagens e aplica filtros para extração de textura e segmentação
"""
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

from src.filters import build_filters
from src.workers import segment_worker, format_worker

def main():
    """
    Função principal que gerencia diretórios e fluxo do programa.
    """
    src_dir = "images/raw" # imagens originais (sem pré-processamento)
    dst_dir = "images/processed" # imagens pré-processadas (512x512, grayscale)
    segmented_dir = "images/segmented" # imagens segmentadas (resultado final)

    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dst_dir, exist_ok=True)
    os.makedirs(segmented_dir, exist_ok=True)

    origin_files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not origin_files:
        print(f"[ERRO] Nenhuma imagem encontrada na pasta '{src_dir}'. Adicione as imagens e rode novamente.")
        return

    # pré-processamento paralelo
    print("[INFO] Iniciando formatação paralela...")
    with ProcessPoolExecutor() as executor:
        futures_format = [executor.submit(format_worker, f, src_dir, dst_dir) for f in origin_files]
        for future in as_completed(futures_format):
            print(future.result())

    # constrói o banco com 24 filtros
    filters = build_filters()

    processed_files = os.listdir(dst_dir)

    # extração e segmentação paralelas
    print("\n[INFO] Iniciando extração e segmentação paralelas...")
    with ProcessPoolExecutor() as executor:
        # envia filtros em memória para cada processo worker
        futures_segment = [
            executor.submit(segment_worker, f, dst_dir, segmented_dir, filters)
            for f in processed_files
        ]
        for future in as_completed(futures_segment):
            print(future.result())

    print("\n[INFO] Processamento concluído. Todas as imagens foram segmentadas e salvas em 'images/segmented'.")

if __name__ == "__main__":
    main()
