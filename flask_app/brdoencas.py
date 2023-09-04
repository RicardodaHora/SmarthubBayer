from flask_app import templates
from flask_app import static
import pandas as pd
from flask import Flask, render_template
from flask.globals import request
import time
daaltera=time.ctime()
tabela1 = pd.read_csv('/domino/datasets/local/MD/doecasmcompleta.csv')
tabela1a =tabela1
tabela1=tabela1.loc[tabela1['Status'] != "old"]
cb1a =   ''
cb2b =  ''
cb3c =  ''
cb4d =  ''
desabilita3 = ''
hab=0
hab2=0
def homepagebr():
    daaltera=time.ctime()
    nome=request.headers.get("domino-username")
    tabela1 = pd.read_csv('/domino/datasets/local/MD/doecasmcompleta.csv')
    tabela1=tabela1.loc[tabela1['Status'] != "old"]
    tabela1=tabela1.sort_values(by=['Product'])
    doencas=tabela1.columns.values.tolist()
    del doencas [-6:]
    del doencas [0:2]  
    if request.method == 'POST':
        
       global cb1a  
       global cb2b 
       global cb3c  
       global cb4d      
                    
       if hab!= 1 or len(cb1a) < 1 or len(cb2b) < 1 or len(cb3c) < 1 or len(cb4d) < 1 :
        cb1 = request.form['cb1']
        cb2 = request.form['cb2']
        cb3 = request.form['cb3']
        cb4 = request.form['cb4']
        cb1a = cb1        
        cb2b = cb2        
        cb3c = cb3        
        cb4d = cb4             
        desabilita3 = '' 
        desabilita2 = 'disabled'
        desabilita1 = 'disabled'
        produto, bio_tecnologia, pipeline, marca = atualiza(filtra(cb1,cb2,cb3,cb4,tabela1))
        cb5, cb6, cb7, cb8, cb9, cb10, cb11, cb12, cb13, cb14, cb15,nota,desabilita4,ativo = carrega_valor(filtra(cb1,cb2,cb3,cb4,tabela1))
        global valor1t 
        global ativo1
        ativo1 = ativo
        valor1t = tabela1.index.values[tabela1['Product']==cb1a]
        global tabelas1
        tabelas1=filtra(cb1,cb2,cb3,cb4,tabela1)
       else:
        cb1=cb1a
        cb2=cb2b
        cb3=cb3c
        cb4=cb4d
        desabilita4 = 'disabled'
        desabilita3 = 'disabled'
        desabilita2 =''
        desabilita1 =''
        produto, bio_tecnologia, pipeline, marca = atualiza(filtra(cb1,cb2,cb3,cb4,tabela1))
        
        cb5 = request.form['cb5']
        cb6 = request.form['cb6']
        cb7 = request.form['cb7']
        cb8 = request.form['cb8']
        cb9 = request.form['cb9']
        cb10 = request.form['cb10']
        cb11 = request.form['cb11']
        cb12 = request.form['cb12']
        cb13 = request.form['cb13']
        cb14 = request.form['cb14']
        cb15 = request.form['cb15']
        nota = request.form['story'] + nome + daaltera 
        global cb5a
        cb5a = cb5
        global cb6a
        cb6a = cb6
        global cb7a
        cb7a = cb7
        global cb8a
        cb8a = cb8
        global cb9a
        cb9a = cb9
        global cb10a
        cb10a = cb10
        global cb11a
        cb11a = cb11
        global cb12a
        cb12a = cb12
        global cb13a
        cb13a = cb13
        global cb14a
        cb14a = cb14
        global cb15a
        cb15a = cb15
        global tab1
        tab1 = tabela1 
        tabelas1 = tabelas
        valor1t = tabelas.index.values[tabelas['Product']==cb1a]
        tabelas1.loc[valor1t] = [cb1a,cb2b,cb5a,cb6a,cb7a,cb8a,cb9a,cb10a,cb11a,cb12a,cb13a,cb14a,cb15a,cb3c,cb4d,nota,"",daaltera,ativo1]

    else:
        cb2 = ''
        cb1 = ''
        cb3 = ''
        cb4 = ''
        cb1a = cb1        
        cb2b = cb2        
        cb3c = cb3        
        cb4d = cb4
        
        produto, bio_tecnologia, pipeline, marca = atualiza(tabela1)
        cb5, cb6, cb7, cb8, cb9, cb10, cb11, cb12, cb13, cb14, cb15,nota,desabilita4,ativo = carrega_valor(tabela1)
        desabilita2 = 'disabled'
        desabilita1 = 'disabled'
        desabilita3 = ''
        
    return render_template("doencasmilho.html",produto1=produto,bio_tecnologia=bio_tecnologia,pipeline=pipeline,timea=daaltera,
                           marca=marca, cb2=cb2,cb1=cb1,cb3=cb3,cb4=cb4, cb5=cb5,cb6=cb6,cb7=cb7,cb8=cb8,cb9=cb9,
                           cb10=cb10,cb11=cb11, cb12=cb12,cb13=cb13,cb14=cb14,cb15=cb15,desabilita1=desabilita1,
                           desabilita2=desabilita2,desabilita3=desabilita3,desabilita4=desabilita4,nota=nota,doencas=doencas, nome=nome)

