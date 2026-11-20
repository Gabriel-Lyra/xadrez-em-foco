// Lógica da página: envio do print (PB07), processamento, resultado (PB19, PB20, PB17)
// e mensagens de erro (PB21).
"use strict";

(function () {
  const TAMANHO_MAX_BYTES = 10 * 1024 * 1024;
  const TIPOS_ACEITOS = ["image/png", "image/jpeg", "image/webp"];
  const URL_API = "/api/reconhecer";

  const MENSAGEM_SEM_IMAGEM = "A área de transferência não contém uma imagem. Copie o print e tente de novo.";
  const SEM_CONEXAO = 0;

  // Mensagens da Tabela 4 do Documento de Arquitetura, com título e dicas para cada caso.
  // Para códigos fora desta lista, vale a mensagem enviada pela API, com as dicas do 500.
  const ERROS = {
    400: {
      titulo: "Esse arquivo não é uma imagem aceita.",
      mensagem: "Envie uma imagem PNG, JPG ou WEBP.",
      dicas: [
        "Use a captura de tela original, em PNG ou JPG.",
        "Se a imagem veio de um aplicativo de mensagens, salve-a de novo antes de enviar.",
        "GIF, HEIC, PDF e outros formatos não são aceitos.",
      ],
    },
    413: {
      titulo: "A imagem é grande demais.",
      mensagem: "A imagem excede o limite de 10 MB ou de 25 megapixels.",
      dicas: [
        "Recorte o print deixando só o tabuleiro.",
        "Salve em JPG ou WEBP, que costumam ocupar menos espaço que PNG.",
        "Capturas de tela comuns têm bem menos de 10 MB e de 25 megapixels; confira se não é uma foto em alta resolução.",
      ],
    },
    422: {
      titulo: "Não encontramos um tabuleiro nessa imagem.",
      mensagem: "O arquivo foi recebido, mas nenhuma grade 8×8 foi localizada com segurança.",
      dicas: [
        "Recorte o print deixando o tabuleiro inteiro visível.",
        "Evite setas, destaques de lance ou menus abertos sobre as casas.",
        "Prefira temas de tabuleiro padrão (marrom, verde ou azul).",
        "Use a resolução original; evite fotos da tela ou imagens reduzidas.",
      ],
    },
    500: {
      titulo: "Não foi possível processar agora.",
      mensagem: "Não foi possível processar agora; tente novamente.",
      dicas: [
        "Tente de novo em alguns segundos.",
        "Se o erro continuar com o mesmo print, tente outro.",
      ],
    },
    [SEM_CONEXAO]: {
      titulo: "Sem conexão com o servidor.",
      mensagem: "Não foi possível falar com o servidor. Verifique a conexão e tente de novo.",
      dicas: [
        "Confira se o computador ou o celular está conectado à internet.",
        "Depois de um tempo sem uso, o servidor pode levar cerca de 1 minuto para voltar; tente de novo em seguida.",
      ],
    },
  };

  const telas = {
    inicial: document.getElementById("tela-inicial"),
    processando: document.getElementById("tela-processando"),
    resultado: document.getElementById("tela-resultado"),
    erro: document.getElementById("tela-erro"),
  };
  const areaEnvio = document.getElementById("area-envio");
  const campoArquivo = document.getElementById("campo-arquivo");
  const mensagemEnvio = document.getElementById("mensagem-envio");
  const previaImagem = document.getElementById("previa-imagem");
  const previaLegenda = document.getElementById("previa-legenda");

  let enviando = false;
  let urlPrevia = null;

  // ---------- Telas ----------

  function mostrarTela(nome) {
    Object.entries(telas).forEach(([chave, tela]) => {
      tela.hidden = chave !== nome;
    });
    window.scrollTo(0, 0);
  }

  function recomecar() {
    esconderMensagemEnvio();
    campoArquivo.value = "";
    mostrarTela("inicial");
    areaEnvio.focus();
  }

  // ---------- Validação no navegador ----------
  // O servidor valida de novo pelos primeiros bytes; aqui a ideia é recusar na hora.

  // Devolve o código HTTP que o servidor daria (400 ou 413), ou null se o arquivo serve.
  function validarArquivo(arquivo) {
    if (!TIPOS_ACEITOS.includes(arquivo.type)) {
      return 400;
    }
    if (arquivo.size > TAMANHO_MAX_BYTES) {
      return 413;
    }
    return null;
  }

  function mostrarMensagemEnvio(texto) {
    mensagemEnvio.textContent = texto;
    mensagemEnvio.hidden = false;
  }

  function esconderMensagemEnvio() {
    mensagemEnvio.hidden = true;
    mensagemEnvio.textContent = "";
  }

  function formatarTamanho(bytes) {
    if (bytes < 1024 * 1024) {
      return Math.max(1, Math.round(bytes / 1024)) + " KB";
    }
    return (bytes / (1024 * 1024)).toFixed(1).replace(".", ",") + " MB";
  }

  // ---------- Envio ----------

  async function enviar(arquivo) {
    if (enviando) {
      return;
    }
    const problema = validarArquivo(arquivo);
    if (problema) {
      campoArquivo.value = "";
      mostrarErro(problema);
      return;
    }

    enviando = true;
    esconderMensagemEnvio();
    mostrarPrevia(arquivo);
    mostrarTela("processando");

    const formulario = new FormData();
    formulario.append("imagem", arquivo, arquivo.name || "print.png");

    try {
      const resposta = await fetch(URL_API, { method: "POST", body: formulario });
      const corpo = await lerJson(resposta);
      if (resposta.ok && corpo) {
        mostrarResultado(corpo);
      } else {
        mostrarErro(resposta.status, corpo && corpo.mensagem);
      }
    } catch (erro) {
      mostrarErro(SEM_CONEXAO);
    } finally {
      enviando = false;
      campoArquivo.value = "";
    }
  }

  async function lerJson(resposta) {
    try {
      return await resposta.json();
    } catch (erro) {
      return null;
    }
  }

  function mostrarPrevia(arquivo) {
    if (urlPrevia) {
      URL.revokeObjectURL(urlPrevia);
    }
    urlPrevia = URL.createObjectURL(arquivo);
    previaImagem.src = urlPrevia;
    previaLegenda.textContent = (arquivo.name || "Imagem colada") + " · " + formatarTamanho(arquivo.size);
  }

  // ---------- Resultado (PB19, PB20 e troca manual do lado de baixo do PB17) ----------

  const GLIFOS = { k: "\u265A", q: "\u265B", r: "\u265C", b: "\u265D", n: "\u265E", p: "\u265F" };
  // Força a versão em texto do símbolo; sem isso, o Windows pode desenhar o peão como emoji.
  const VARIACAO_TEXTO = "\uFE0E";
  const COLUNAS = "abcdefgh";

  const campoFen = document.getElementById("campo-fen");
  const botaoCopiar = document.getElementById("botao-copiar");
  const avisoCopia = document.getElementById("aviso-copia");
  const linkLichess = document.getElementById("link-lichess");
  const botoesOrientacao = document.querySelectorAll("[data-orientacao]");
  let resultado = null;
  let temporizadorCopia = null;

  function mostrarResultado(dados) {
    resultado = dados;
    mostrarDemonstracao(dados);
    mostrarConfianca(dados.confianca_media);
    mostrarAvisos(dados);
    aplicarOrientacao(dados.orientacao === "pretas" ? "pretas" : "brancas");
    avisoCopia.textContent = "";
    mostrarTela("resultado");
  }

  function mostrarDemonstracao(dados) {
    const faixa = document.getElementById("faixa-demonstracao");
    const emDemonstracao = dados.modo === "demonstracao";
    faixa.hidden = !emDemonstracao;
    // No modo demonstração, a API garante que o primeiro aviso é o que explica o modo.
    document.getElementById("texto-demonstracao").textContent = emDemonstracao ? dados.avisos[0] : "";
  }

  function mostrarConfianca(confianca) {
    const selo = document.getElementById("selo-confianca");
    if (confianca === null || confianca === undefined) {
      selo.textContent = "Demonstração";
      selo.classList.add("demonstracao");
      return;
    }
    const percentual = (confianca * 100).toFixed(1).replace(".", ",");
    selo.textContent = "\u25CF Confiança " + percentual + "%";
    selo.classList.remove("demonstracao");
  }

  function mostrarAvisos(dados) {
    const avisos = dados.modo === "demonstracao" ? dados.avisos.slice(1) : dados.avisos;
    const bloco = document.getElementById("avisos-posicao");
    const lista = document.getElementById("lista-avisos");
    lista.replaceChildren(
      ...avisos.map((texto) => {
        const item = document.createElement("li");
        item.textContent = texto;
        return item;
      })
    );
    bloco.hidden = avisos.length === 0;
  }

  // "pretas" significa que o print mostra as pretas embaixo: vale o FEN invertido,
  // e o tabuleiro é desenhado do ponto de vista das pretas, como no print.
  function aplicarOrientacao(orientacao) {
    const pretasEmbaixo = orientacao === "pretas";
    const fen = pretasEmbaixo ? resultado.fen_invertido : resultado.fen;
    campoFen.value = fen;
    linkLichess.href = pretasEmbaixo ? resultado.link_lichess_invertido : resultado.link_lichess;
    desenharTabuleiro(fen, pretasEmbaixo);
    botoesOrientacao.forEach((botao) => {
      botao.setAttribute("aria-pressed", String(botao.dataset.orientacao === orientacao));
    });
    const detectada = resultado.orientacao === orientacao;
    document.getElementById("explicacao-orientacao").textContent = detectada
      ? "Lado detectado pelo sistema. Troque se o print estiver com as " + (pretasEmbaixo ? "brancas" : "pretas") + " embaixo."
      : "Alterado por você. O FEN e o link do Lichess já correspondem a este lado.";
  }

  function lerFen(fen) {
    return fen.split("/").map((fileira) => {
      const casas = [];
      for (const caractere of fileira) {
        if (/[1-8]/.test(caractere)) {
          for (let i = 0; i < Number(caractere); i++) {
            casas.push(null);
          }
        } else {
          casas.push(caractere);
        }
      }
      return casas;
    });
  }

  function desenharTabuleiro(fen, pretasEmbaixo) {
    const grade = lerFen(fen); // grade[0] é a fileira 8; grade[i][0] é a coluna a.
    const tabuleiro = document.getElementById("tabuleiro");
    const casas = [];
    for (let linha = 0; linha < 8; linha++) {
      for (let coluna = 0; coluna < 8; coluna++) {
        const indiceFileira = pretasEmbaixo ? 7 - linha : linha;
        const indiceColuna = pretasEmbaixo ? 7 - coluna : coluna;
        const fileira = 8 - indiceFileira;
        const peca = grade[indiceFileira][indiceColuna];

        const casa = document.createElement("div");
        // a1 é escura: (coluna + fileira - 1) par.
        casa.className = "casa " + ((indiceColuna + fileira - 1) % 2 === 0 ? "escura" : "clara");
        if (peca) {
          const simbolo = document.createElement("span");
          simbolo.textContent = GLIFOS[peca.toLowerCase()] + VARIACAO_TEXTO;
          simbolo.className = peca === peca.toUpperCase() ? "peca-branca" : "peca-preta";
          casa.appendChild(simbolo);
        }
        if (linha === 7) {
          casa.appendChild(coordenada("coluna", COLUNAS[indiceColuna]));
        }
        if (coluna === 0) {
          casa.appendChild(coordenada("fileira", String(fileira)));
        }
        casas.push(casa);
      }
    }
    tabuleiro.replaceChildren(...casas);
    tabuleiro.setAttribute("aria-label", "Tabuleiro reconhecido, " + (pretasEmbaixo ? "pretas" : "brancas") + " embaixo: " + fen);
  }

  function coordenada(tipo, texto) {
    const elemento = document.createElement("span");
    elemento.className = "coordenada " + tipo;
    elemento.textContent = texto;
    elemento.setAttribute("aria-hidden", "true");
    return elemento;
  }

  async function copiarFen() {
    const fen = campoFen.value;
    let copiou = false;
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(fen);
        copiou = true;
      } catch (erro) {
        copiou = false;
      }
    }
    if (!copiou) {
      // Plano B para navegadores sem a API da área de transferência ou fora de HTTPS.
      campoFen.focus();
      campoFen.select();
      try {
        copiou = document.execCommand("copy");
      } catch (erro) {
        copiou = false;
      }
    }
    avisoCopia.textContent = copiou ? "FEN copiado para a área de transferência." : "Não foi possível copiar; selecione o texto e use Ctrl+C.";
    botaoCopiar.textContent = copiou ? "Copiado!" : "Copiar";
    clearTimeout(temporizadorCopia);
    temporizadorCopia = setTimeout(() => {
      botaoCopiar.textContent = "Copiar";
    }, 2000);
  }

  botaoCopiar.addEventListener("click", copiarFen);
  campoFen.addEventListener("focus", () => campoFen.select());
  botoesOrientacao.forEach((botao) => {
    botao.addEventListener("click", () => aplicarOrientacao(botao.dataset.orientacao));
  });

  // ---------- Erro (PB21) ----------

  function mostrarErro(codigo, mensagemDaApi) {
    const conhecido = Object.prototype.hasOwnProperty.call(ERROS, codigo);
    const erro = conhecido ? ERROS[codigo] : ERROS[500];
    document.getElementById("titulo-erro").textContent = erro.titulo;
    document.getElementById("erro-mensagem").textContent = conhecido ? erro.mensagem : mensagemDaApi || erro.mensagem;
    document.getElementById("erro-dicas").replaceChildren(
      ...erro.dicas.map((texto) => {
        const item = document.createElement("li");
        item.textContent = texto;
        return item;
      })
    );
    mostrarTela("erro");
  }

  // ---------- Formas de envio: arquivo, arrastar e Ctrl+V ----------

  areaEnvio.addEventListener("click", () => campoArquivo.click());
  areaEnvio.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter" || evento.key === " ") {
      evento.preventDefault();
      campoArquivo.click();
    }
  });

  campoArquivo.addEventListener("change", () => {
    if (campoArquivo.files.length > 0) {
      enviar(campoArquivo.files[0]);
    }
  });

  ["dragenter", "dragover"].forEach((tipo) => {
    areaEnvio.addEventListener(tipo, (evento) => {
      evento.preventDefault();
      areaEnvio.classList.add("arrastando");
    });
  });
  ["dragleave", "dragend"].forEach((tipo) => {
    areaEnvio.addEventListener(tipo, () => areaEnvio.classList.remove("arrastando"));
  });
  areaEnvio.addEventListener("drop", (evento) => {
    evento.preventDefault();
    areaEnvio.classList.remove("arrastando");
    const arquivos = evento.dataTransfer && evento.dataTransfer.files;
    if (arquivos && arquivos.length > 0) {
      enviar(arquivos[0]);
    }
  });

  // Evita que soltar a imagem fora da área faça o navegador abrir o arquivo.
  window.addEventListener("dragover", (evento) => evento.preventDefault());
  window.addEventListener("drop", (evento) => evento.preventDefault());

  // Ctrl+V funciona em qualquer ponto da página, na tela inicial ou na de erro.
  document.addEventListener("paste", (evento) => {
    if (telas.processando.hidden === false) {
      return;
    }
    const itens = (evento.clipboardData && evento.clipboardData.items) || [];
    for (const item of itens) {
      if (item.kind === "file" && item.type.startsWith("image/")) {
        const arquivo = item.getAsFile();
        if (arquivo) {
          evento.preventDefault();
          enviar(arquivo);
          return;
        }
      }
    }
    if (telas.inicial.hidden === false || telas.erro.hidden === false) {
      mostrarTela("inicial");
      mostrarMensagemEnvio(MENSAGEM_SEM_IMAGEM);
    }
  });

  document.querySelectorAll('[data-acao="recomecar"]').forEach((botao) => {
    botao.addEventListener("click", recomecar);
  });
})();
