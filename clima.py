import requests
import json
import streamlit as st
#streamlit run your_script.py [-- script args]    # para pegar o hostlocal
#from db_clima import *
import datetime

# parte de database :
import sqlite3
banco = sqlite3.connect("data.db")
db = banco.cursor()

def create_table():
    db.execute('CREATE TABLE IF NOT EXISTS tabelaclima(cidade TEXT, temperatura TEXT, dia TEXT)')

def inserir_db(cidade,temperatura,dia):
    db.execute("INSERT INTO tabelaclima VALUES (?,?,?)",(cidade,temperatura,dia))
    banco.commit()
    db.close()
    banco.close()

def view_db():
    db.execute("SELECT * FROM tabelaclima")
    data =  db.fetchall()
    return data

def get_cidade(cidade):
    db.execute(f"SELECT * FROM tabelaclima WHERE cidade='{cidade}'")
    data = db.fetchall()
    return data

def delete_db(cidade):
    db.execute(f"DELETE FROM tabelaclima WHERE cidade='{cidade}'")
    banco.commit()

def deleteTudo_db():
    db.execute(f"DELETE FROM tabelaclima")
    banco.commit()

# fim parte database

st.sidebar.header('Escolha uma opção')
paginaselecionada = st.sidebar.selectbox('Selecione:', ['Pesquisar', 'Consultar'])


if paginaselecionada == 'Pesquisar':
    st.title('O Clima em Python')
    st.header('Pesquisa Online')
    cidade = st.text_input("Escolha a cidade").upper().strip()
    st.button('mostrar')
    if cidade != "":
        requisicao = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cidade+'&appid=d155d52bf0cc67795a73744ebde23897')
        tempo = json.loads(requisicao.text)
        temperatura = (float(tempo['main']['temp']) - 273.15)
        st.write('Cidade Escolhida : ', cidade)
        st.write('Condicao do tempo : ', tempo['weather'][0]['main'])
        st.write('Resumo : ', tempo['weather'][0]['description'])
        st.write('Temperatura : ', round(temperatura, 2))
        st.write('Umidade Relativa : ', tempo['main']['humidity'])
        data = datetime.datetime.now()
        st.write('Data : ', str(data.day)+"/"+str(data.month)+"/"+str(data.year))
        st.write('Dados fornecidos por openweathermap.org')
        gravar = st.button('gravar')

        if gravar:
            create_table()
            st.write('enviando comando ao banco de dados')
            inserir_db(str(cidade), str(temperatura), str(data))
            st.success('gravado com sucesso')


elif paginaselecionada == 'Consultar':
    st.title('O Clima em Python')
    st.header('Consulta DataBase')
    cidade = st.text_input("Escolha a cidade").upper().strip()
    consultar = st.button('consultar')
    deletar = st.button('deletar tudo')
    if consultar:
        st.write('consultando o banco de dados')
        #st.write(view_db())
        st.write(get_cidade(cidade))
        st.success('retorno da consulta efetuado com sucesso')
    if deletar:
        deleteTudo_db()
        st.success('todos os dados foram deletados com sucesso')
