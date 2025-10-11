from farmacia.entidades.pessoa import Cliente, Funcionario
from farmacia.entidades.produto import Lote, Medicamento, Perfumaria
from farmacia.servicos.estoque import Estoque
from farmacia.servicos.venda import HistoricoVendas, ItemVenda, Orcamento, Venda
from datetime import date
import os

def exibir_menu(titulo: str, opcoes: list) -> None:
    largura = 50
    print("+" + "-" * (largura + 2) + "+")
    print(f"| {titulo.center(largura)} |")
    print("+" + "=" * (largura + 2) + "+")
    for i, opcao in enumerate(opcoes):
        texto_da_opcao = f"{i + 1}. {opcao}"
        print(f"| {texto_da_opcao.ljust(largura)} |")
    print("+" + "-" * (largura + 2) + "+")

def menu_caixa(estoque: Estoque, historico: HistoricoVendas, funcionario: Funcionario, cliente: Cliente):
    pass

def menu_balcao(lista_de_clientes: list, lista_de_funcionarios: list, estoque: Estoque, historico: HistoricoVendas, funcionario: Funcionario):
    while True:
        titulo_menu = "MÓDULO DO BALCÃO"
        opcoes_menu = [
            "Gerenciar Clientes",
            "Gerenciar Funcionarios",
            "Gerenciar Produtos",
            "Gerenciar Relatórios de Estoque"
            ]
        exibir_menu(titulo_menu, opcoes_menu)
        largura_menu = 50
        print(f"| {'0. Voltar ao Menu Principal'.ljust(largura_menu)} |")
        print("+" + "-" * (largura_menu + 2) + "+")

        try:
            escolha = int(input("Digite sua opção: "))
        except ValueError:
            print("ERRO: Por favor, digite um número.")
            input("Pressione Enter para seguir...")
            continue

        if escolha == 1:
            submenu_clientes(lista_de_clientes, historico)
        elif escolha == 2:
            submenu_funcionarios(lista_de_funcionarios, historico)
        elif escolha == 3:
            submenu_produtos(estoque)
        elif escolha == 4:
            submenu_relatorios(estoque)
        elif escolha == 0:
            print("Voltando ao Menu Principal...")
            break
        else:
            print("ERRO: Opção não existe.")

