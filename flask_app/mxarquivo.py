from flask_app import templates
from flask_app import static
import pandas as pd
import os
from flask import Flask, render_template, send_file
from flask.globals import request
import time
daaltera=time.ctime()
DIRETORIO= "/domino/datasets/local/MD/"
# bloco de envio de aquivo para o usuario.
def page2mx():
    return render_template("NDRECmx.html")

def get_arquivomx():
   
    return send_file('/domino/datasets/local/MD/doencasdemilhomx.csv')    

def get_arquivo2mx():
    
    return send_file('/domino/datasets/local/salvar_arquivos/arquivo_para_mdmx.xlsx')     

def get_arquivo3mx():
    
    return send_file('/domino/datasets/local/MD/descriptmx1.xlsx')    

def get_arquivo4mx():
    
    return send_file('/domino/datasets/local/MD/filtroparamexico.xlsx')    

def get_arquivo5mx():
    
    return send_file('/domino/datasets/local/MD/exD_N_RECmx.xlsx')

def get_arquivo6mx():
    
    return send_file('/domino/datasets/local/MD/fenologia_mx.xlsx')  

#bloco que cria um arquivo temporario para o arquivo recebido do usuario.  

def post_arquivomx():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_RECtmpmx.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/D_N_RECmx.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/D_N_RECmx.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/D_N_RECtmpmx.csv',index = False)
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_RECmx.xlsx')   
    return render_template("NDRECsmx.html")

def post_arquivo1mx():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    return render_template("rm_valoresmx.html")

def post_arquivo2mx():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.xlsx') 
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempmx.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv',index = False)
    return render_template("dadosparafiltromx.html")

def post_arquivo3mx():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')      
    return render_template("corpmonitormx.html")

def post_arquivo4mx():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    os.remove('/domino/datasets/local/salvar_arquivos/tempmx.xlsx') 
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempmx.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv',index = False)
        
    return render_template("notedescrip1mx.html")
