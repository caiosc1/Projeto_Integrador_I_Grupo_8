import oracledb
import getpass
senha = getpass.getpass("DIGITE A SENHA DO ADMIN DO BANCO DE DADOS: ")
connection = oracledb.connect(
    user = "BD15022426",
    password = senha,
    dsn = "172.16.12.14/xe"
)
cursor = connection.cursor()
print("\nC o n e c t a d o   a o   B a n c o    c o m    S u c e s s o\n")
print(f"==========================================================================")
print(f"||                                                                      ||")
print(f"||      S I S T E M A   D E   C O N T R O L E   D E   E S T O Q U E     ||")
print(f"||                                                                      ||")
print(f"==========================================================================")
print(f"||                                                                      ||")
print(f"||                                  M E N U                             ||")
print(f"||                                                                      ||")
print(f"==========================================================================")
print(f"|| 1. Inserir  |  2. Alterar  |  3. Excluir  |  4. Listar  |  5. Sair   ||")
print(f"==========================================================================")
escolaMenu = int(input("\n\nD I G I T E   A   O P Ç Ã O   D E S E J A D A(N Ú M E R O): "))
while escolaMenu != 5:
    if escolaMenu == 1:
        print(f"\n==========================================================================")
        print(f"||                   I N S E R Ç Ã O   D E   D A D O S                  ||")
        print(f"==========================================================================")
        codigoProduto = int(input("Digite o código do produto: "))
        nomeProduto = str(input("Digite o nome do produto: "))
        descricaoProduto = str(input("Digite a descrição do produto: "))
        custoProduto = int(input("Digite o custo do produto(R$): "))
        impostos = int(input("Digite os impostos do produto(%): "))
        custoFixo = int(input("Digite o custo fixo do produto(%): "))
        comissaoVenda = int(input("Digite a comissão de venda do produto(%): "))
        rentabilidade = int(input("Digite a rentabilidade do produto(%): "))
        while (impostos+custoFixo+comissaoVenda+rentabilidade)>=100:
            print("\nVALORES DO PRODUTO ULTRAPASSAM O LIMITE, POR FAVOR REINSIRA OS CAMPOS: ")
            impostos = int(input("Digite os impostos do produto(%): "))
            custoFixo = int(input("Digite o custo fixo do produto(%): "))
            comissaoVenda = int(input("Digite a comissão de venda do produto(%): "))
            rentabilidade = int(input("Digite a rentabilidade do produto(%): "))
        cursor.execute(f"INSERT INTO produtos_pi VALUES({codigoProduto}, '{nomeProduto}', '{descricaoProduto}', {custoProduto}, {impostos}, {custoFixo}, {comissaoVenda}, {rentabilidade})")
        connection.commit()
        input("DADOS DO PRODUTO INSERIDOS COM SUCESSO, APERTE ENTER PARA VOLTAR AO MENU...")
    elif escolaMenu == 2:
        print(f"\n==========================================================================")
        print(f"||                A L T E R A Ç Ã O   D E   D A D O S                   ||")
        print(f"==========================================================================")
        codigoProduto = int(input("\nDIGITE O CÓDIGO DO PRODUTO QUE DESEJA ALTERAR: "))
        print("\nDIGITE AS NOVAS INFORMAÇÕES DO PRODUTO:")
        nomeProduto = str(input("Digite o nome do produto: "))
        descricaoProduto = str(input("Digite a descrição do produto: "))
        custoProduto = int(input("Digite o custo do produto(R$): "))
        impostos = int(input("Digite os impostos do produto(%): "))
        custoFixo = int(input("Digite o custo fixo do produto(%): "))
        comissaoVenda = int(input("Digite a comissão de venda do produto(%): "))
        rentabilidade = int(input("Digite a rentabilidade do produto(%): "))
        while (impostos+custoFixo+comissaoVenda+rentabilidade)>=100:
            print("\nVALORES DO PRODUTO ULTRAPASSAM O LIMITE, POR FAVOR REINSIRA OS CAMPOS: ")
            impostos = int(input("Digite os impostos do produto(%): "))
            custoFixo = int(input("Digite o custo fixo do produto(%): "))
            comissaoVenda = int(input("Digite a comissão de venda do produto(%): "))
            rentabilidade = int(input("Digite a rentabilidade do produto(%): "))
        cursor.execute(f"UPDATE produtos_pi SET nome = '{nomeProduto}', descriçao = '{descricaoProduto}', custo_produto = {custoProduto}, impostos = {impostos}, custo_fixo = {custoFixo}, comissao_vendas = {comissaoVenda}, rentabilidade = {rentabilidade} WHERE codigo_produto = {codigoProduto}")
        connection.commit()
        input("\nDADOS ALTERADOS COM SUCESSO, APERTE ENTER PARA CONTINUAR...")
    elif escolaMenu == 3:
        print(f"\n==========================================================================")
        print(f"||                   E X C L U S Ã O   D E   D A D O S                  ||")
        print(f"==========================================================================")
        codigoProduto = int(input("\nDIGITE O CÓDIGO DO PRODUTO QUE DESEJA EXCLUIR: "))
        cursor.execute(f"DELETE produtos_pi WHERE codigo_produto = {codigoProduto}")
        connection.commit()
        input("PRODUTO EXCLUIDO COM SUCESSO, APERTE ENTER PARA CONTINUAR...")
    elif escolaMenu == 4:
        print(f"\n==========================================================================")
        print(f"||                 L I S T A G E M   D E  P R O D U T O S               ||")
        print(f"==========================================================================")
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
        input("APERTE ENTER PARA CONTINUAR...")
    else:
        input("ESCOLHA INVALIDA, APERTE ENTER PARA CONTINUAR...")
    print(f"==========================================================================")
    print(f"||                                                                      ||")
    print(f"||      S I S T E M A   D E   C O N T R O L E   D E   E S T O Q U E     ||")
    print(f"||                                                                      ||")
    print(f"==========================================================================")
    print(f"||                                                                      ||")
    print(f"||                                  M E N U                             ||")
    print(f"||                                                                      ||")
    print(f"==========================================================================")
    print(f"|| 1. Inserir  |  2. Alterar  |  3. Excluir  |  4. Listar  |  5. Sair   ||")
    print(f"==========================================================================")
    escolaMenu = int(input("\n\nD I G I T E   A   O P Ç Ã O   D E S E J A D A(N Ú M E R O): "))

cursor.close()
connection.close()