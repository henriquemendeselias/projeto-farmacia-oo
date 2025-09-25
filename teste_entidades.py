from farmacia.entidades.pessoa import Funcionario, Cliente
from farmacia.entidades.produto import Medicamento, Perfumaria, Lote
from datetime import date

print("Testando a criação das pessoas")
funcionario = Funcionario("Funcionario", "111.111.111-11", "F001")
cliente = Cliente("Cliente", "000.000.000-00", 1)

print(funcionario)
print(cliente)

print("Testando a criação de produtos")
medicamento = Medicamento("DIP01", "Dipirona", 9.99, False)
perfumaria = Perfumaria("shm01", "Shampoo", 11.99, "300ml" )

print(medicamento)
print(perfumaria)

print("Testando a criação de um Lote")
data_validade_lote = date(2027, 4, 30)
lote1 = Lote("L001", 45, data_validade_lote)
print(lote1)
