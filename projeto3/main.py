from llm_client import LLMClient
from retriever import load_conhecimento, simple_retriever
from validator import validate_json
from prompt import build_system_prompt

def main():
    provider = input("Escolha o provedor (openai/groq): ").strip().lower()
    client = LLMClient(provider=provider)
    
    load_conhecimento()

    while True:
        query = input("\nPergunta (ou 'sair'): ").strip()

        if query.lower() == "sair":
            break
        
        contexto = simple_retriever(query)
        system_prompt = build_system_prompt()

        user_prompt = f"""
Contexto:
{contexto}

Pergunta:
{query}
"""

        response_text = client.generate_text(system_prompt, user_prompt)

        try:
            is_valid, data = validate_json(response_text)
            if is_valid:
                print(f"[{data['status'].upper()}] {data['resposta']}")
        except Exception:
            print("⚠️ Resposta inválida:")
            print(response_text)

if __name__ == "__main__":
    main()