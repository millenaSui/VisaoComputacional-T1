
import os

from images.preprocess import format_images

def main():
    """
    Função principal que gerencia diretórios e fluxo do programa.
    """
    src_dir = "images/raw" # imagens originais (sem pré-processamento)
    dst_dir = "images/processed" # imagens pré-processadas (512x512, grayscale)
    
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dst_dir, exist_ok=True)
    
    arquivos_origem = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not arquivos_origem:
        print(f"[ERRO] Nenhuma imagem encontrada na pasta '{src_dir}'. Adicione as imagens e rode novamente.")
        return

    # pré-processamento das imagens
    for arquivo in arquivos_origem:
        src = os.path.join(src_dir, arquivo)
        dst = os.path.join(dst_dir, arquivo)
        if format_images(src, dst):
            print(f" -> {arquivo} formatada")

if __name__ == "__main__":
    main()