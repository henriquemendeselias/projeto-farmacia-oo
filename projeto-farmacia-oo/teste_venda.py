from farmacia.entidades.pessoa import Funcionario, Cliente
from farmacia.entidades.produto import Medicamento, Perfumaria, Lote
from farmacia.servicos.estoque import Estoque
from farmacia.servicos.venda import ItemVenda, Venda, Orcamento, HistoricoVendas
from datetime import date

estoque = Estoque()
historico = HistoricoVendas()
func_ana = Funcionario("Ana", "111.111.111-11")
cliente_henrique = Cliente("Henrique","000.000.000-00")
dipirona = Medicamento("dip001", "Dipirona", 5.99, False)
dorflex = Medicamento("dflx001","Dorflex", 7.99, False)
shampoo = Perfumaria("sh001","Shampoo",10.99,"300ML")
fio_dental = Perfumaria("fd001","Fio Dental",6.99,"100M")

print('adicionando lotes para ter oque vender')
estoque.adicionar_lote(dipirona,"diplote001",100,date(2027,5,15))
estoque.adicionar_lote(shampoo, "shlote001",20,date(2029,11,29))
estoque.adicionar_lote(dorflex, "dflxlote001", 30, date(2026,2,4))
estoque.adicionar_lote(fio_dental, "fdlote001", 30, date(2027,3,4))
print(50*'=')
print(estoque)

print(15*'='+"FLUXO PRINCIPAL"+15*'=')
print('criando venda 1')
venda1 = Venda(func_ana, cliente_henrique)
venda1.adicionar_item(dipirona, 1)
venda1.adicionar_item(shampoo, 2)
print(venda1)

venda1.aplicar_desconto(10) #teste de desconto

print("pausando a venda para testar se é possível processar pagamento(deve falhar)")
venda1.pausar_venda()
venda1.processar_pagamento("Dinheiro", 100.0)
print("retomando")
venda1.retomar_venda()
print(50*'=')
pagamento_ok = venda1.processar_pagamento("Dinheiro", 100.0)
print(50*'=')

print('finalizando a venda') 
if pagamento_ok: #necessita que processar_pagamento retorne True
    venda1.finalizar_venda(estoque, historico)
else:
    print("pagamento não aprovado")

print(50*'=')

print("avaliando as mudanças de estoque, historico e status da venda após a venda")
print(estoque)
print(50*'=')
print(historico)
print(50*'=')
print(venda1.status)

print(15*'='+"FLUXO ALTERNATIVO"+15*'=')
venda2 = Venda(func_ana, cliente_henrique)
venda2.adicionar_item(dorflex, 5)
venda2.adicionar_item(fio_dental, 2)
pagamento_ok_2 = venda2.processar_pagamento("Débito",53.95)
print(50*'=')
if pagamento_ok_2:
    venda2.finalizar_venda(estoque, historico)
else: 
    print("pagamento não aprovado")
print(50*'=')

print(estoque) #nada de diferente até aqui
print(50*'=')
print("cancelando a venda após ser finalizada")
venda2.cancelar_venda(estoque)
print(50*'=')
print("avaliando mudanças pós cancelamento")
print(estoque)
print(50*'=')
print(historico) #o historico ainda guarda a venda, porém agora com o status de cancelada.
print(50*'=')
print(venda2.status)

print(15*'='+"ORÇAMENTO"+15*'=')
orcamento = Orcamento(func_ana, cliente_henrique)
orcamento.adicionar_item(dorflex, 3)
orcamento.adicionar_item(dipirona, 2)
print("criação de um orçamento")
print(orcamento)
nova_venda = orcamento.converter_em_venda()
print("transformar um orçamento em uma venda, sendo essa a venda de id 3")
print(nova_venda)
