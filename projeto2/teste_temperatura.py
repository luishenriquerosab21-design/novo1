from classificador import classificar_mensagem

cliente = [
    "Quero contratar o plano premium,",
    "O sistema esta com erro",
    "Quero cancelar minha assinatura",
    "Quero falar com um atendente",
    "Preciso de ajuda com meu pagamento",
    "Gostaria de atualizar minhas informações de conta",
    "voces trabalham com sabado"
]

temperaturas = [0.0, 0.5, 1.0]

repeticoes = 10


for temp in temperaturas:

    print(f"\n=== Temperatura: {temp} ===")

    resultados = {}

    for i in range(repeticoes):

        categoria = classificar_mensagem(cliente, temperature=temp)

        print(f"Teste {i+1}: {categoria}")

        if categoria in resultados:
            resultados[categoria] += 1
        else:
            resultados[categoria] = 1

    print("\nResumo:")
    print(resultados)