def submenu_clientes(lista_de_clientes: list, historico: HistoricoVendas):
    while True:
        titulo = "GERENCIAR CLIENTES"
        opcoes = [
            "Cadastrar Novo Cliente",
            "Listar Todos os Clientes",
            "Consultar Histórico de um Cliente",
            "Atualizar Cliente",
            "Deletar Cliente" 
        ]
        exibir_menu(titulo, opcoes)
        largura_menu = 50
        print(f"| {'0. Voltar'.ljust(largura_menu)} |")
        print("+" + "-" * (largura_menu + 2) + "+")
        
        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para continuar...")
            continue

        if escolha == 1:
            print("\n--- Cadastro de Novo Cliente ---")
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            novo_cliente = Cliente(nome, cpf)
            lista_de_clientes.append(novo_cliente)

            print(f"\n Cliente '{novo_cliente.nome}' cadastrado com o ID: {novo_cliente.id_cliente}")
            input("Pressione Enter para continuar...")

        elif escolha == 2:
            print("\n--- Lista de Clientes Cadastrados ---")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado.")
            else:
                for cliente in lista_de_clientes:
                    print(cliente)
            input("\nPressione Enter para continuar...")

        elif escolha == 3:
            print("\n--- Consultar Histórico de Cliente ---")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado para consultar.")
                input("\nPressione Enter para continuar...")
                continue 

            for cliente in lista_de_clientes:
                print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome}")
            
            try:
                id_busca = int(input("\nDigite o ID do cliente para ver o histórico: "))
                
                cliente_encontrado = None
                for cliente in lista_de_clientes:
                    if cliente.id_cliente == id_busca:
                        cliente_encontrado = cliente
                        break
                
                if cliente_encontrado:
                    vendas_cliente = historico.consultar_historico_cliente(cliente_encontrado)
                    print(f"\n--- Histórico de Compras de {cliente_encontrado.nome} ---")
                    if not vendas_cliente:
                        print("Nenhuma compra registrada para este cliente.")
                    else:
                        for venda in vendas_cliente:
                            print(venda) 
                else:
                    print("ERRO: Nenhum cliente encontrado com o ID informado.")

            except ValueError:
                print("ERRO: ID inválido. Digite apenas números.")
            
            input("\nPressione Enter para continuar...")

        elif escolha == 4:
            print("\n--- Atualizar Cliente ---")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado para atualizar.")
                input("\nPressione Enter para continuar...")
                continue

            for cliente in lista_de_clientes:
                print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome}")
            
            try:
                id_busca = int(input("\nDigite o ID do cliente para atualizá-lo: "))
                cliente_encontrado = None
                for cliente in lista_de_clientes:
                    if cliente.id_cliente == id_busca:
                        cliente_encontrado = cliente
                        break

                if cliente_encontrado:
                    print("(Deixe em branco e pressione Enter para não alterar)")
                    
                    novo_nome = input("Digite o novo nome: ")
                    if novo_nome:
                        cliente_encontrado.nome = novo_nome 

                    novo_cpf = input(f"Digite o novo CPF: ")
                    if novo_cpf:
                        cliente_encontrado.cpf = novo_cpf 
                    
                    print(f"\n[SUCESSO] Dados do cliente atualizados!")
                    print(f"Novos dados: {cliente_encontrado}")
                else:
                    print("ERRO: Nenhum cliente encontrado com o ID informado.")

            except ValueError:
                print("ERRO: ID inválido. Digite apenas números.")
            input("Pressione Enter para continuar...")

        elif escolha == 5:
            print("\n--- Deletar Cliente ---")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado para remover.")
                input("\nPressione Enter para continuar...")
                continue

            for cliente in lista_de_clientes:
                print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome}")
            
            try:
                id_busca = int(input("\nDigite o ID do cliente para removê-lo: "))

                cliente_encontrado = None
                for cliente in lista_de_clientes:
                    if cliente.id_cliente == id_busca:
                        cliente_encontrado = cliente
                        break

                if cliente_encontrado:
                    lista_de_clientes.remove(cliente_encontrado)
                    print(f"{cliente_encontrado.nome}, removido com sucesso")
                else:
                    print("ERRO: Nenhum cliente encontrado com o ID informado.")

            except ValueError:
                print("ERRO: ID inválido. Digite apenas números.")

            input("Pressione Enter para continuar...")    


        elif escolha == 0:
            break
        else:
            print("Opção em construção ou inválida.")
            input("Pressione Enter para continuar...")

