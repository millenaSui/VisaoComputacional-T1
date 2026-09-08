
import os

from images.preprocess import format_images
from filters.filters import build_filters, apply_filters

def main():
    """
    Função principal que gerencia diretórios e fluxo do programa.
    """
    src_dir = "images/raw" # imagens originais (sem pré-processamento)
    dst_dir = "images/processed" # imagens pré-processadas (512x512, grayscale)
    
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dst_dir, exist_ok=True)
    
    origin_files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not origin_files:
        print(f"[ERRO] Nenhuma imagem encontrada na pasta '{src_dir}'. Adicione as imagens e rode novamente.")
        return

    # pré-processamento das imagens
    for file in origin_files:
        src = os.path.join(src_dir, file)
        dst = os.path.join(dst_dir, file)
        if format_images(src, dst):
            print(f" [INFO] {file} formatada com sucesso")

    filters = build_filters()

    # extração de textura em cada imagem
    for file in os.listdir(dst_dir):
        img_path = os.path.join(dst_dir, file)
        img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        if img_gray is None:
            print(f"[ERRO] Falha ao ler a imagem '{file}'. Verifique se o arquivo está corrompido.")
            continue
            
        features, positions = apply_filters(img_gray, filters)

if __name__ == "__main__":
    main()