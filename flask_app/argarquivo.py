from flask_app import templates
from flask_app import static
import pandas as pd
import os
from flask import Flask, render_template, send_file
from flask.globals import request
import time
daaltera=time.ctime()
DIRETORIO= "/domino/datasets/local/MD/"
def page2arg():
    return render_template("NDRECarg.html")
# bloco de envio de aquivo para o usuario.
def get_arquivoarg():
   
    return send_file('/domino/datasets/local/MD/doencasdemilhoarg.csv')    

def get_arquivo2arg():
    
    return send_file('/domino/datasets/local/salvar_arquivos/arquivo_para_mdar.xlsx')     

def get_arquivo3arg():
    
    return send_file('/domino/datasets/local/MD/descriptar1.xlsx')    

def get_arquivo4arg():
    
    return send_file('/domino/datasets/local/MD/filtroparamdargentina.xlsx')    

def get_arquivo5arg():
    
    return send_file('/domino/datasets/local/MD/exD_N_RECar.xlsx')

def get_arquivo6arg():
    
    return send_file('/domino/datasets/local/MD/fenologia_arg.xlsx')    

#bloco que cria um arquivo temporario para o arquivo recebido do usuario.

def post_arquivoarg():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_RECtmparg.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/D_N_RECar.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/D_N_RECar.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/D_N_RECtmparg.csv',index = False)
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_RECar.xlsx')   
    return render_template("NDRECsarg.html")

def post_arquivo1arg():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/temparg.xlsx')
    return render_template("rm_valoresarg.html")

def post_arquivo2arg():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.xlsx') 
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/temparg.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/temparg.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/temparg.csv',index = False)
    return render_template("dadosparafiltroarg.html")

def post_arquivo3arg():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/temparg.xlsx')      
    return render_template("corpmonitorarg.html")

def post_arquivo4arg():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.csv')
    os.remove('/domino/datasets/local/salvar_arquivos/temparg.xlsx') 
    arquivo.save('/domino/datasets/local/salvar_arquivos/temparg.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/temparg.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/temparg.csv',index = False)
        
    return render_template("notedescrip1arg.html")