def submenu_funcionarios(lista_de_funcionarios: list, historico: HistoricoVendas):
    while True:
        titulo = "GERENCIAR FUNCIONÁRIOS"
        opcoes = [
            "Cadastrar Novo Funcionário",
            "Listar Todos os Funcionários",
            "Consultar Histórico de um Funcionário",
            "Atualizar Funcionário",
            "Deletar Funcionário" 
        ]
        exibir_menu(titulo, opcoes)
        largura_menu = 50
        print(f"| {'0. Voltar'.ljust(largura_menu)} |")
        print("+" + "-" * (largura_menu + 2) + "+")
        
        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para continuar...")
            continue

        if escolha == 1:
            print("\n--- Cadastro de Novo Funcionário ---")
            nome = input("Digite o nome do funcionário: ")
            cpf = input("Digite o CPF do funcionário: ")
            novo_funcionário = Funcionario(nome, cpf)
            lista_de_funcionarios.append(novo_funcionário)

            print(f"\n Funcionário '{novo_funcionário.nome}' cadastrado com a matrícula: {novo_funcionário.matricula}")
            input("Pressione Enter para continuar...")

        elif escolha == 2:
            print("\n--- Lista de Funcionários Cadastrados ---")
            if not lista_de_funcionarios:
                print("Nenhum funcionário cadastrado.")
            else:
                for funcionario in lista_de_funcionarios:
                    print(funcionario)
            input("\n Pressione Enter para continuar...")

        elif escolha == 3:
            print("\n--- Consultar Histórico de Funcionário ---")
            if not lista_de_funcionarios:
                print("Nenhum funcionário cadastrado para consultar.")
                input("\n Pressione Enter para continuar...")
                continue 

            for funcionario in lista_de_funcionarios:
                print(f"Matrícula: {funcionario.matricula} | Nome: {funcionario.nome}")
            
            try:
                matricula_busca = str(input("\n Digite a matrícula do funcionário para ver o histórico: ").upper())
                
                funcionario_encontrado = None
                for funcionario in lista_de_funcionarios:
                    if funcionario.matricula == matricula_busca:
                        funcionario_encontrado = funcionario
                        break
                
                if funcionario_encontrado:
                    vendas_funcionario = historico.consultar_historico_funcionario(funcionario_encontrado)
                    print(f"\n--- Histórico de Compras de {funcionario_encontrado.nome} ---")
                    if not vendas_funcionario:
                        print("Nenhuma compra registrada para este funcionário.")
                    else:
                        for venda in vendas_funcionario:
                            print(venda) 
                else:
                    print("ERRO: Nenhum funcionário encontrado com a matrícula informada.")

            except ValueError:
                print("ERRO: Matrícula inválida.")
            
            input("\n Pressione Enter para continuar...")

        elif escolha == 4:
            print("\n--- Atualizar Funcionário ---")
            if not lista_de_funcionarios:
                print("Nenhum funcionário cadastrado para atualizar.")
                input("\n Pressione Enter para continuar...")
                continue

            for funcionario in lista_de_funcionarios:
                print(f"Matrícula: {funcionario.matricula} | Nome: {funcionario.nome}")
            
            try:
                matricula_busca = str(input("\nDigite a matrícula do funcionário para atualizá-lo: ")).upper()
                funcionario_encontrado = None
                for funcionario in lista_de_funcionarios:
                    if funcionario.matricula == matricula_busca:
                        funcionario_encontrado = funcionario
                        break

                if funcionario_encontrado:
                    print("(Deixe em branco e pressione Enter para não alterar)")
                    
                    novo_nome = input("Digite o novo nome: ")
                    if novo_nome:
                        funcionario_encontrado.nome = novo_nome 

                    novo_cpf = input(f"Digite o novo CPF: ")
                    if novo_cpf:
                        funcionario_encontrado.cpf = novo_cpf 
                    
                    print(f"\n[SUCESSO] Dados do funcionário atualizados!")
                    print(f"Novos dados: {funcionario_encontrado}")
                else:
                    print("ERRO: Nenhum funcionário encontrado com a matrícula informada.")

            except ValueError:
                print("ERRO: Matrícula inválida.")
            input("Pressione Enter para continuar...")

        elif escolha == 5:
            print("\n--- Deletar Funcionário ---")
            if not lista_de_funcionarios:
                print("Nenhum funcionário cadastrado para remover.")
                input("\nPressione Enter para continuar...")
                continue

            for funcionario in lista_de_funcionarios:
                print(f"Matrícula: {funcionario.matricula} | Nome: {funcionario.nome}")
            
            try:
                matricula_busca = str(input("\n Digite a Matrícula do funcionário para removê-lo: ")).upper()

                funcionario_encontrado = None
                for funcionario in lista_de_funcionarios:
                    if funcionario.matricula == matricula_busca:
                        funcionario_encontrado = funcionario
                        break

                if funcionario_encontrado:
                    lista_de_funcionarios.remove(funcionario_encontrado)
                    print(f"{funcionario_encontrado.nome}, removido com sucesso")
                else:
                    print("ERRO: Nenhum funcionário encontrado com a matrícula informada.")

            except ValueError:
                print("ERRO: ID inválido. Digite apenas números.")

            input("Pressione Enter para continuar...")    


        elif escolha == 0:
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def submenu_produtos(estoque: Estoque):
    while True:
        titulo = "GERENCIAR PRODUTOS"
        opcoes = [
            "Cadastrar Novo Produto",
            "Listar Todos os Produtos",
            "Atualizar Produto",
            "Deletar Produto"
            ]
        exibir_menu(titulo, opcoes)
        largura_menu = 50
        print(f"| {'0. Voltar'.ljust(largura_menu)} |")
        print("+" + "-" * (largura_menu + 2) + "+")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para continuar...")
            continue
        
        if escolha == 1:
            print("\n--- Cadastro de Novo Produto ---")
            try:
                tipo = input("Tipo (1-Medicamento, 2-Perfumaria), escolha o desejado: ")
                codigo = input("Código do produto: ").upper()
                nome = input("Nome do produto: ")
                preco = float(input("Preço de venda: R$ "))
                codigo_lote = input("Código do primeiro lote: ").upper()
                quantidade = int(input("Quantidade inicial no lote: "))
                ano = int(input("Ano de validade (AAAA): "))
                mes = int(input("Mês de validade (MM): "))
                dia = int(input("Dia de validade (DD): "))
                data_validade = date(ano, mes, dia)

                if tipo == '1':
                    receita = input("Exige receita? (s/n): ").lower() == 's'
                    novo_produto = Medicamento(codigo, nome, preco, receita)
                elif tipo == '2':
                    volume = input("Volume/Descrição (ex: 250ml): ")
                    novo_produto = Perfumaria(codigo, nome, preco, volume)
                else:
                    print("Tipo de produto inválido.")
                    continue
                
                estoque.adicionar_lote(novo_produto, codigo_lote, quantidade, data_validade)

            except ValueError:
                print("ERRO: Preço, data de validade ou quantidade inválidos. Digite apenas números.")
            input("\n Pressione Enter para continuar...")

        elif escolha == 2:
            print("\n--- Lista de Produtos no Estoque ---")
            todos_os_produtos = estoque.produtos
            if not todos_os_produtos:
                print("Nenhum produto cadastrado no estoque.")
            else:
                print(f"\n{'NOME DO PRODUTO'.ljust(30)} | {'ESTOQUE TOTAL'.ljust(15)} | {'PREÇO'.ljust(15)}")
                print("-" * 65)
                for produto in todos_os_produtos:
                    lotes_do_produto = estoque.consultar_lotes_produto(produto)
                    estoque_total = sum(lote.quantidade for lote in lotes_do_produto)
                    preco_formatado = f"R$ {produto.preco:.2f}"
                    print(f"{produto.nome.ljust(30)} | {str(estoque_total).ljust(15)} | {preco_formatado.ljust(15)}")
            input("\n Pressione Enter para continuar...")

        elif escolha == 3:
            print("\n--- Atualizar Produto ---")
            
            print("\n --- Produtos disponíveis ---")
            for produto in estoque.produtos:
                print(f"Código: {produto.codigo} | Nome: {produto.nome}")

            codigo_busca = input("Digite o código do produto que deseja atualizar: ").upper()
            
            produto_encontrado = None
            for produto in estoque.produtos:
                if produto.codigo == codigo_busca:
                    produto_encontrado = produto
                    break
            
            if produto_encontrado:
                print("(Deixe em branco e pressione Enter para não alterar)")
                try:
                    novo_preco_str = input("Digite o novo preço: ")
                    if novo_preco_str:
                        produto_encontrado.preco = float(novo_preco_str)
                    print("Produto atualizado.")
                except ValueError:
                    print("Preço inválido.")
            else:
                print("ERRO: Nenhum produto encontrado com o código informado.")
            input("\n Pressione Enter para continuar...")

        elif escolha == 4:
            print("\n--- Deletar Produto ---")

            if not estoque.produtos:
                print("Nenhum produto cadastrado para deletar.")
            else:
                for produto in estoque.produtos:
                    print(f"Código: {produto.codigo} | Nome: {produto.nome}")

            codigo_busca = input("Digite o código do produto que deseja deletar: ").upper()
            sucesso = estoque.remover_produto(codigo_busca)
            if sucesso:
                    print("\nOperação concluída.")
            else:
                print("\nOperação não concluída.")
            input("\nPressione Enter para continuar...")

        elif escolha == 0:
            break
        else:
            print("ERRO: Opção não existe.")
            input("Pressione Enter para continuar...")

