from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str):
        self._nome = nome
        self._cpf = cpf

    def __str__(self) -> str:
        return f"Nome: {self._nome}, CPF: {self._cpf}"
    
class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, matricula: str):
        super().__init__(nome, cpf)
        self.__matricula = matricula
    
    def __str__(self) -> str: 
        info_base = super().__str__()
        return f"Funcionario | {info_base}, Matricula: {self.__matricula}"
    
class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, id_cliente: int):
        super().__init__(nome, cpf)
        self.__id_cliente = id_cliente

    def __str__(self) -> str:
        info_base = super().__str__()
        return f"Cliente | {info_base}, ID: {self.__id_cliente}"