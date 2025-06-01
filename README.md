# Bubble Meter

O **Bubble Meter** é uma ferramenta profissional para análise do efeito bolha em plataformas de recomendação de conteúdo, como YouTube e Twitch. O sistema coleta recomendações via APIs públicas, calcula métricas de diversidade e personalização, e apresenta resultados em um espectro visual, facilitando a compreensão do potencial de formação de bolhas de cada plataforma.

## Funcionalidades

- Coleta automática de recomendações das plataformas suportadas (YouTube e Twitch)
- Análise quantitativa de similaridade e diversidade do conteúdo sugerido
- Visualização gráfica dos resultados comparativos ao longo do tempo
- Exportação dos resultados em formato JSON para análise posterior

## Configuração

1. **Clone o repositório e instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

2. **Crie um arquivo `.env` na raiz do projeto com suas chaves de API:**
   ```
   YOUTUBE_API_KEY=sua_chave_youtube
   TWITCH_API_KEY=sua_chave_twitch
   ```

3. **Execute o programa:**
   ```
   python bubble_meter.py
   ```

## Observações

- As chaves de API são obrigatórias para funcionamento. Consulte a documentação de cada plataforma para obter suas credenciais.
- Os resultados são salvos em `results.json` e a visualização é exportada como `diversity_comparison.png`.

## Licença

MIT License.