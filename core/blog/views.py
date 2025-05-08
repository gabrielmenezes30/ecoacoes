from django.shortcuts import render
import feedparser

def index(request):
    return render(request, 'index.html')

def noticias_sustentabilidade(request):
    url = "https://g1.globo.com/rss/g1/meio-ambiente/"
    feed = feedparser.parse(url)
    noticias = feed.entries[:5]
    
    print(f"Nº de notícias encontradas: {len(noticias)}")  # debug
    return render(request, 'noticias_externas.html', {'noticias': noticias})