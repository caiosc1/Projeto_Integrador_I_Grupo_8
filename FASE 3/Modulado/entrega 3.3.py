#TODO modularizar as contas, fazer validação na inserção do código (não pode ser igual a algum existente) e da descrição (possuir apenas letras validas)

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

    print("==========================================================================")
    print("||                                                                      ||")
    print("||      S I S T E M A   D E   C O N T R O L E   D E   E S T O Q U E     ||")
    print("||                                                                      ||")
    print("==========================================================================")
    print("||                                                                      ||")
    print("||                                  M E N U                             ||")
    print("||                                                                      ||")
    print("==========================================================================")
    print("|| 1. Inserir  |  2. Alterar  |  3. Excluir  |  4. Listar  |  5. Sair   ||")
    print("==========================================================================")

    escolha_menu = str(input("\n\nDIGITE A OPÇÃO DESEJADA(NÚMERO): "))
    
    return escolha_menu


def menu_insercao():
    print(f"\n==========================================================================")
    print(f"||                   I N S E R Ç Ã O   D E   D A D O S                  ||")
    print(f"==========================================================================")

    codigoProduto = validacao_codigo()
    nomeProduto = str(input("Digite o nome do produto: "))
    descricaoProduto = validacao_descricao(str(input("Digite a descrição do produto: ")))
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
    
    descricaoProduto = criptografar(descricaoProduto)
    cursor.execute(f"INSERT INTO produtos_pi VALUES({codigoProduto}, '{nomeProduto}', '{descricaoProduto}', {custoProduto}, {impostos}, {custoFixo}, {comissaoVenda}, {rentabilidade})")
    connection.commit()

    input("DADOS DO PRODUTO INSERIDOS COM SUCESSO, APERTE ENTER PARA VOLTAR AO MENU...")


def menu_alteracao():
    print(f"\n==========================================================================")
    print(f"||                A L T E R A Ç Ã O   D E   D A D O S                   ||")
    print(f"==========================================================================")

    listaMudancas = {1:"nome" ,2: "descriçao",3: "custo_produto", 4: "custo_fixo",5: "comissao_vendas",6: "impostos",7: "rentabilidade"}
    valsstring = [1, 2]
    codigoProduto = existencia_codigo()
    cursor.execute(f"SELECT * FROM produtos_pi WHERE codigo_produto = {codigoProduto}")
    produto_excluido = cursor

    for produto in produto_excluido:
        #             Nome, descrição, custo,custo fixo, comissão, impostos, rentabilidade
        infProd = [produto[1],produto[2],produto[3],produto[5],produto[6],produto[4],produto[7]]
        #Tela de apresentação dos resultados
        print("--------------------------------------------------------")
        print(f"\t1. Nome: {produto[1]}")
        print(f"\t2. Descrição: {descriptografar(produto[2])}")
        print(f"\t3. Custo de Aquisição: {produto[3]}")
        print(f"\t4. Custo Fixo/Administrativo: {produto[5]}")
        print(f"\t5. Comissão de Vendas: {produto[6]}")
        print(f"\t6. Impostos: {produto[4]}")
        print(f"\t7. Rentabilidade: {produto[7]}")
        print("--------------------------------------------------------")

    escolhaAlteracao = int(input("DIGITE O NÚMERO DO CAMPO QUE DESEJA ALTERAR: "))

    if escolhaAlteracao in valsstring:
        alteracao = str(input("DIGITE O NOVO VALOR DO CAMPO ESCOLHIDO: "))
        if escolhaAlteracao == 2:
            alteracao = validacao_descricao(alteracao)
            alteracao = criptografar(alteracao)
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


def menu_exclusao():
    print(f"\n==========================================================================")
    print(f"||                   E X C L U S Ã O   D E   D A D O S                  ||")
    print(f"==========================================================================")

    codigoProduto = existencia_codigo()
    cursor.execute(f"SELECT * FROM produtos_pi WHERE codigo_produto = {codigoProduto}")
    produto_excluido = cursor

    calculo_produtos(produto_excluido)

    escolha_exclusao = str(input("DESEJA REALMENTE EXCLUIR O PRODUTO(S/N): "))

    if escolha_exclusao.upper() == "S":
        cursor.execute(f"DELETE produtos_pi WHERE codigo_produto = {codigoProduto}")
        connection.commit()
        input("PRODUTO EXCLUIDO COM SUCESSO, APERTE ENTER PARA CONTINUAR...")

    else: 
        input("EXCLUSÃO CANCELADA, APERTE ENTER PARA CONTINUAR...")


def listagem():
    print(f"\n==========================================================================")
    print(f"||                 L I S T A G E M   D E  P R O D U T O S               ||")
    print(f"==========================================================================")
    cursor.execute("SELECT * FROM produtos_pi ORDER BY codigo_produto ASC")
    #produtos = cursor.fetchall()
    produtos_listagem = cursor

    calculo_produtos(produtos_listagem)

    input("\nAPERTE ENTER PARA CONTINUAR...")


