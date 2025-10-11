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

    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def preco(self) -> float:
        return self._preco
    
    @nome.setter
    def nome(self, novo_nome: str):
        if novo_nome and novo_nome.strip():
            self._nome = novo_nome
        else:
            print("O nome não pode ser vazio.")

    @preco.setter
    def preco(self, novo_preco: float):
        if novo_preco > 0:
            self._preco = novo_preco
        else:
            print("O preço deve ser um valor positivo.")

class Medicamento(Produto):
    def __init__(self, codigo: str, nome: str, preco: float, receita_obrigatoria: bool):
        super().__init__(codigo, nome, preco)
        self.__receita_obrigatoria = receita_obrigatoria
    
    def __str__(self) -> str:
        info_base = f"Medicamento: {self._nome} | Preço: R${self._preco:.2f}"
        info_especifica = f"Exige Receita: {'Sim' if self.__receita_obrigatoria else 'Não'}"
        return f"{info_base} | {info_especifica}"
    
    @property
    def receita_obrigatoria(self) -> bool:
        return self.__receita_obrigatoria
    
    @property
    def codigo(self):
        return self._codigo
    
    @codigo.setter
    def codigo(self, novo_codigo: str, ):
        if novo_codigo and novo_codigo.strip():
            self._codigo = novo_codigo
        else:
            print("O nome não pode ser vazio.")

    
class Perfumaria(Produto):
    def __init__(self, codigo: str, nome: str, preco: float, volume: str):
        super().__init__(codigo, nome, preco)
        self.__volume = volume
    
    def __str__(self) -> str:
        info_base = f"Perfumaria: {self._nome} | Preço: R${self._preco:.2f}"
        info_especifica = f"Volume: {self.__volume}"
        return f"{info_base} | {info_especifica}"
    
    @property
    def volume(self) -> str:
        return self.__volume

class Lote: 
    def __init__(self, codigo_lote: str, quantidade: int, data_validade: date):
        self.__codigo_lote = codigo_lote
        self.__quantidade = quantidade
        self.__data_validade = data_validade

    def __str__(self) -> str:
        data_formatada = self.__data_validade.strftime('%d/%m/%Y')
        return f"Lote: {self.__codigo_lote} | Qtd: {self.__quantidade} | Validade: {data_formatada}"
    
    @property
    def codigo_lote(self) -> str:
        return self.__codigo_lote
    
    @property
    def quantidade(self) -> int:
        return self.__quantidade
    
    @property
    def data_validade(self) -> date:
        return self.__data_validade
    
    @quantidade.setter
    def quantidade(self, nova_quantidade: int):
        if nova_quantidade >=0:
            self.__quantidade = nova_quantidade
        else:
            self.__quantidade = 0