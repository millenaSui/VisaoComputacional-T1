# TA01 - Visão Computacional (Texturas)

A aplicação foi projetada para receber imagens comuns, padronizá-las para um formato específico (dimensão 512x512 em *grayscale*), extrair informações avançadas sobre seus padrões visuais (texturas) por meio de filtros matemáticos e, em seguida, agrupar áreas semelhantes da imagem usando a técnica K-Means.

O objetivo principal do sistema é identificar, separar e destacar diferentes regiões de uma imagem com base na sua textura (como presença de bordas, linhas, barras ou pontos), em vez de se basear apenas nas cores dos pixels.

## Fluxo

O fluxo de trabalho da aplicação é dividido em cinco etapas:

- **Pré-Processamento:** Imagens (.png, .jpg ou .jpeg) presentes no diretório `./images/raw/` (a partir do diretório raiz do projeto) sofrem um crop quadrado a partir de seu centro, redimensionamento para 512x512, convertidas para *grayscale* e armazenadas no diretório `./images/processed/`
- **Construção do Banco de Filtros:** É construída uma estrutura com 24 filtros, sendo 8 tipos e orientações diferentes aplicados em 3 escalas logarítmicas, sendo eles: Filtros de borda (Gabor antissimétricos nas angulações 0, 45, 90 e 135), filtros de barras (Gabor simétricos nas angulações 0, 45 e 90) e filtros de pontos (Laplaciano do Gaussiano)
- **Extração de Características:** Os filtros são aplicados nas imagens pré-processadas de forma que, essas sejam divididas em janelas de 8x8 pixels (não sobrepostos), para cada uma delas calcula-se a média do valor absoluto da aplicação dos filtros e cada uma delas passa a ser representada por um vetor de 24 dimensões com as características de textura
- **Segmentação:** As características sofrem uma normalização estatística, aplica-se K-means para dividir blocos em 4 grupos e cada bloco recebe um rótulo (indicando a qual dos 4 padrões de textura pertencem)
- **Geração da Imagem Final:** Cada bloco de 8x8 pixels recebe uma cor sólida correspondente ao seu grupo, é feita uma sobreposição mesclando essas cores sobre a imagem original em *grayscale* e a imagem segmentada resultante é salva no diretório `./images/segmented/`

## Execução

Devido às dependências de sistema exigidas pelo `OpenCV` (como as bibliotecas nativas `libgl1` e `libglib2.0-0`), a aplicação foi conteinerizada via *Docker*. Isso garante um ambiente de execução isolado e reprodutível, eliminando a necessidade de configurar o ambiente *Python* ou instalar pacotes de sistema na máquina *host*.

Para executar o projeto (no diretório raiz do projeto e com a ferramenta *Docker* devidamente instalada):

```bash
docker build -t ta01-visao-computacional .
docker run --rm -v $(pwd)/images:/app/images ta01-visao-computacional
```

Caso queira rodar o projeto sem utilizar conteinerização, basta executar (no diretório raiz do projeto):
```bash
python3 main.py
```
