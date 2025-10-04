from farmacia.entidades.produto import Produto, Lote
from datetime import date, timedelta
from typing import List, Dict

class Estoque:
    def __init__(self):
        self.__inventario: Dict[str, Dict] = {}

    def adicionar_lote(self, produto: Produto, codigo_lote: str, quantidade: int, data_validade: date) -> None:
        novo_lote = Lote(codigo_lote, quantidade, data_validade)
        chave_produto = produto.codigo

        if chave_produto in self.__inventario:
            self.__inventario[chave_produto]["lotes"].append(novo_lote)
            print(f"Novo lote {codigo_lote} adicionado ao produto existente '{produto.nome}'.")
        else:
            self.__inventario[chave_produto] = {"produto": produto, "lotes": [novo_lote]}

            print(f"Produto novo '{produto.nome}'adicionado ao inventário com o lote {codigo_lote}.")


    def dar_baixa_por_venda(self, produto: Produto, quantidade: int) -> bool:
        chave_produto = produto.codigo

        if chave_produto not in self.__inventario:
            print(f"Produto '{produto.nome}' não encontrado.")
            return False
        else:
            lista_de_lotes = self.__inventario[chave_produto]["lotes"]

        estoque_total_produto = 0
        for lote in lista_de_lotes:
            estoque_total_produto += lote.quantidade

        if estoque_total_produto < quantidade:
            print(f"Estoque insuficiente para '{produto.nome}'.")
            return False
        
        lista_de_lotes.sort(key=lambda lote: lote.data_validade)

        for lote in lista_de_lotes:
            if quantidade == 0:
                break

            elif lote.quantidade >= quantidade:
                lote.quantidade -= quantidade
                quantidade = 0 
            
            else: 
                quantidade -= lote.quantidade
                lote.quantidade = 0

        return True

    def estornar_item(self, produto: Produto, quantidade: int) -> None:
        chave_produto = produto.codigo

        if chave_produto not in self.__inventario:
            print(f"Tentativa de estornar produto não existente no inventário: {produto.nome}") 
            return
        
        lista_de_lotes = self.__inventario[chave_produto]["lotes"]

        if not lista_de_lotes:
            print(f"produto: {produto.nome} não possui lotes")
            return 

        lista_de_lotes.sort(key=lambda lote: lote.data_validade, reverse=True)

        lote_alvo = lista_de_lotes[0]
        lote_alvo.quantidade += quantidade
        print(f"Estornado {quantidade} un. para o lote {lote_alvo.codigo_lote} do produto '{produto.nome}'.")

    def registrar_perda(self, lote: Lote, quantidade: int, motivo: str) -> None:
        if quantidade <= 0 or quantidade > lote.quantidade:
            print("Quantidade inválida ou maior que o estoque do lote")
            return
        
        lote_encontrado = False
        for dados_produtos in self.__inventario.values():
            if lote in dados_produtos["lotes"]:
                lote_encontrado = True
                break

        if not lote_encontrado:
            print(f"O lote {lote.codigo_lote} não foi encontrado no inventário.")
            return
        
        lote.quantidade -= quantidade

        print(f"Registrada perda de {quantidade} un. do lote {lote.codigo_lote}. Motivo: {motivo}")

    def consultar_lote_produto(self, produto: Produto) -> List[Lote]:
        chave_produto = produto.codigo
        dados_produto = self.__inventario.get(chave_produto)
        
        if dados_produto:
            return dados_produto["lotes"]
        
        return []

    def listar_produtos_baixo_estoque(self, limite_minimo: int) -> List[Produto]:
        produtos_em_falta = []

        for dados_produtos in self.__inventario.values():
            estoque_total = sum(lote.quantidade for lote in dados_produtos["lotes"])
            if estoque_total <= limite_minimo:
                produtos_em_falta.append(dados_produtos["produto"])
        return produtos_em_falta


    def listar_produtos_proximo_vencimento(self,        dias_limite: int) -> List[Lote]:
        lotes_a_vencer = []
        data_limite = date.today() + timedelta(days=dias_limite)
        
        for dados_produtos in self.__inventario.values():
            for lote in dados_produtos["lotes"]:
                if lote.data_validade <= data_limite:
                    lotes_a_vencer.append(lote)
        
        return lotes_a_vencer


    def __str__(self) -> str:
        if not self.__inventario:
            return "Estoque vazio"
        
        resumo = "Resumo do estoque\n"
        for dados_produto in self.__inventario.values():
            produto = dados_produto["produto"]
            estoque_total = sum(lote.quantidade for lote in dados_produto["lotes"])
            resumo += f"produto: {produto.nome} | estoque total: {estoque_total} unidades\n"
        
        return resumo    