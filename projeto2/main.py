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

for mensagem in cliente:
    resposta = classificar_mensagem(mensagem)
    print(f"Cliente: {mensagem}")
    print(f"Resposta: {resposta}\n")


