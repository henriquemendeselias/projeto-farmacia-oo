from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str):
        self._nome = nome
        self._cpf = cpf

    def __str__(self) -> str:
        return f"Nome: {self._nome}, CPF: {self._cpf}"
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @nome.setter
    def nome(self, novo_nome: str):
        if novo_nome and novo_nome.strip():
            self._nome = novo_nome
        else:
            print("O nome não pode ser vazio.")

    @cpf.setter
    def cpf(self, novo_cpf: str):
        if novo_cpf and novo_cpf.strip():
            self._cpf = novo_cpf
        else:
            print("[ERRO] O CPF não pode ser vazio.")
    
class Funcionario(Pessoa):
    _contador_matricula = 0
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome, cpf)
        Funcionario._contador_matricula += 1
        self.__matricula = f"F{Funcionario._contador_matricula:03d}"
    
    def __str__(self) -> str: 
        info_base = super().__str__()
        return f"Funcionario | {info_base}, Matricula: {self.__matricula}"
    
    @property
    def matricula(self) -> str:
        return self.__matricula
    
class Cliente(Pessoa):
    _contador_id = 0
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome, cpf)
        Cliente._contador_id += 1
        self.__id_cliente = Cliente._contador_id

    def __str__(self) -> str:
        info_base = super().__str__()
        return f"Cliente | {info_base}, ID: {self.__id_cliente}"
    
    @property
    def id_cliente(self) -> int:
        return self.__id_cliente