def submenu_relatorios(estoque: Estoque):
    while True:
        titulo = "GERAR RELATÓRIOS"
        opcoes = [
            "Produtos com Baixo Estoque",
            "Lotes Próximos ao Vencimento"
            ]
        
        exibir_menu(titulo, opcoes)
        largura_menu = 50
        print(f"| {'0. Voltar'.ljust(largura_menu)} |")
        print("+" + "-" * (largura_menu + 2) + "+")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para continuar...")
            continue
        
        if escolha == 1:
            try:
                limite = int(input("\nListar produtos com estoque menor ou igual a: "))
                print(f"\n--- Relatório: Produtos com Baixo Estoque dado Limite: {limite}) ---")
                
                produtos_encontrados = estoque.listar_produtos_baixo_estoque(limite)

                if not produtos_encontrados:
                    print("Nenhum produto encontrado com estoque baixo.")
                else:
                    print(f"\n{'NOME DO PRODUTO'.ljust(30)} | {'CÓDIGO'.ljust(15)} | {'ESTOQUE ATUAL'}")
                    print("-" * 65)
                    for produto, quantidade in produtos_encontrados:
                        print(f"{produto.nome.ljust(30)} | {produto.codigo.ljust(15)} | {quantidade}")

            except ValueError:
                print("ERRO: Limite inválido. Digite apenas um número.")

            input("\nPressione Enter para continuar...")

        elif escolha == 2:
            try:
                dias = int(input("\nListar lotes que vencem nos próximos (dias): "))
                print(f"\n--- Relatório: Lotes a Vencer nos Próximos {dias} Dias ---")

                lotes_encontrados = estoque.listar_produtos_proximo_vencimento(dias)

                if not lotes_encontrados:
                    print("Nenhum lote encontrado próximo do vencimento.")
                else:
                    print(f"\n{'PRODUTO'.ljust(25)} | {'LOTE'.ljust(15)} | {'QTD'.ljust(5)} | {'DATA DE VENCIMENTO'}")
                    print("-" * 75)
                    for produto, lote in lotes_encontrados:
                        data_str = lote.data_validade.strftime('%d/%m/%Y')
                        print(f"{produto.nome.ljust(25)} | {lote.codigo_lote.ljust(15)} | {str(lote.quantidade).ljust(5)} | {data_str}")
            except ValueError:
                print("ERRO: Número de dias inválido.")
            input("\nPressione Enter para continuar...")
            
        elif escolha == 0:
            break
        else:
            print("ERRO: Opção não existe.")
            input("Pressione Enter para continuar...")

