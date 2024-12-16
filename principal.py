# instale o pacote: pip install pypdf2
# instale o pacote acompanhante para imagens: pip install PyPDF2[image]
# executar este código (se estiver na pasta raiz): python .\principal.py

from pathlib import Path
from PyPDF2 import PdfReader, PageObject, PdfWriter, PdfMerger


def contar_algarismos(elementos: int) -> int:
    algarismos: int = 1
    while elementos > 10:
        elementos = int(elementos / 10)
        algarismos += 1
    return algarismos


def criar_zeros_na_frente(contador: int) -> str:
    numero: int = contador + 1
    numeroS: str = str(numero)

    while len(numeroS) < algarismos:
        troca: str = numeroS
        numeroS = "0" + troca

    return numeroS


def inverter_lista(lista: list[Path]) -> list[Path]:
    lista_invertida: list[Path] = []
    elementos = len(lista)

    for indice in range(elementos - 1, -1, -1):
        lista_invertida.append(lista[indice])

    return lista_invertida


PASTA_RAIZ: Path = Path(__file__).parent
PASTA_ORIGINAIS: Path = PASTA_RAIZ / "pdfs_originais"
PASTA_NOVA: Path = PASTA_RAIZ / "arquivos_novos"
NOME_ARQUIVO_PDF = "Epson L365.pdf"
CAMINHO_ARQUIVO: Path = PASTA_ORIGINAIS / NOME_ARQUIVO_PDF

PASTA_NOVA.mkdir(exist_ok=True)

leitor: PdfReader = PdfReader(CAMINHO_ARQUIVO)

paginas: list[PageObject] = leitor.pages

for c, pagina in enumerate(paginas):
    elementos: int = len(paginas)
    algarismos: int = contar_algarismos(elementos)

    try:
        imagens = pagina.images

        if len(imagens) > 0:
            numeroS: str = criar_zeros_na_frente(c)

            PASTA_IMAGENS = (
                PASTA_NOVA / f"{NOME_ARQUIVO_PDF.replace(".pdf", "")} - "
                f"página {numeroS} - imagens"
            )
            PASTA_IMAGENS.mkdir(exist_ok=True)

            for imagem in imagens:
                with open(PASTA_IMAGENS / imagem.name, "wb") as fp:
                    fp.write(imagem.data)
    except ValueError:
        pass
    except:
        raise Exception("Houve um erro grave no programa! ")

arquivos: list[Path] = []

for c, pg in enumerate(paginas):
    elementos: int = len(paginas)
    algarismos: int = contar_algarismos(elementos)
    numeroS: str = criar_zeros_na_frente(c)
    escritor: PdfWriter = PdfWriter()

    with open(
        PASTA_NOVA / f"{NOME_ARQUIVO_PDF.replace(".pdf", "")} - página {numeroS}.pdf", "wb"
    ) as fp:
        escritor.add_page(pg)
        escritor.write(fp)
        arquivos.append(Path(fp.name))

fusao = PdfMerger()
arquivos: list[Path] = inverter_lista(arquivos)

for arq in arquivos:
    fusao.append(arq)

with open(PASTA_NOVA / f"{NOME_ARQUIVO_PDF.replace(".pdf", "")} - reverso.pdf", "wb") as fp:
    fusao.write(fp)
