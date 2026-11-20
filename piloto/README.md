# Piloto: Probabilidade — Joca Estuda

**Status:** prova de conceito, não integrada ao site público.

Este protótipo mantém a branch `desenvolvimento/piloto-probabilidade` separada da branch pública `main`. Nenhum arquivo principal do site foi alterado.

## O que já funciona
- Cinco etapas: experimento aleatório, espaço amostral, evento, fórmula, baralho e revisão;
- Diálogos de Joruto e Sensei Capivara, usando o roteiro fornecido;
- Narração sob demanda por `SpeechSynthesis` (voz de pt-BR do navegador, quando disponível);
- Dado virtual, visualização de eventos equiprováveis e quatro questões com feedback;
- Layout responsivo, fontes grandes e opção de seguir sem áudio;
- Um único arquivo `probabilidade.html`, sem conta, API, envio de dados ou custos.

## Como testar
Baixe `piloto/probabilidade.html` e abra o arquivo no navegador (pode ser sem internet).
Clique em **Ouvir explicação**, **Lançar o dado** e **Praticar**.
A voz depende do suporte do navegador/dispositivo; não é um vídeo MP4.

## Próximas etapas propostas
1. Validar com Joaquim a clareza, o ritmo da narração e o esforço visual.
2. Comparar com o vídeo do NotebookLM usando os mesmos conceitos.
3. Criar um arquivo de conteúdo estruturado único (JSON) do qual sairão cartões, quizzes e roteiros.
4. Adicionar renderizador MP4, caso a experiência interativa não seja suficiente; voz sintética natural requer um provedor ou modelo local compatível.
5. Criar automação de teste e publicação com aprovação antes da mudança na branch `main`.

## Referência pedagógica
Roteiro fornecido: **Vídeo 2: Missão 2, A Chance Ninja (Probabilidade)**. 
Não foram usadas fotografias do livro no repositório público.
