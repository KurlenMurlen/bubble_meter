# bubble_meter
Programa feito para medir o espectro de aproximação de algoritmo de recomendação das plataformas de mídia social.


Como o Programa Funciona:
'''
Coleta de Dados:

Utiliza APIs oficiais do YouTube e Twitter (TikTok requer implementação adicional)

Coleta recomendações com base em termos de busca padrão ou vídeos/usuários específicos

Análise de Conteúdo:

Usa processamento de linguagem natural (TF-IDF) para vetorizar o texto

Calcula similaridade de cosseno entre as recomendações

Gera métricas de diversidade (0 = totalmente personalizado, 1 = totalmente diverso)

Simulação e Comparação:

Executa múltiplas coletas para criar série temporal

Compara plataformas em um espectro de diversidade

Gera visualização gráfica automática

Saída de Dados:

Salva resultados em JSON para análise posterior

Gera gráfico comparativo entre plataformas
'''
