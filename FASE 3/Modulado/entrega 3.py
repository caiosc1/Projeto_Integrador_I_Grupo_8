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
def menu():
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
    escolaMenu = int(input("\n\nDIGITE A OPÇÃO DESEJADA(NÚMERO): "))
    if escolaMenu == 5:
        print("SAINDO DO PROGRAMA...")
    elif escolaMenu == 1:
        menu_insercao()
    elif escolaMenu == 2:
        menu_alteracao()
    elif escolaMenu == 3:
        menu_exclusao()
    elif escolaMenu == 4:
        listagem()
    else:
        input("ESCOLHA INVALIDA, APERTE ENTER PARA CONTINUAR...")
        return menu()

def menu_insercao():
    print(f"\n==========================================================================")
    print(f"||                   I N S E R Ç Ã O   D E   D A D O S                  ||")
    print(f"==========================================================================")
    codigoProduto = int(input("Digite o código do produto: "))
    nomeProduto = str(input("Digite o nome do produto: "))
    descricaoProduto = str(input("Digite a descrição do produto: "))
    custoProduto = float(input("Digite o custo do produto(R$): "))
    impostos = float(input("Digite os impostos do produto(%): "))
    custoFixo = float(input("Digite o custo fixo do produto(%): "))
    comissaoVenda = float(input("Digite a comissão de venda do produto(%): "))
    rentabilidade = float(input("Digite a rentabilidade do produto(%): "))
    while (impostos+custoFixo+comissaoVenda+rentabilidade)>=100:
        print("\nVALORES DO PRODUTO ULTRAPASSAM O LIMITE, POR FAVOR REINSIRA OS CAMPOS: ")
        impostos = float(input("Digite os impostos do produto(%): "))
        custoFixo = float(input("Digite o custo fixo do produto(%): "))
        comissaoVenda = float(input("Digite a comissão de venda do produto(%): "))
        rentabilidade = float(input("Digite a rentabilidade do produto(%): "))
    cursor.execute(f"INSERT INTO produtos_pi VALUES({codigoProduto}, '{nomeProduto}', '{descricaoProduto}', {custoProduto}, {impostos}, {custoFixo}, {comissaoVenda}, {rentabilidade})")
    connection.commit()
    input("DADOS DO PRODUTO INSERIDOS COM SUCESSO, APERTE ENTER PARA VOLTAR AO MENU...")
    return menu()

def menu_alteracao():
    print(f"\n==========================================================================")
    print(f"||                A L T E R A Ç Ã O   D E   D A D O S                   ||")
    print(f"==========================================================================")
    listaMudancas = {1:"nome" ,2: "descriçao",3: "custo_produto", 4: "custo_fixo",5: "comissao_vendas",6: "impostos",7: "rentabilidade"}
    valsstring = [1, 2]
    codigoProduto = int(input("\nDIGITE O CÓDIGO DO PRODUTO QUE DESEJA ALTERAR: "))
    cursor.execute(f"SELECT * FROM produtos_pi WHERE codigo_produto = {codigoProduto}")
    produto_excluido = cursor
    for produto in produto_excluido:
        #             Nome, descrição, custo,custo fixo, comissão, impostos, rentabilidade
        infProd = [produto[1],produto[2],produto[3],produto[5],produto[6],produto[4],produto[7]]
        #Tela de apresentação dos resultados
        print("--------------------------------------------------------")
        print(f"\t1. Nome: {produto[1]}")
        print(f"\t2. Descrição: {produto[2]}")
        print(f"\t3. Custo de Aquisição: {produto[3]}")
        print(f"\t4. Custo Fixo/Administrativo: {produto[5]}")
        print(f"\t5. Comissão de Vendas: {produto[6]}")
        print(f"\t6. Impostos: {produto[4]}")
        print(f"\t7. Rentabilidade: {produto[7]}")
        print("--------------------------------------------------------")
    escolhaAlteracao = int(input("DIGITE O NÚMERO DO CAMPO QUE DESEJA ALTERAR: "))
    if escolhaAlteracao in valsstring:
        alteracao = str(input("DIGITE O NOVO VALOR DO CAMPO ESCOLHIDO: "))
        cursor.execute(f"UPDATE produtos_pi set {listaMudancas[escolhaAlteracao]} = '{alteracao}' WHERE codigo_produto = {codigoProduto}")
    else:
        alteracao = float(input("DIGITE O NOVO VALOR DO CAMPO ESCOLHIDO: "))
        infProd[escolhaAlteracao-1] = alteracao
        while (infProd[3]+infProd[4]+infProd[5]+infProd[6])>=100:
            print("\nVALORES DO PRODUTO ULTRAPASSAM O LIMITE, POR FAVOR REINSIRA O CAMPO: ")
            alteracao = float(input("DIGITE O NOVO VALOR DO CAMPO ESCOLHIDO: "))
            infProd[escolhaAlteracao-1] = alteracao
        cursor.execute(f"UPDATE produtos_pi set {listaMudancas[escolhaAlteracao]} = {alteracao} WHERE codigo_produto = {codigoProduto}")
    connection.commit()
    input("PRODUTO ALTERADO COM SUCESSO, APERTE ENTER PARA CONTINUAR...")
    return menu()

def menu_exclusao():
    print(f"\n==========================================================================")
    print(f"||                   E X C L U S Ã O   D E   D A D O S                  ||")
    print(f"==========================================================================")
    codigoProduto = int(input("\nDIGITE O CÓDIGO DO PRODUTO QUE DESEJA EXCLUIR: "))
    cursor.execute(f"SELECT * FROM produtos_pi WHERE codigo_produto = {codigoProduto}")
    produto_excluido = cursor
    for produto in produto_excluido:
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
    escolha_exclusao = str(input("DESEJA REALMENTE EXCLUIR O PRODUTO(S/N): "))
    if escolha_exclusao.upper() == "S":
        cursor.execute(f"DELETE produtos_pi WHERE codigo_produto = {codigoProduto}")
        connection.commit()
        input("PRODUTO EXCLUIDO COM SUCESSO, APERTE ENTER PARA CONTINUAR...")
    else: 
        input("EXCLUSÃO CANCELADA, APERTE ENTER PARA CONTINUAR...")
    return menu()

def listagem():
    print(f"\n==========================================================================")
    print(f"||                 L I S T A G E M   D E  P R O D U T O S               ||")
    print(f"==========================================================================")
    cursor.execute("SELECT * FROM produtos_pi ORDER BY codigo_produto ASC")
    #produtos = cursor.fetchall()
    produto_excluido = cursor
    for produto in  produto_excluido:
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
    input("\nAPERTE ENTER PARA CONTINUAR...")
    return menu()

menu()
cursor.close()
connection.close()