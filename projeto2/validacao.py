import json

CATEGORIAS = ["Suporte", "Vendas", "Financeiro", "Geral"]


def validar_resposta(resposta):

    try:
        # converter JSON
        dados = json.loads(resposta)

        categoria = dados["categoria"]

        # validar categoria
        if categoria in CATEGORIAS:
            return categoria
        else:
            return "Geral"

    except json.JSONDecodeError:
        print("Erro: JSON inválido")
        return "Geral"

    except KeyError:
        print("Erro: chave 'categoria' não encontrada")
        return "Geral"