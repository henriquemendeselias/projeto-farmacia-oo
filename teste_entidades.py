from farmacia.entidades.pessoa import Funcionario, Cliente
from farmacia.entidades.produto import Medicamento, Perfumaria, Lote
from datetime import date

print("Testando a criação das pessoas")
funcionario = Funcionario("Funcionario", "111.111.111-11", "F001")
cliente = Cliente("Cliente", "000.000.000-00", 1)
print(50*'=')
print(funcionario)
print(cliente)
print(50*'=')

print("Testando a criação de produtos")
medicamento = Medicamento("DIP01", "Dipirona", 9.99, False)
perfumaria = Perfumaria("shm01", "Shampoo", 11.99, "300ml" )

print(50*'=')
print(medicamento)
print(perfumaria)
print(50*'=')

print("Testando a criação de um Lote")
lote1 = Lote("L001", 45, date(2027, 4, 30))
print(50*'=')
print(lote1)
