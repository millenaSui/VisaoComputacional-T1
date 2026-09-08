"""
Módulo de pré-processamento de imagens para que se
enquadrem no padrão estabelecido para o dataset:
    - Tamanho: 512x512
    - Escala de cinza
"""
import cv2

def format_images(src_path, dst_path):
    """
    Lê a imagem, cropa para o tamanho 512x512 no centro, converte para 
    escala de cinza (grayscale) e salva no diretório de destino.

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
        
        # se a imagem for menor que 512, redimensiona primeiro mantendo a proporção
        if h < 512 or w < 512:
            escala = max(512/h, 512/w)
            img = cv2.resize(img, (int(w * escala), int(h * escala)))
            h, w = img.shape[:2]
            
        # recorte central (512x512)
        cy, cx = h // 2, w // 2
        cropped = img[cy-256 : cy+256, cx-256 : cx+256]
        
        # converte para grayscale
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

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
