"""
Módulo de pré-processamento de imagens para que se
enquadrem no padrão estabelecido para o dataset:
    - Tamanho: 512x512
    - Escala de cinza
"""
import cv2

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