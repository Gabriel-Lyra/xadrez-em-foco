# Modelos

Arquivos do modelo usado em produção, gerados pelo pipeline de [treinamento](../treinamento/README.md):

- `modelo_pecas.onnx`: CNN de 13 classes. Entrada `casas` (`uint8`, N×64×64×3, BGR, a saída do `SegmentadorCasas`); saída `probabilidades` (N×13).
- `classes.json`: ordem das classes (`K Q R B N P k q r b n p vazio`).
- `treino.json`: parâmetros e métricas do treino que gerou o modelo.

## Modelo atual (16/11/2026)

Treinado com 132.561 casas sintéticas de 30 conjuntos de peças, 12 épocas, 286.597 parâmetros, 1,1 MB.

| Conjunto | Acerto por casa | Acerto nas casas ocupadas | Tabuleiros com as 64 casas corretas |
| --- | --- | --- | --- |
| Validação interna (peças do treino) | 100% | 100% | não se aplica |
| Peças reservadas (`fresca`, `leipzig`, `staunty`), 400 tabuleiros | 99,46% | 98,43% | 79,5% |

Os erros nas peças reservadas se concentram no conjunto `leipzig`: a torre e o rei pretos são lidos como brancos. Nos outros dois conjuntos, mais de 97% dos tabuleiros saem sem erro.

Estes números são de imagens sintéticas, desenhadas pelo mesmo gerador do treino. A medição com as 200 posições do conjunto de teste, pelo caminho completo da aplicação, está em [`conjunto-teste/README.md`](../conjunto-teste/README.md): 99,0% das peças e 81,5% de FEN exato.
