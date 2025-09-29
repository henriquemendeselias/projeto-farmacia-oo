from farmacia.entidades.produto import Medicamento, Perfumaria, Lote
from farmacia.servicos.estoque import Estoque
from datetime import date
print(50 *'=')

estoque = Estoque()
dipirona = Medicamento("dip", "dipirona 1g", 9.99, False)
shampoo = Perfumaria("sh01", "shampoo", 15.99, "300ml")
neosaldina = Medicamento("neo", "neosaldina", 4.99, False)

print("teste de adicionar lotes diferentes")
estoque.adicionar_lote(dipirona, "dip_lote1", 30, date(2027, 5, 20))
estoque.adicionar_lote(dipirona, "dip_lote2", 20, date(2028, 8, 10))
estoque.adicionar_lote(neosaldina, "neolote1", 20, date(2025, 11, 13))
estoque.adicionar_lote(neosaldina, "neolote2", 30, date(2026, 1, 1))

print(estoque)

print(50 *'=')

print("teste de dar baixas no estoque")
estoque.dar_baixa_por_venda(dipirona, 2)
print(estoque)

print(50 *'=')

print("teste para produto inexsitente")
estoque.dar_baixa_por_venda(shampoo, 1)

print(50 *'=')

print("teste para estoque insuficiente")
sucesso = estoque.dar_baixa_por_venda(dipirona, 49)
print(F"{'Sucesso' if sucesso else 'falha'}")
print(estoque)

print(50 *'=')
print("teste para verificar que produtos com validade mais perto estão sendo baixados primeiro")
estoque.dar_baixa_por_venda(neosaldina, 25)
i = estoque.consultar_lote_produto(neosaldina)
for e in i:
    print(e)

print(50 *'=')

print("teste para métodos de listagem")
nivea = Perfumaria("nv001", "nivea", 15.99, "450ml")
estoque.adicionar_lote(nivea, "nvlote1", 2, date(2025, 10, 15))
estoque.dar_baixa_por_venda(dipirona, 47)

print(20 *'-' + "produtos em falta" + 20*'-')
p = estoque.listar_produtos_baixo_estoque(5)
for a in p:
    print(a)

print(20 *'-' + "produtos perto de vencer" + 20*'-')
h = estoque.listar_produtos_proximo_vencimento(30)
for i in h:
    print(i)