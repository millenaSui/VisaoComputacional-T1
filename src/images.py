"""
Módulo de processamento de imagens:
- Modifica para que se enquadrem no padrão estabelecido para o dataset:
    - Tamanho: 512x512
    - Escala de cinza
- Cropa o maior quadrado possível no centro da imagem
- Segmenta a imagem em blocos 16x16, extrai características de textura e aplica
  K-Means para agrupar regiões semelhantes
- Pinta a imagem segmentada com cores diferentes
"""

import cv2
import numpy as np
from src.filters import WINDOW_SIZE

def format_images(src_path, dst_path):
    """
    Lê a imagem, cropa o maior quadrado possível no centro, redimensiona
    para 512x512, converte para escala de cinza e salva no destino.

    :param src_path: Caminho da imagem original
    :param dst_path: Caminho da imagem processada
    
    :return: True se a imagem foi processada com sucesso, False caso contrário
    """
    print(f"[INFO] Processando imagem: {src_path}")
    try:
        img = cv2.imread(src_path)
        if img is None:
            print(f"[ERRO] Falha ao ler a imagem '{src_path}'")
            return False
        
        h, w = img.shape[:2]

        # define o tamanho do maior quadrado possível (a menor dimensão da imagem)
        min_dim = min(h, w)

        # calcula os pontos de início para centralizar o recorte
        start_y = (h - min_dim) // 2
        start_x = (w - min_dim) // 2

        # cropa o maior quadrado central (para pegar uma boa dimensão da imagem)
        square_img = img[start_y : start_y + min_dim, start_x : start_x + min_dim]

        # redimensiona o quadrado para 512x512 (INTER_AREA)
        resized_img = cv2.resize(square_img, (512, 512), interpolation=cv2.INTER_AREA)

        # converte para grayscale
        gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    except Exception as e:
        print(f"[ERRO] Falha ao processar a imagem '{src_path}': {e}")
        return False

    try:
        # salva a imagem processada
        print(f"[INFO] Salvando imagem processada em: {dst_path}")
        cv2.imwrite(dst_path, gray)
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao salvar a imagem processada '{dst_path}': {e}")
        return False

def segment_image(features, threshold=None):
    """
    Segmenta a imagem com base nas características extraídas
    usando distância euclidiana para agrupar regiões semelhantes.

    :param features: Vetor de características extraídas (N x 24)
    :param threshold: Limite de distância para definir os grupos.
                      Se None, utiliza um valor padrão.
    :return: labels (rótulos de cada bloco após o agrupamento)
    """

    # normaliza as características para média 0 e desvio padrão 1
    features_norm = (features - np.mean(features, axis=0)) / (np.std(features, axis=0) + 1e-8)

    # limite de distância padrão
    if threshold is None:
        threshold = 4.0

    protos = [] # representantes de cada grupo
    labels = [] # rotulos região
    sums = [] # somas para atualizar os representantes
    qtd = [] # quantidade de membros em cada grupo
    MAX_GRUPOS = 4

    # percorre cada vetor de características
    for vet in features_norm:
        # cria o primeiro grupo
        if len(protos) == 0:
            protos.append(vet.copy())
            sums.append(vet.copy())
            qtd.append(1)
            labels.append(0)
            continue

        # calcula a distância euclidiana do vetor para o representante de cada grupo
        dist = [np.linalg.norm(vet - proto) for proto in protos]
        closest_proto = int(np.argmin(dist))
        closest_dist = dist[closest_proto]

        # coloca o vetor no grupo suficientemente proximo
        if closest_dist <= threshold:
            labels.append(closest_proto)

            # atualiza soma e quantidade
            sums[closest_proto] += vet
            qtd[closest_proto] += 1

            # atualiza representantes
            protos[closest_proto] = (sums[closest_proto] / qtd[closest_proto])

        elif len(protos) < MAX_GRUPOS:
            new_proto = len(protos)

            protos.append(vet.copy())
            sums.append(vet.copy())
            qtd.append(1)

            labels.append(new_proto)

        else:
            labels.append(closest_proto)

            # atualiza soma e quantidade
            sums[closest_proto] += vet
            qtd[closest_proto] += 1

            # atualiza representantes
            protos[closest_proto] = (sums[closest_proto] / qtd[closest_proto])

    return np.array(labels)

def paint_image(img_gray, posicoes, labels):
    """
    Pinta os blocos 16x16 com base nos rótulos definidos pelo agrupamento
    e gera a imagem final com sobreposição (overlay)

    :param img_gray: Imagem original em escala de cinza
    :param posicoes: Lista de posições (y, x) dos blocos 16
    :param labels: Rótulos de cada bloco após o agrupamento

    :return: Imagem final com sobreposição das cores
    """
    # dicionário de cores para os K=6 grupos
    cores = [
        (255, 0, 0), # azul
        (0, 255, 255), # amarelo
        (0, 255, 0), # verde
        (0, 0, 255) # vermelho
    ]

    out_map = np.zeros((img_gray.shape[0], img_gray.shape[1], 3), dtype=np.uint8)

    tamanho_janela = WINDOW_SIZE
    for (y, x), label in zip(posicoes, labels):

        if label < 0 or label >= len(cores):
            print(f"[ERRO] Label inválido: {label}. Número de cores: {len(cores)}")
            label = label % len(cores)

        out_map[y:y+tamanho_janela, x:x+tamanho_janela] = cores[label]

    # sobreposição para visualizar o resultado (mantem textura original)
    img_color = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    resultado = cv2.addWeighted(img_color, 0.6, out_map, 0.4, 0)

    return resultado