def main():
    estoque = Estoque()
    historico = HistoricoVendas()
    func_teste = Funcionario("Funcionario Teste", "000.000.000-00")
    cliente_teste = Cliente("Cliente Teste", "111.111.111-11")
    med_teste = Medicamento("MED_TESTE", "med_teste", 4.99, False)
    estoque.adicionar_lote(med_teste, "diplote001", 100, date(2027, 5, 16))
    lista_de_clientes = [cliente_teste]
    lista_de_funcionarios = [func_teste]

    while True:
        titulo_menu = "MENU PRINCIPAL"
        opcoes_menu = ["Módulo Caixa", "Módulo Balcão", "Sair do Sistema"]
        exibir_menu(titulo_menu, opcoes_menu)

        try:
            escolha = int(input("Digite sua opção: "))
        except ValueError:
            print("ERRO: Por favor, digite um número.")
            input("Pressione Enter para seguir...")
            continue

        if escolha == 1:
            menu_caixa(estoque, historico, func_teste, cliente_teste)

        elif escolha == 2:
            menu_balcao(lista_de_clientes, lista_de_funcionarios, estoque, historico, func_teste)

        elif escolha == 3:
            print("Saindo do sistema.")
            break
        else:
            print("ERRO: Opção inválida, escolha entre 1, 2 ou 3.")
            input("Pressione Enter para continuar")
    

if __name__ == "__main__": main()