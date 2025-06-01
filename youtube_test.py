import requests
from urllib.parse import quote_plus

def test_youtube_connection():
    API_KEY = "AIzaSyCKwX1omTDnCSdRmxVwzowxEZGJLVqi37U"
    search_query = quote_plus("test")  # Codifica o termo de busca
    
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id=dQw4w9WgXcQ&key={API_KEY}"

    response = requests.get(url)
    print(response.json())  # Deve retornar dados do vídeo "Never Gonna Give You Up"
    
    print("Testando URL:", url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Resposta da API:", data)
        
        if 'error' in data:
            print(f"Erro {data['error']['code']}: {data['error']['message']}")
            if 'errors' in data['error']:
                for error in data['error']['errors']:
                    print(f"Detalhes: {error['reason']} - {error['message']}")
        else:
            print("Conexão bem-sucedida!")
            print("Primeiro resultado:", data['items'][0]['snippet']['title'])
            
    except Exception as e:
        print("Falha completa:", str(e))

test_youtube_connection()