"""
Módulo de workers para paralelizar a formatação das imagens
e a extração de textura/segmentação (reduz o tempo de
processamento para quantidades massivas de imagens).
"""



import os
import cv2
from src.images import format_images, segment_image, paint_image
from src.filters import apply_filters

def format_worker(file, src_dir, dst_dir):
    """
    Worker para paralelizar a formatação das imagens.
    
    :param file: Nome do arquivo da imagem
    :param src_dir: Diretório de origem das imagens
    :param dst_dir: Diretório de destino das imagens processadas

    :return: Mensagem de sucesso ou erro
    """
    src = os.path.join(src_dir, file)
    dst = os.path.join(dst_dir, file)
    if format_images(src, dst):
        return f" [INFO] {file} formatada com sucesso"

    return f" [ERRO] Falha ao processar {file}"

def segment_worker(file, dst_dir, segmented_dir, filters):
    """
    Worker para paralelizar a extração de textura e segmentação.

    :param file: Nome do arquivo da imagem
    :param dst_dir: Diretório de destino das imagens processadas
    :param segmented_dir: Diretório de destino das imagens segmentadas
    :param filters: Lista de filtros a serem aplicados

    :return: Mensagem de sucesso ou erro
    """
    img_path = os.path.join(dst_dir, file)
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        return f"[ERRO] Falha ao ler a imagem '{file}'. Verifique se o arquivo está corrompido."

    features, positions = apply_filters(img_gray, filters)
    labels = segment_image(features, k=4)
    segmented_img = paint_image(img_gray, positions, labels)

    caminho_salvar = os.path.join(segmented_dir, "seg_" + file)
    cv2.imwrite(caminho_salvar, segmented_img)

    return f"[INFO] Concluído: {file}"
