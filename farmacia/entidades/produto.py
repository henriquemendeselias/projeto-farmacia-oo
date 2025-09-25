from abc import ABC, abstractmethod
from datetime import date

class Produto(ABC):
    def __init__(self, codigo: str, nome: str, preco: float):
        self._codigo = codigo
        self._nome = nome
        self._preco = preco

    @abstractmethod
    def __str__(self) -> str:
        pass

class Medicamento(Produto):
    def __init__(self, codigo: str, nome: str, preco: float, receita_obrigatoria: bool):
        super().__init__(codigo, nome, preco)
        self.__receita_obrigatoria = receita_obrigatoria
    
    def __str__(self) -> str:
        info_base = f"Medicamento: {self._nome} | Preço: R${self._preco:.2f}"
        info_especifica = f"Exige Receita: {'Sim' if self.__receita_obrigatoria else 'Não'}"
        return f"{info_base} | {info_especifica}"
    
class Perfumaria(Produto):
    def __init__(self, codigo: str, nome: str, preco: float, volume: str):
        super().__init__(codigo, nome, preco)
        self.__volume = volume
    
    def __str__(self) -> str:
        info_base = f"Perfumaria: {self._nome} | Preço: R${self._preco:.2f}"
        info_especifica = f"Volume: {self.__volume}"
        return f"{info_base} | {info_especifica}"

class Lote: 
    def __init__(self, codigo_lote: str, quantidade: int, data_validade: date):
        self.__codigo_lote = codigo_lote
        self.__quantidade = quantidade
        self.__data_validade = data_validade

    def __str__(self) -> str:
        data_formatada = self.__data_validade.strftime('%d/%m/%Y')
        return f"Lote: {self.__codigo_lote} | Qtd: {self.__quantidade} | Validade: {data_formatada}"