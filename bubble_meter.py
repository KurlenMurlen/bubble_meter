import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import praw

load_dotenv()

class BubbleMeter:
    def __init__(self):
        self.platforms = {
            'YouTube': self.analyze_youtube,
            'Reddit': self.analyze_reddit
        }
        self.results = []
        
        # Configurações de API
        self.api_keys = {
            'youtube': os.getenv('YOUTUBE_API_KEY'),
            'reddit_client_id': os.getenv('REDDIT_CLIENT_ID'),
            'reddit_client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
            'reddit_user_agent': os.getenv('REDDIT_USER_AGENT')
        }
        
        # Inicializa cliente do Reddit
        self.reddit = praw.Reddit(
            client_id=self.api_keys['reddit_client_id'],
            client_secret=self.api_keys['reddit_client_secret'],
            user_agent=self.api_keys['reddit_user_agent']
        )

    def get_youtube_recommendations(self, video_id=None, max_results=10):
        """Coleta recomendações do YouTube API"""
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'maxResults': max_results,
            'key': self.api_keys['youtube'],
            'type': 'video'
        }
        
        if video_id:
            params['relatedToVideoId'] = video_id
        else:
            params['q'] = 'news'
            
        response = requests.get(base_url, params=params)
        return response.json()

    def get_reddit_recommendations(self, subreddit="news", max_results=10):
        """Coleta posts populares do Reddit"""
        try:
            posts = []
            for post in self.reddit.subreddit(subreddit).hot(limit=max_results):
                posts.append({
                    'title': post.title,
                    'score': post.score,
                    'url': post.url,
                    'subreddit': post.subreddit.display_name
                })
            return {'data': posts}
        except Exception as e:
            print(f"Erro ao coletar dados do Reddit: {str(e)}")
            return {"data": []}

    def analyze_content(self, items, platform):
        """Analisa o conteúdo coletado e calcula métricas de personalização"""
        if not items:
            print(f"Nenhum item coletado para {platform}. Pulando análise.")
            return {
                'platform': platform,
                'avg_similarity': None,
                'diversity_score': None,
                'sample_size': 0,
                'timestamp': datetime.now().isoformat()
            }

        if platform == 'YouTube':
            texts = [item['snippet']['title'] for item in items]
        elif platform == 'Reddit':
            texts = [item['title'] for item in items]
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(similarity_matrix, 0)
        avg_similarity = np.mean(similarity_matrix)
        diversity_score = 1 - avg_similarity
        
        return {
            'platform': platform,
            'avg_similarity': avg_similarity,
            'diversity_score': diversity_score,
            'sample_size': len(items),
            'timestamp': datetime.now().isoformat()
        }

    def analyze_youtube(self):
        """Fluxo completo de análise para YouTube"""
        print("Coletando recomendações do YouTube...")
        data = self.get_youtube_recommendations()
        if 'items' in data and data['items']:
            result = self.analyze_content(data['items'], 'YouTube')
            self.results.append(result)
            print(f"Análise do YouTube concluída: {result}")
            return result
        else:
            print("Nenhum dado coletado do YouTube.")
            return None

    def analyze_reddit(self):
        """Fluxo completo de análise para Reddit"""
        print("Coletando posts do Reddit...")
        data = self.get_reddit_recommendations()
        if 'data' in data:
            result = self.analyze_content(data['data'], 'Reddit')
            self.results.append(result)
            return result
        return None

    def run_simulation(self, iterations=3):
        """Executa simulações repetidas para criar espectro comparativo"""
        for i in range(iterations):
            print(f"\nIteração {i+1}/{iterations}")
            for platform, analyzer in self.platforms.items():
                analyzer()
            time.sleep(60)  # Intervalo entre coletas

    def visualize_results(self):
        """Gera visualização dos resultados"""
        if not self.results:
            print("Nenhum resultado para visualizar")
            return
            
        df = pd.DataFrame(self.results)
        pivot = df.pivot_table(index='timestamp', columns='platform', values='diversity_score')
        
        plt.figure(figsize=(12, 8))
        for platform in pivot.columns:
            plt.plot(pivot.index, pivot[platform], marker='o', label=platform)
        
        plt.title('Comparação de Diversidade de Conteúdo entre Plataformas', fontsize=16)
        plt.ylabel('Score de Diversidade (0-1)', fontsize=14)
        plt.xlabel('Tempo', fontsize=14)
        plt.ylim(0, 1)
        plt.legend(title="Plataformas", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('diversity_comparison.png')
        plt.show()
        
        return pivot

    def save_results(self, filename='results.json'):
        """Salva resultados em arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    analyzer = BubbleMeter()
    print("Iniciando simulação de coleta de dados...")
    analyzer.run_simulation(iterations=2)
    print("\nResultados da análise:")
    results_df = analyzer.visualize_results()
    print(results_df)
    analyzer.save_results()
    print("Análise concluída. Resultados salvos em results.json")