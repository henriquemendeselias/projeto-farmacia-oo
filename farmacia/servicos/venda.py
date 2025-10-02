from farmacia.entidades.produto import Produto
from farmacia.entidades.pessoa import Funcionario, Cliente
from datetime import datetime

class ItemVenda:
    def __init__(self, produto: Produto, quantidade: int):
        if quantidade <= 0:
            raise ValueError("a quantidade de um item deve ser positiva")
        
        self.__produto = produto
        self.__quantidade = quantidade
        self.__preco_momento = produto.preco

    @property
    def produto(self) -> Produto:
        return self.__produto
        
    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @property
    def preco_momento(self) -> float:
        return self.__preco_momento
        
    def calcular_subtotal(self) -> float:
        return self.__quantidade * self.__preco_momento
        
    def __str__(self) -> str:
        subtotal = self.calcular_subtotal()
        return f"{self.__produto.nome} com {self.__quantidade} unidades, Preço Un.: R${self.__preco_momento:.2f} | Subtotal: R${subtotal:.2f}"
    
class Venda:
    _contador_id = 0
    def __init__(self,  funcionario: Funcionario, cliente: Cliente):
        Venda._contador_id += 1
        self.__id_venda = Venda._contador_id
        self.__funcionario = funcionario
        self.__cliente = cliente
        self.__data_hora = datetime.now()
        self.__itens = []
        self.__valor_total = 0.0
        self.__status = "ATIVA"

    @property
    def id_venda(self) -> int:
        return self.__id_venda

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def funcionario(self) -> Funcionario:
        return self.__funcionario
    
    @property
    def data_hora(self) -> datetime:
        return self.__data_hora

    @property
    def itens(self) -> list:
        return self.__itens

    @property
    def valor_total(self) -> float:
        return self.__valor_total
        
    @property
    def status(self) -> str:
        return self.__status
    
    def adicionar_item(self, produto: Produto, quantidade: int) -> None:
        novo_item = ItemVenda(produto, quantidade)
        self.__itens.append(novo_item)
        self._recalcular_total()

    def remover_item(self, item: ItemVenda) -> None:
        if item in self.__itens:
            self.__itens.remove(item)
            self._recalcular_total()
            print("produto adicio...")
        else:
            print("não foi...")

    def _recalcular_total(self) -> None:
        total_atualizado = 0.0
        for item in self.__itens:
            s = item.calcular_subtotal()
            total_atualizado += s

        self.__valor_total = total_atualizado
    
    def finalizar_venda(self, estoque, historico) -> None:
        if self.__status != "ATIVA":
            print("impossível finalizar venda não ativa")
            return
        
        for item in self.__itens:
            estoque.dar_baixa_por_venda(item.produto, item.quantidade)

        self.__status = "FINALIZADA"
        print(f"status da venda {self.id_venda} atualizada para 'FINALIZADA'.")

        #historico.registrarVenda(self)

    def cancelar_venda(self, estoque) -> None:
        if self.__status == "ATIVA" or self.__status == "PAUSADA":
            self.__status = "CANCELADA"
            print(f"venda {self.id_venda} (em andamento) cancelada")
        elif self.__status == "FINALIZADA":
            for item in self.__itens:
                estoque.estornar_item(item.produto, item.quantidade)
            self.__status = "CANCELADA"
            print(f"venda{self.id_venda} estornada com sucesso")
    
    def pausar_venda(self) -> None:
        if self.__status == "ATIVA":
            self.__status = "PAUSADA"
            print(f"venda {self.id_venda} pausada")
        else:
            print("impossível pausar esta venda")

    def retomar_venda(self) -> None:
        if self.__status == "PAUSADA":
            self.__status = "ATIVA"
        else:
            print("impossível retomar esta venda")

    def aplicar_desconto(self, percentual: float):
        if not 0 <= percentual <= 100:
            print("percentual inválido")
            return
        
        desconto_decimal = percentual / 100.0
        fator_multiplicador = 1 - desconto_decimal
        novo_valor = self.__valor_total * fator_multiplicador
        self.__valor_total = novo_valor
        print(f"desconto de {percentual}% aplicado. novo total: R$ {self.__valor_total:.2f}")
    
    def processar_pagamento(self, forma: str, valor: float) -> bool:
        if self.__status != "ATIVA":
            print("pagamento não pode ser processado para uma venda que não está ativa.")
            return False

        if valor >= self.__valor_total:
            print(f"Total da Venda: R$ {self.__valor_total:.2f}")
            print(f"Valor Pago: R${valor:.2f}")
            print(f"Forma: {forma}")
            if forma.lower() == 'dinheiro':
                troco = valor - self.__valor_total
                print(f"Troco: R${troco:.2f}")
            print("Pagamento APROVADO.")
            return True
        else:
            print(f"Total da Venda: R$ {self.__valor_total:.2f}")
            print(f"Valor Pago: R${valor:.2f}")
            print("Valor pago é insuficiente.")
            print("Pagamento RECUSADO.")
            return False


    def __str__(self) -> str:
        cabecalho = (
            f"--- Venda ID: {self.id_venda} | Status: {self.status} ---\n"
            f"Data: {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Cliente: {self.cliente.nome}\n"
            f"Funcionário: {self.funcionario.nome}\n"
            f"{'-'*40}\n"
        )

        itens_str = ""
        if not self.itens:
            itens_str = "Nenhum item na venda.\n"
        else:
            for item in self.itens:
                itens_str += f"- {item}\n"
        
        rodape = (
            f"{'-'*40}\n"
            f"Valor Total: R$ {self.valor_total:.2f}\n"
            f"{'='*40}"
        )

        return cabecalho + itens_str + rodape