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
def page2br():
    return render_template("NDRECbr.html")

def get_arquivobr():   
    return send_file('/domino/datasets/local/MD/doecasmcompleta.csv')    

def get_arquivo2br():    
    return send_file('/domino/datasets/local/salvar_arquivos/arquivo_para_md.xlsx')     

def get_arquivo3br():    
    return send_file('/domino/datasets/local/MD/exnotedescrip1.xlsx')    

def get_arquivo4br():    
    return send_file('/domino/datasets/local/MD/dadosparafiltro.xlsx')    

def get_arquivo5br():
    
    return send_file('/domino/datasets/local/MD/exD_N_REC.xlsx')

def get_arquivo6br():
    
    return send_file('/domino/datasets/local/MD/exrm_valores.xlsx')

def get_arquivo7br():    
    return send_file('/domino/datasets/local/MD/corpmonitor.xlsx')
  
#bloco que cria um arquivo temporario para o arquivo recebido do usuario. 
def post_arquivobr():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_RECtmpbr.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/D_N_REC.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/D_N_REC.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/D_N_RECtmpbr.csv',index = False)
    os.remove('/domino/datasets/local/salvar_arquivos/D_N_REC.xlsx')   
    return render_template("NDRECs.html")

def post_arquivobr1():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')
    return render_template("rm_valores.html")

def post_arquivobr2():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.xlsx') 
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.csv')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempbr.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/tempbr.csv',index = False)
    return render_template("dadosparafiltro.html")

def post_arquivobr3():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')      
    return render_template("corpmonitor.html")

def post_arquivobr4():
    arquivo = request.files.get("meuArquivo")
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.csv')
    os.remove('/domino/datasets/local/salvar_arquivos/tempbr.xlsx') 
    arquivo.save('/domino/datasets/local/salvar_arquivos/tempbr.xlsx') 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempbr.xlsx')
    descricao1t.to_csv('/domino/datasets/local/salvar_arquivos/tempbr.csv',index = False)
        
    return render_template("notedescrip1.html")





