# TA01 - Visão Computacional (Texturas)

A aplicação foi projetada para receber imagens comuns, padronizá-las para um formato específico (dimensão $512\times512$ em *grayscale*), extrair informações avançadas sobre seus padrões visuais (texturas) por meio de filtros matemáticos e, em seguida, agrupar áreas semelhantes da imagem usando a técnica de distância euclidiana.

O objetivo principal do sistema é identificar, separar e destacar diferentes regiões de uma imagem com base na sua textura (como presença de bordas, linhas, barras ou características circulares), em vez de se basear apenas nas cores dos pixels.

## Fluxo

O fluxo de trabalho da aplicação é dividido em cinco etapas:

- **Pré-Processamento:** Imagens (`.png`, `.jpg` ou `.jpeg`) presentes no diretório `./images/raw/` (a partir do diretório raiz do projeto) sofrem um recorte (*crop*) quadrado a partir de seu centro, redimensionamento para $512\times512$ pixels utilizando interpolação de área (`cv2.INTER_AREA`), conversão para *grayscale* e armazenamento no diretório `./images/processed/`.
- **Construção do Banco de Filtros:** É construída uma estrutura com 24 filtros, sendo 8 tipos e orientações diferentes aplicados em 3 escalas logarítmicas de desvio padrão ($\sigma \in \{0.5, 1.0, 2.0\}$): filtros de borda (Gabor antissimétricos nas angulações 0\textdegree, 45\textdegree, 90\textdegree e 135\textdegree), filtros de barras (Gabor simétricos nas angulações 0\textdegree, 45\textdegree e 90\textdegree) e um filtro circular (máscara de suavização/passa-baixas em formato de disco).
- **Extração de Características:** Os 24 filtros são aplicados nas imagens pré-processadas por meio de convolução. A imagem resultante é dividida em blocos/janelas contíguas de $16\times16$ pixels (não sobrepostos) e, para cada janela, calcula-se a média do valor absoluto da resposta de cada filtro. Cada região passa a ser representada por um vetor de características com exatas 24 dimensões.
- **Segmentação:** Os vetores de características sofrem normalização estatística (Z-score), aplicando-se em seguida o algoritmo de agrupamento sequencial baseado na distância euclidiana para dividir os blocos em até 4 grupos, atribuindo a cada bloco um rótulo correspondente ao padrão de textura identificado.
- **Geração da Imagem Final:** Cada bloco de $16\times16$ pixels é pintado com uma cor sólida representativa do seu grupo (utilizando o espaço BGR/RGB: Azul, Amarelo, Verde e Vermelho). É realizada uma sobreposição ponderada (*overlay* com fator de 0.6 para a imagem original e 0.4 para a máscara de agrupamento) e a imagem segmentada final é salva no diretório `./images/segmented/`.

## Execução

Devido às dependências de sistema exigidas pelo `OpenCV` (como bibliotecas nativas de imagem e interface gráficos), a aplicação foi conteinerizada via *Docker*. Isso garante um ambiente de execução isolado e reprodutível, eliminando a necessidade de configurar manualmente o ambiente *Python* ou instalar pacotes de sistema na máquina *host*.

Para executar o projeto (no diretório raiz e com a ferramenta *Docker* devidamente instalada):

```bash
docker build -t ta01-visao-computacional .
docker run --rm -v $(pwd)/images:/app/images ta01-visao-computacional