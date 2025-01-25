
import MySQLdb
from PyQt5 import uic, QtWidgets

# conectando ao banco de dados
conexao = MySQLdb.connect(
    host='127.0.0.1',
    user='Eder',
    passwd='124751',
    db='cadastro_produtos',
    port= 3306

)

# variavel global para comunicação com o BD
var_global = 0


# função para deletar registros:
def excluir():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
    valor_Id = leitura_banco[remover] [0]
    cursor.execute('DELETE FROM produtos\
                    WHERE id=' +str(valor_Id))
    
    conexao.commit() 
    

# 2º criar função para identificar a linha ativa que será editada
# ou deletada:
def editar():
    global var_global
    # busca linha ativa
    dados = lista.tableWidget.currentRow()
    # leitura completa do BD:
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
   
    valor_Id = leitura_banco [dados][0]  # verifica qual id ativo ou selecionado
    # buscar na tabela toda pelo id selecionado:
    cursor.execute('SELECT * FROM produtos \
                     WHERE id = ' + str(valor_Id))
    # fazendo a busca pelo id na linha e coluna:
    leitura_banco = cursor.fetchall()

    # abria a tela editar
    editar.show() 
    var_global = valor_Id

    # itens da tela editar cadastro e suas posições-'[]'
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarProduto.setText(str(leitura_banco[0][1]))
    editar.txtAlterarPreco.setText(str(leitura_banco[0][2]))
    editar.txtAlterarEstoque.setText(str(leitura_banco[0][3]))


# função para salvar dados
def salvar_dados():
    global var_global

    # passando as novas informações ao BD:
    id = editar.txtAlterarId.text()
    produto = editar.txtAlterarProduto.text()
    preco = editar.txtAlterarPreco.text()
    estoque = editar.txtAlterarEstoque.text()

    cursor= conexao.cursor()
    cursor.execute("UPDATE produtos SET id ='{}', produto = '{}', preco = '{}', estoque = '{}'\
         WHERE id = {}". format(id, produto, preco, estoque, var_global))

    editar.close()
    lista.close()
    formularios.show()
 
    # verifica os dados antes de enviar ao BD
    conexao.commit() 



# função para acessar a tela de relatório
def lista():
    lista.show()  # abre a lista

    # fazendo a leitura do banco com consulta de um select
    cursor = conexao.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    # fetchall: fazendo a leitura e separa linhas e colunas 
    leitura_banco = cursor.fetchall()

    # fazendo a contagem de linhas da tela de lista, com fetchall
    lista.tableWidget.setRowCount(len(leitura_banco))
    # fazendo a leitura das 4 colunas da tela lista com len()
    lista.tableWidget.setColumnCount(4)

    # fazendo as buscas da informações nas linhas e colunas
    for linha in range(0, len(leitura_banco)):
        # contagem das 4 colunas
        for coluna in range(0, 4):
            # armazenando as informações do for
            lista.tableWidget.setItem(
                linha, coluna, QtWidgets.QTableWidgetItem(str(leitura_banco[linha][coluna])))


def inserir():
    # capturar dados:
    produto = formularios.txtProduto.text()
    preco = formularios.txtPreco.text()
    estoque = formularios.txtEstoque.text()

    # metodo de escrita no banco:
    cursor = conexao.cursor()  # escreve no BD
    # inserir dados no BD:
    comando_SQL = "INSERT INTO produtos(produto, preco, estoque)\
                   VALUES(%s,%s,%s)"

    # organiza as informações:
    dados = (str(produto), str(preco), str(estoque))

    # executar o envio dos dados:
    cursor.execute(comando_SQL, dados)

    # commint verifica se os dados de envio estão
    # corretos antes de enviar para o banco de dados
    conexao.commit()

    # limpando caixa de texto:
    formularios.txtProduto.setText('')
    formularios.txtPreco.setText('')
    formularios.txtEstoque.setText('')

    # mensagem de confirmação de dados inseridos
    formularios.lblConfirmacao.setText('* DADOS INSERIDOS COM SUCESSO!!')


app = QtWidgets.QApplication([])
# abrindo o formulário
formularios = uic.loadUi('formularios.ui')
# botao de inserir dados
formularios.btnCadastrar.clicked.connect(inserir)

# informando botão de Relatório
formularios.btnRelatorio.clicked.connect(lista)
# abrindo a lista de relatório
lista = uic.loadUi('lista.ui')
lista.btnAlterarRegistro.clicked.connect(editar)
lista.btnDeletar.clicked.connect(excluir)

# realizando o update: alterar ou deletar, item da tabela:
# 1º informar que a tela alterar regostro existe:
editar = uic.loadUi('editar.ui')
# informar botão Confirmar
editar.btnConfirmar.clicked.connect(salvar_dados)

formularios.show()
app.exec()
