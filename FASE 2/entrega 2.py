import oracledb
import getpass
senha = getpass.getpass("DIGITE A SENHA DO ADMIN DO BANCO DE DADOS: ")
connection = oracledb.connect(
    user = "BD15022426",
    password = senha,
    dsn = "172.16.12.14/xe"
)
print("\nC o n e c t a d o   a o   B a n c o    c o m    S u c e s s o\n")
print("I m p o r t a n d o   D a d o s   d o s   P r o d u t o s . . .\n\n")
cursor = connection.cursor()
cursor.execute("SELECT * FROM produtos_pi")
#produtos = cursor.fetchall()
listaProdutos = cursor
for produto in listaProdutos:
    codigoProduto = produto[0]
    nomeProduto = produto[1]
    descricaoProduto = produto[2]
    custoProduto = produto[3]
    impostos = produto[4]
    custoFixo = produto[5]
    comissaoVenda = produto[6]
    rentabilidade = produto[7]
    #Cálculo do Preço de Venda
    precoVenda = custoProduto/(1-(custoFixo+comissaoVenda+impostos+rentabilidade)/100)
    #Tela de apresentação dos resultados
    print("--------------------------------------------------------")
    print(f"Código: {codigoProduto:<10}{"Nome: "+nomeProduto:>37} \n\nDescrição: {descricaoProduto}")
    print("--------------------------------------------------------")
    print("{:35} Valor \t %".format("Descrição"))
    print("--------------------------------------------------------")
    print("{:35} {:.2f} \t 100%".format("A. Preço de Venda", precoVenda))
    print("{:35} {:.2f} \t {:.2f}%".format("B. Custo de Aquisição(Fornecedor)", custoProduto, custoProduto*100/precoVenda))
    print("{:35} {:.2f} \t {:.2f}%".format("C. Receita Bruta (A-B)", (precoVenda-custoProduto), (precoVenda-custoProduto)*100/precoVenda))
    print("{:35} {:.2f} \t {:.2f}%".format("D. Custo Fixo/Administrativo", custoFixo/100 * precoVenda, custoFixo))
    print("{:35} {:.2f} \t {:.2f}%".format("E. Comissão de Vendas", comissaoVenda/100 * precoVenda, comissaoVenda))
    print("{:35} {:.2f} \t {:.2f}%".format("F. Impostos", impostos/100 * precoVenda, impostos))
    print("{:35} {:.2f} \t {:.2f}%".format("G. Outros custos(D+E+F)", custoFixo/100 * precoVenda + comissaoVenda/100 * precoVenda + impostos/100 * precoVenda, custoFixo+comissaoVenda+impostos))
    print("{:35} {:.2f} \t {:.2f}%".format("H. Rentabilidade",  rentabilidade/100 * precoVenda, rentabilidade))
    print("--------------------------------------------------------")
    if  rentabilidade > 20:
        print("Lucro: Alto")
    elif    rentabilidade > 10:
        print("Lucro: Médio")
    elif    rentabilidade > 0:
        print("Lucro: Baixo")
    elif    rentabilidade == 0:
        print("Equilíbrio")
    elif    rentabilidade < 0:
        print("Prejuízo")
    print("--------------------------------------------------------\n\n\n")

cursor.close()
connection.close()
