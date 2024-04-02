#Coleta de Informações do produto
codigoProduto = str(input("Digite o código do produto:"))
nomeProduto = str(input("Digite o nome do produto:"))
descricaoProduto = str(input("Digite a descrição do produto: "))
precoVenda = 0
custoProduto = float(input("Digite o custo do produto: "))
custoFixo = float(input("Digite o custo fixo (%): "))
impostos = float(input("Digite o valor dos impostos (%): "))
comissaoVenda = float(input("Digite a comissão de venda (%): "))
margemLucro = float(input("Digite a margem de lucro (%): "))
#Cálculo do Preço de Venda
precoVenda = custoProduto/(1-(custoFixo+comissaoVenda+impostos+margemLucro)/100)
#Tela de apresentação dos resultados
print("-----------------------------------------------------")
print("{:35} Valor \t %".format("Descrição"))
print("-----------------------------------------------------")
print("{:35} {:.2f} \t 100%".format("A. Preço de Venda", precoVenda))
print("{:35} {:.2f} \t {:.0f}%".format("B. Custo de Aquisição(Fornecedor)", custoProduto, custoProduto*100/precoVenda))
print("{:35} {:.2f} \t {:.0f}%".format("C. Receita Bruta (A-B)", (precoVenda-custoProduto), (precoVenda-custoProduto)*100/precoVenda))
print("{:35} {:.2f} \t {:.0f}%".format("D. Custo Fixo/Administrativo", custoFixo/100 * precoVenda, custoFixo))
print("{:35} {:.2f} \t {:.0f}%".format("E. Comissão de Vendas", comissaoVenda/100 * precoVenda, comissaoVenda))
print("{:35} {:.2f} \t {:.0f}%".format("F. Impostos", impostos/100 * precoVenda, impostos))
print("{:35} {:.2f} \t {:.0f}%".format("G. Outros custos(D+E+F)", custoFixo/100 * precoVenda + comissaoVenda/100 * precoVenda + impostos/100 * precoVenda, custoFixo+comissaoVenda+impostos))
print("{:35} {:.2f} \t {:.0f}%".format("H. Rentabilidade", margemLucro/100 * precoVenda, margemLucro))
print("-----------------------------------------------------")
if  margemLucro > 20:
    print("Lucro: Alto")
elif margemLucro > 10:
    print("Lucro: Médio")
elif margemLucro > 0:
    print("Lucro: Baixo")
elif margemLucro == 0:
    print("Equilíbrio")
elif margemLucro < 0:
    print("Prejuízo")
print("-----------------------------------------------------")
