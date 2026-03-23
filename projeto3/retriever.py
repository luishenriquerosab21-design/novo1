
import os
import numpy as np
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer

# Carrega o modelo local
model = SentenceTransformer('all-MiniLM-L6-v2')
vector_db = []


def ler_txt(caminho):
    """Lê ficheiros de texto padrão."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler TXT {caminho}: {e}")
        return ""

def ler_pdf(caminho):
    """Extrai texto de ficheiros PDF."""
    texto = ""
    try:
        with open(caminho, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            for pagina in leitor.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"
    except Exception as e:
        print(f"Erro ao ler PDF {caminho}: {e}")
    return texto

def ler_docx(caminho):
    """Extrai texto de documentos do Word."""
    texto = ""
    try:
        doc = docx.Document(caminho)
        for paragrafo in doc.paragraphs:
            if paragrafo.text:
                texto += paragrafo.text + "\n"
    except Exception as e:
        print(f"Erro ao ler DOCX {caminho}: {e}")
    return texto

def load_conhecimento():
    """Percorre a pasta de conhecimento e vetoriza todos os ficheiros."""
    global vector_db
    vector_db = [] 
    pasta_conhecimento = "conhecimento"
    
    
    print("\nA processar ficheiros e a gerar embeddings locais...")
    
    if not os.path.exists(pasta_conhecimento):
        print(f"Pasta '{pasta_conhecimento}' não encontrada!")
        return vector_db

    texto_total = ""
    
    # Inspeciona todos os ficheiros dentro da pasta
    for nome_ficheiro in os.listdir(pasta_conhecimento):
        caminho_ficheiro = os.path.join(pasta_conhecimento, nome_ficheiro)
        
        if nome_ficheiro.endswith(".txt"):
            texto_total += ler_txt(caminho_ficheiro) + "\n\n"
        elif nome_ficheiro.endswith(".pdf"):
            texto_total += ler_pdf(caminho_ficheiro) + "\n\n"
        elif nome_ficheiro.endswith(".docx"):
            texto_total += ler_docx(caminho_ficheiro) + "\n\n"

    # Uniformiza as separações para criar os blocos (chunks)
    texto_total = texto_total.replace("--------------------------------------------------", "\n\n")
    chunks = [chunk.strip() for chunk in texto_total.split("\n\n") if len(chunk.strip()) > 15]
    
    for chunk in chunks:
        emb = model.encode(chunk)
        vector_db.append({"texto": chunk, "embedding": emb})
    
    print(f"Conhecimento carregado! {len(vector_db)} blocos vetorizados a partir dos ficheiros.")
    return vector_db

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def simple_retriever(query):
    if not vector_db:
        return "Base de conhecimento vazia."
    
    query_emb = model.encode(query)
    
    resultados = []
    for item in vector_db:
        sim = cosine_similarity(query_emb, item["embedding"])
        resultados.append((sim, item["texto"]))
    
    resultados.sort(key=lambda x: x[0], reverse=True)
    melhor_contexto = resultados[0][1]
    
    return melhor_contexto