def editarbr():
    daaltera=time.ctime()
    nome=request.headers.get("domino-username")
    tabela1 = pd.read_csv('/domino/datasets/local/MD/doecasmcompleta.csv')
    tabela1=tabela1.loc[tabela1['Status'] != "old"]
    tabela1=tabela1.sort_values(by=['Product'])
    doencas=tabela1.columns.values.tolist()
    del doencas [-6:]
    del doencas [0:2]  
    if request.method == 'POST':
        desabilita3 = 'disabled'
        desabilita2 =''
        cb1=cb1a
        cb2=cb2b
        cb3=cb3c
        cb4=cb4d
        produto, bio_tecnologia, pipeline, marca = atualiza(filtra(cb1, cb2, cb3, cb4, tabela1))
        cb5, cb6, cb7, cb8, cb9, cb10, cb11, cb12, cb13, cb14, cb15,nota, desabilita1, ativo = carrega_valor(filtra(cb1, cb2, cb3, cb4, tabela1))
        global tabelas
        tabelas=filtra(cb1a, cb2b, cb3c, cb4d, tabela1)
        desabilita4 = 'disabled'
        global hab
        hab = 1
    else:
        desabilita3 = ''
        desabilita2 = 'disabled'
        desabilita4 = ''
        hab = 0 
    return render_template("doencasmilho.html",produto1=produto,bio_tecnologia=bio_tecnologia,pipeline=pipeline,timea=daaltera,
                           marca=marca, cb2=cb2,cb1=cb1,cb3=cb3,cb4=cb4, cb5=cb5,cb6=cb6,cb7=cb7,cb8=cb8,cb9=cb9,
                           cb10=cb10,cb11=cb11, cb12=cb12,cb13=cb13,cb14=cb14,cb15=cb15,desabilita1=desabilita1,
                           desabilita2=desabilita2,desabilita3=desabilita3, desabilita4=desabilita4,hab=hab,doencas=doencas, nome=nome)

def salvarbr():
    tabela1 = pd.read_csv('/domino/datasets/local/MD/doecasmcompleta.csv')
    tab1=tabela1
    #salva o valor atual da tablela para backup
    tabelassalvar = tab1.loc[valor1t]
    tabela3=tab1.drop(index=valor1t)
    tabelassalvar['Status']= 'old' 
    #salva o valor que foi alterado para a tabela atual    
    tabela3=pd.concat([tabela3, tabelas1])   
    tabela1=tabela3
    doecasmcompleta2=pd.concat([tabela3, tabelassalvar])
    doecasmcompleta2=doecasmcompleta2.sort_values(by=['Product']) 
    global hab
    hab=0
    doecasmcompleta2.to_csv('/domino/datasets/local/MD/doecasmcompleta.csv',index = False)
           
    return render_template("salvo.html")  

def atualiza(tabela):
    tabela1=tabela
    tabela1=tabela1.loc[tabela1['Status'] != "old"]
    produto = tabela1['Product'].unique()
    bio_tecnologia = tabela1['Biotecnologias_disponiveis'].unique()
    pipeline = tabela1['Pipeline'].unique()
    marca = tabela1['Marca'].unique()
    return produto, bio_tecnologia, pipeline, marca
produto, bio_tecnologia, pipeline, marca = atualiza(tabela1) 

def carrega_valor(tab4):
    a = len(tab4.index)
    if a == 1 and cb1a != '' and cb2b != '' and cb3c != '' and cb4d != '':
        cb5 = tab4["Turcicum"].values[0]
        cb6 = tab4["Ferrugem_Polysora"].values[0]
        cb7 = tab4["Cercospora"].values[0]
        cb8 = tab4["Mancha_Branca"].values[0]
        cb9 = tab4["Complexo_Enfezamento"].values[0]
        cb10 = tab4["Estria_Bacteriana"].values[0]
        cb11 = tab4["Diplodia_Espiga"].values[0]
        cb12 = tab4["Giberela_Espiga"].values[0]
        cb13 = tab4["Fusarium_Colmo"].values[0]
        cb14 = tab4["Antracnose_Colmo"].values[0]
        cb15 = tab4["Bipolaris"].values[0]
        nota = tab4['notas_de_mudancas'].values[0]
        ativo = tab4['situacao'].values[0]    
        desabilita4 = ''
    else:
        cb5 = ''
        cb6 = ''
        cb7 = ''
        cb8 = ''
        cb9 = ''
        cb10 = ''
        cb11 = ''
        cb12 = ''
        cb13 = ''
        cb14 = ''
        cb15 = ''
        nota = 'Coloque a informação da mudança aqui. '
        ativo =''
        desabilita4 = 'disabled'
    return cb5, cb6, cb7, cb8, cb9, cb10, cb11, cb12, cb13, cb14, cb15,nota,desabilita4,ativo

def filtra(p,b,pi,m,tabela3):
    tabela2=tabela3
    if p != '':
        tabela2=tabela2[tabela2['Product']== p]
    else:
        tabela2=tabela2
    if b != '':
        tabela2=tabela2[tabela2['Biotecnologias_disponiveis']== b]
    else:
        tabela2=tabela2
    if pi != '':
        tabela2 = tabela2[tabela2['Pipeline'] == pi]
    else:
        tabela2 = tabela2
    if m != '':
        tabela2 = tabela2[tabela2['Marca'] == m]
    else:
        tabela2 = tabela2
    return tabela2                        