from PIL import Image

from settings import CAMINHO_FUNDO_MENU, CAMINHO_TELA_CARREGAMENTO

with Image.open(CAMINHO_FUNDO_MENU) as gif:
    print("Quadros:", gif.n_frames)
    print("Resolução:", gif.size)
    print("Tamanho:", gif.n_frames * gif.width * gif.height * 4 / 1024 / 1024, "MB aproximados em memória")