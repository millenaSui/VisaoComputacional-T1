"""
Módulo de construção de filtros para extração de características
das imagens, sendo 24 filtros no total (8 tipos x 3 escalas):
    - Bordas: 0, 45, 90, 135 graus (Gabor antissimétrico)
    - Barras: 0, 45, 90 graus (Gabor simétrico)
    - Pontos: LoG (Laplaciano do Gaussiano)
"""

import cv2
import numpy as np

WINDOW_SIZE = 16
VETOR_ESCALAS = [0.5, 1.0, 2.0]
VETOR_ANGULOS_BORDAS = [0, 45, 90, 135]
VETOR_ANGULOS_BARRAS = [0, 45, 90]

def build_filters():
    """
    Constrói um banco com 24 filtros (8 tipos x 3 escalas)
    - Bordas: 0, 45, 90, 135 graus (Gabor antissimétrico)
    - Barras: 0, 45, 90 graus (Gabor simétrico)
    - Pontos: LoG (Laplaciano do Gaussiano)
    """
    filters = []
    escalas = VETOR_ESCALAS # escala logarítmica no desvio padrão

    print("\n[INFO] Construindo Banco de 24 Filtros (3 Escalas x 8 Orientacoes)")

    for sigma in escalas:
        ksize = int(6 * sigma) | 1 # garante tamanho do kernel ímpar
        lambd = sigma * 3 # comprimento de onda da senoide

        # bordas (Gabor com fase psi = pi/2 -> Antissimétrico)
        for angulo in VETOR_ANGULOS_BORDAS:
            print(f"[INFO] Construindo filtro Gabor (Borda) - Escala: {sigma}, Angulo: {angulo} graus")
            theta = np.deg2rad(angulo)
            kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, 1.0, psi=np.pi/2, ktype=cv2.CV_32F)
            filters.append(kernel)

        # barras (Gabor com fase psi = 0 -> Simétrico)
        for angulo in VETOR_ANGULOS_BARRAS:
            print(f"[INFO] Construindo filtro Gabor (Barras) - Escala: {sigma}, Angulo: {angulo} graus")
            theta = np.deg2rad(angulo)
            kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, 1.0, psi=0, ktype=cv2.CV_32F)
            filters.append(kernel)

        # pontos (Laplaciano do Gaussiano)
        print(f"[INFO] Construindo filtro LoG (Pontos) - Escala: {sigma}")
        # criação do grid centralizado (ex: para ksize=5, eixo vai de -2 a 2)
        meio = ksize // 2
        eixo = np.arange(-meio, meio + 1)
        xx, yy = np.meshgrid(eixo, eixo)

        # variáveis intermediárias
        r_quadrado = xx**2 + yy**2
        sigma_quad = sigma**2

        # composição da fórmula do Laplaciano do Gaussiano (LoG inversa)
        constante = -1 / (np.pi * sigma**4)
        termo_central = 1 - (r_quadrado / (2 * sigma_quad))
        exponencial = np.exp(-r_quadrado / (2 * sigma_quad))

        kernel_log = constante * termo_central * exponencial

        # normalização e armazenamento
        kernel_log -= kernel_log.mean() # garante soma zero
        filters.append(kernel_log.astype(np.float32))

    print(f"[INFO] Banco de filtros construído com sucesso. Total de filtros: {len(filters)}")

    return filters


def apply_filters(img, filters):
    """
    Aplica os 24 filtros, divide em janelas de 16x16 e retorna o vetor médio

    :param img: imagem em escala de cinza (512x512)
    :param filters: lista de filtros (24 filtros)

    :return: features (N x 24), posicoes (lista de tuplas)
    """
    results = []
    for f in filters:
        filtered = cv2.filter2D(img, cv2.CV_32F, f) # evita estouro numérico
        results.append(np.abs(filtered))

    h, w = img.shape
    w_size = WINDOW_SIZE

    features = []
    positions = []

    # blocos não sobrepostos
    for y in range(0, h, w_size):
        for x in range(0, w, w_size):
            mean_filters = []
            for res in results:
                bloco = res[y:y+w_size, x:x+w_size]
                mean_filters.append(np.mean(bloco)) # média do valor absoluto do bloco

            features.append(mean_filters) # vetor de 24 dimensões
            positions.append((y, x))

    return np.array(features), positions