def criptografar(descricao):
    letras = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 0}
    numeros = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h", 9: "i", 10: "j", 11: "k", 12: "l", 13: "m", 14: "n", 15: "o", 16: "p", 17: "q", 18: "r", 19: "s", 20: "t", 21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 0: "z"}
    descricao_letras = descricao
    descricao_em_numeros = []
    descricao_numeros_criptografada = []
    descricao_letras_criptografado = ""
    primeira_linha_matriz = [11, 13]
    segunda_linha_matriz = [2, 3]

    """
        Transforma a palavra em numeros
    """

    for i in range(len(descricao_letras)):
        descricao_em_numeros.append(letras.get(descricao_letras[i]))

    """
        Faz a criptografia
    """

    while len(descricao_em_numeros) > 0:
        if len(descricao_em_numeros) >= 2:
            numero_criptografado = (primeira_linha_matriz[0] * descricao_em_numeros[0] + primeira_linha_matriz[1] * descricao_em_numeros[1]) % 26
            descricao_numeros_criptografada.append(numero_criptografado)
            numero_criptografado = (segunda_linha_matriz[0] * descricao_em_numeros[0] + segunda_linha_matriz[1] * descricao_em_numeros[1]) % 26
            descricao_numeros_criptografada.append(numero_criptografado)
        else:
            numero_criptografado = descricao_em_numeros[0]
            descricao_numeros_criptografada.append(numero_criptografado)

        descricao_em_numeros = descricao_em_numeros[2:]

    """
        Transforma a palavra criptografa em letras
    """

    for i in range(len(descricao_numeros_criptografada)):
        descricao_letras_criptografado += numeros.get(descricao_numeros_criptografada[i])

    return descricao_letras_criptografado

def descriptografar(descricao_criptografada):
    letras = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 0}
    numeros = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h", 9: "i", 10: "j", 11: "k", 12: "l", 13: "m", 14: "n", 15: "o", 16: "p", 17: "q", 18: "r", 19: "s", 20: "t", 21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 0: "z"}
    descricao_letras = descricao_criptografada
    descricao_em_numeros = []
    descricao_numeros_descriptografado = []
    descricao_letras_descriptografado = ""
    primeira_linha_matriz = [11, 13]
    segunda_linha_matriz = [2, 3]
    primeira_linha_matriz = [11, 13]
    segunda_linha_matriz = [2, 3]

    """
        faz a matriz inversa e calcula o determinante e o inverso modular
    """
    primeira_linha_matriz_inversa = [segunda_linha_matriz[1], -primeira_linha_matriz[1]]
    segunda_linha_matriz_inversa = [-segunda_linha_matriz[0], primeira_linha_matriz[0]]

    determinante = primeira_linha_matriz[0] * segunda_linha_matriz[1] - primeira_linha_matriz[1] * segunda_linha_matriz [0]
    inverso_modular = 1

    while ((determinante * inverso_modular) % 26) != 1:
        inverso_modular += 1
    #print(determinante)
    #print(inverso_modular)

    """
        calcula a chave
    """
    chave_primeira_linha = [(inverso_modular*primeira_linha_matriz_inversa[0]) % 26, (inverso_modular*primeira_linha_matriz_inversa[1]) % 26]
    chave_segunda_linha = [(inverso_modular*segunda_linha_matriz_inversa[0]) % 26, (inverso_modular*segunda_linha_matriz_inversa[1]) % 26]

    """
        Transforma a palavra em numeros
    """

    for i in range(len(descricao_letras)):
        descricao_em_numeros.append(letras.get(descricao_letras[i]))

    """
        pega a palavra criptografada em numeros e descriptografa
    """

    while len(descricao_em_numeros) > 0:
        if len(descricao_em_numeros) >= 2:
            numero_descriptografado = (chave_primeira_linha[0] * descricao_em_numeros[0] + chave_primeira_linha[1] * descricao_em_numeros[1]) % 26
            descricao_numeros_descriptografado.append(numero_descriptografado)
            numero_descriptografado = (chave_segunda_linha[0] * descricao_em_numeros[0] + chave_segunda_linha[1] * descricao_em_numeros[1]) % 26
            descricao_numeros_descriptografado.append(numero_descriptografado)
        else:
            numero_descriptografado = descricao_em_numeros[0]
            descricao_numeros_descriptografado.append(numero_descriptografado)
        descricao_em_numeros = descricao_em_numeros[2:]

    """
        transforma a palavra descriptografada em letras
    """

    for i in range(len(descricao_numeros_descriptografado)):
        descricao_letras_descriptografado += numeros.get(descricao_numeros_descriptografado[i])
    
    return descricao_letras_descriptografado

def main():
    escolha = menu()

    while escolha != "5":
        if escolha == "1":
            menu_insercao()

        elif escolha == "2":
            menu_alteracao()

        elif escolha == "3":
            menu_exclusao()

        elif escolha == "4":
            listagem()
        else:
            input("ESCOLHA INVALIDA, APERTE ENTER PARA CONTINUAR...")

        escolha = menu()
    
    print("SAINDO DO PROGRAMA...")

def validacao_codigo():
    codigoProduto = int(input("Digite o código do produto: "))
    cursor.execute("SELECT codigo_produto from produtos_pi")
    for produto in cursor:
        if codigoProduto in produto:
            print("CÓDIGO DE PRODUTO JÁ UTILIZADO!\n")
            return validacao_codigo()
    return codigoProduto

def existencia_codigo():
    codigoProduto = int(input("Digite o código do produto desejado: "))
    cursor.execute("SELECT codigo_produto from produtos_pi")
    for produto in cursor:
        if codigoProduto in produto:
            return codigoProduto
    print("CODIGO DE PRODUTO INEXISTENTE!\n")
    return existencia_codigo()

def calculo_produtos(produtos_desejados):
    for produto in produtos_desejados:
        codigoProduto = produto[0]
        nomeProduto = produto[1]
        descricaoProduto = descriptografar(produto[2])
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

def validacao_descricao(descricao: str):
    descricao = descricao.lower()
    letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for letra in descricao:
        if letra not in letras:
            print("CARACTERE INVALIDO NA DESCRIÇÃO DO PRODUTO!")
            nova_descricao = str(input("Digite a descrição do produto: "))
            return validacao_descricao(nova_descricao)
    return descricao

main()
cursor.close()
connection.close()