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
            print(f"Produto {item.produto.nome} removido com sucesso")
        else:
            print(f"Produto {item.produto.nome} não encontrado na venda.")

    def _recalcular_total(self) -> None:
        total_atualizado = 0.0
        for item in self.__itens:
            s = item.calcular_subtotal()
            total_atualizado += s

        self.__valor_total = total_atualizado
    
    def finalizar_venda(self, estoque, historico: "HistoricoVendas") -> None:
        if not self.__itens:
            print("impossível finalizar venda sem itens")
            return
        
        if self.__status != "ATIVA":
            print("impossível finalizar venda não ativa")
            return
        
        for item in self.__itens:
            estoque.dar_baixa_por_venda(item.produto, item.quantidade)

        self.__status = "FINALIZADA"
        print(f"status da venda {self.id_venda} atualizada para 'FINALIZADA'.")

        historico.registrar_venda(self)

    def cancelar_venda(self, estoque) -> None:
        if self.__status == "ATIVA" or self.__status == "PAUSADA":
            self.__status = "CANCELADA"
            print(f"venda {self.id_venda} (em andamento) cancelada")
        elif self.__status == "FINALIZADA":
            for item in self.__itens:
                estoque.estornar_item(item.produto, item.quantidade)
            self.__status = "CANCELADA"
            print(f"venda{self.id_venda} estornada com sucesso")
        else:
            print(f"venda {self.id_venda} já cancelada")
    
    def pausar_venda(self) -> None:
        if self.__status == "ATIVA":
            self.__status = "PAUSADA"
            print(f"venda {self.id_venda} pausada")
        else:
            print("impossível pausar esta venda")

    def retomar_venda(self) -> None:
        if self.__status == "PAUSADA":
            self.__status = "ATIVA"
            print("venda retomada")
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
        if self.__valor_total == 0:
            print("Venda sem itens ou com valor zerado, pagamento não aplicável")
            return False
        
        if self.__status != "ATIVA":
            print("pagamento não pode ser processado para uma venda que não está ativa.")
            return False

        if round(valor, 2) >= round(self.__valor_total, 2):
            print(f"Total da Venda: R$ {self.__valor_total:.2f}")
            print(f"Valor Pago: R${valor:.2f}")
            print(f"Forma: {forma}")
            if forma.lower() == 'dinheiro':
                troco = round(valor, 2) - round(self.__valor_total, 2)
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
    

class Orcamento:
    _contador_id = 0
    def __init__(self, funcionario: Funcionario, cliente: Cliente):
        Orcamento._contador_id += 1
        self.__id_orcamento = Orcamento._contador_id
        self.__cliente = cliente
        self.__funcionario = funcionario
        self.__data_hora = datetime.now()
        self.__itens = []
        self.__valor_total = 0.0
    
    
    @property
    def id_orcamento(self) -> int:
        return self.__id_orcamento
    
    @property
    def valor_total(self) -> float:
        return self.__valor_total

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

    def _recalcular_total(self) -> None:
        total_atualizado = 0.0
        for item in self.__itens:
            total_atualizado += item.calcular_subtotal()
            
        self.__valor_total = total_atualizado

    def adicionar_item(self, produto: Produto, quantidade: int) -> None:
        novo_item = ItemVenda(produto, quantidade)
        self.__itens.append(novo_item)
        self._recalcular_total()
        
    def remover_item(self, item: ItemVenda) -> None:
        if item in self.__itens:
            self.__itens.remove(item)
            self._recalcular_total()
        else:
            print("produto não encontrado no orçamento")

    def converter_em_venda(self) -> "Venda":
        orcamento_convertido = Venda(self.funcionario, self.cliente)

        if self.itens:
            orcamento_convertido.itens.extend(self.itens)

        orcamento_convertido._recalcular_total()

        print(f"orcamento {self.id_orcamento} convertido na venda {orcamento_convertido.id_venda}")

        return orcamento_convertido

    def __str__(self) -> str:
        cabecalho = (
            f"--- Orçamento ID: {self.id_orcamento} ---\n"
            f"Data: {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Cliente: {self.cliente.nome}\n"
            f"Funcionário: {self.funcionario.nome}\n"
            f"{'-'*40}\n"
        )
        itens_str = "Itens:\n"
        if not self.itens:
            itens_str = "Nenhum item no orçamento.\n"
        else:
            for item in self.itens:
                itens_str += f"  - {item}\n"
    
        rodape = (
            f"{'-'*40}\n"
            f"Valor Total: R$ {self.valor_total:.2f}\n"
            f"{'='*40}"
        )
        return cabecalho + itens_str + rodape  

class HistoricoVendas:
    def __init__(self):
        self.__vendas_finalizadas = []

    @property 
    def vendas(self) -> list:
        return self.__vendas_finalizadas
        
    def registrar_venda(self, venda: Venda) -> None:
        if venda.status != "FINALIZADA":
            print("Impoossível registrar venda não finalizada")
            return
        else:
            self.__vendas_finalizadas.append(venda)
            print("Venda registrada")

    def buscar_venda_por_id(self, id_venda_para_busca: int) -> Venda | None:
        for venda in self.__vendas_finalizadas:
            if venda.id_venda == id_venda_para_busca:
                return venda
        return None
    

    def consultar_historico_cliente(self, cliente: Cliente) -> list:
        compras_do_cliente = []
        for venda in self.__vendas_finalizadas:
            if venda.cliente == cliente:
                compras_do_cliente.append(venda)
            
        return compras_do_cliente
        
    def consultar_historico_funcionario(self, funcionario: Funcionario) -> list:
        vendas_do_funcionario = []
        for venda in self.__vendas_finalizadas:
            if venda.funcionario == funcionario:
                vendas_do_funcionario.append(venda)
            
        return vendas_do_funcionario

    def __str__(self):
        return f"histórico contendo {len(self.__vendas_finalizadas)} vendas registradas."