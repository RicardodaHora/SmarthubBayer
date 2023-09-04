from flask_app import templates
from flask_app import static
import pandas as pd
from flask import Flask, render_template
from flask.globals import request
import time
daaltera=time.ctime()
tabela10 = pd.read_csv('/domino/datasets/local/MD/notedescripmx1.csv')
descricao = pd.read_csv('/domino/datasets/local/MD/descricaomx.csv')
tabela10a =tabela10
tabela10=tabela10.loc[tabela10['Status'] != "old"]
cb1a =   ''
cb2b =  ''
cb3c =  ''
cb4d =  ''
desabilita3 = ''
tabela12a = tabela10
valor1 =tabela10.columns
hab=0
hab2=0
def page1mx():
    daaltera=time.ctime()
    nome=request.headers.get("domino-username")
    tabela10 = pd.read_csv('/domino/datasets/local/MD/notedescripmx1.csv')
    tabela10=tabela10.sort_values(by=['Hybrid'])
    descricao = pd.read_csv('/domino/datasets/local/MD/descricaomx.csv')
    tabela10=tabela10.loc[tabela10['Status'] != "old"]
    if request.method == 'POST':
        global cb11a
       
        global cb13c
        if hab2!= 1 or len(cb11a) < 1 or len(cb13c) < 1 :
            cb1 = request.form['cb1']
            
            cb3 = request.form['cb3']          
            cb11a = cb1        
                  
            cb13c = cb3
            cb4 =''
            cb5=''
            dados= tabela10.columns
            rec1='Descreva aqui a nota ou recomendação.'
            rquer1=''
            info1='Coloque a informação da mudança aqui. '+ daaltera
            if len(cb11a) > 1 and len(cb13c) > 1 :
                global tabela12a
                tabela12a=filtra1(cb1,cb3,tabela10) 
                desabilita4 = ''      
            else:
                desabilita4 = 'disabled'
                tabela12a=tabela10
            produt1, pipeline1= atualiza1(filtra1(cb1,cb3,tabela10))
            hab = 0
            desabilita2 = 'disabled'
            desabilita1 = 'disabled'
            desabilita3 = ''
            global valor10t 
            valor10t = tabela10.index.values[tabela10['Hybrid']==cb11a]
            global tabelas10a
            tabelas10a=filtra1(cb1,cb3,tabela10)
        else:
            cb1=cb11a
            cb2=cb12b
            cb3=cb13c  
            produt1, pipeline1= atualiza1(filtra1(cb1,cb3,tabela10))
            cb4 = request.form['cb4'] 
            global cb4n
            cb4n=cb4
            cb5 = request.form['cb5']
            story1 = request.form['story1']
            rec1=cb5
            info1=''+ nome +' - '+ daaltera 
            rquer1='required'
            dados= tabela10.columns
            dados=dados[3:(len(dados)-2)]
            desabilita3 = 'disabled'
            desabilita2 =''
            desabilita1 =''    
            desabilita4 = 'disabled' 
            hab = 0 
            tabelas10 = tabelas10s
            valor10t = tabelas10.index.values[tabelas10['Hybrid']==cb11a]
            tabela10c=tabelas10.loc[valor10t]
            tabela10c = adicionaitem(cb4,story1,tabela10c, info1)                  
            tabelas10.loc[valor10t] = tabela10c 
            tabela12a=tabela10c
            
                    
    else:
        
      
        cb1 = ''
        cb3 = ''
        cb11a = cb1        
               
        cb13c = cb3
        cb4 = ''
        cb5 =''
        dados= tabela10.columns        
        dados=dados[5:len(dados)]
        produt1,  pipeline1= atualiza1(filtra1(cb1,cb3,tabela10))
        tabela12a=filtra1(cb1,cb3,tabela10)
        desabilita2 = 'disabled'
        desabilita1 = 'disabled'
        desabilita3 = ''
        desabilita4 = 'disabled'
        hab = 0
        rec1='Descreva aqui a nota ou recomendação.'
        rquer1=''
        info1='Coloque a informação da mudança aqui. '+ daaltera
     
    dados1=descricao['descricao']   
    
    return render_template("paginacornotemx.html",produt1=produt1,pipeline1=pipeline1,cb1=cb1,cb3=cb3,cb4=cb4,dados=dados,
                           hab=hab, dados1=dados1,desabilita1=desabilita1,desabilita2=desabilita2,desabilita3=desabilita3,desabilita4=desabilita4, cb5=cb5, rec1=rec1,info1=info1, cursor1="",rquer1=rquer1,nome=nome )

def page3mx():    
    a = len(tabela12a.index)
    if a == 1:
        valor1=tabela12a 
        valor1.columns = valor1.columns.str.lower().str.replace('_', ' ')
        valor1.head()
        valor1=valor1.dropna(axis=1)
        dados= valor1.columns 
        valor1=valor1.iloc[-1] 
              
    else:
        valor1="" 
        dados=""
        dados1=""
    
    return render_template("pagina_de_descricaomx.html",dados=dados, valor1=valor1)
def page4mx():        
    descricao1t=pd.read_csv('/domino/datasets/local/salvar_arquivos/D_N_RECtmpmx.csv')
    descricao2t =pd.read_csv('/domino/datasets/local/MD/DEREC_NREC2mx.csv')
    descricao2f=descricao1t.merge(descricao2t, how='left', suffixes=['', '_'], indicator=True)
    descricao2d=descricao2t.merge(descricao1t, how='left', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f['_merge']=descricao2f['_merge'].replace("left_only",":Novo")
    descricao2d=descricao2d[descricao2d['_merge']=='left_only']
    descricao2d['_merge']=descricao2d['_merge'].replace("left_only","Atual")
    table=pd.concat([descricao2f, descricao2d])
    
    return render_template("NDRECSAIDAmx.html",table=[table.to_html(classes='data', header="true")])

def page4amx(): 
    descricao2t =pd.read_csv('/domino/datasets/local/MD/DEREC_NREC2mx.csv')
    
    table=descricao2t[:100]
    
    return render_template("NDRECSAIDAmx.html",table=[table.to_html(classes='data', header="true")])


def page5mx():    
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    descricao2t =pd.read_excel('/domino/datasets/local/MD/fenologia_mx.xlsx')
    descricao2f=descricao1t.merge(descricao2t, how='left', suffixes=['', '_'], indicator=True)
    descricao2d=descricao2t.merge(descricao1t, how='left', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f['_merge']=descricao2f['_merge'].replace("left_only",":Novo")
    descricao2d=descricao2d[descricao2d['_merge']=='left_only']
    descricao2d['_merge']=descricao2d['_merge'].replace("left_only","Atual")
    table=pd.concat([descricao2f, descricao2d])    
    return render_template("rm_valoresmxs.html",table=[table.to_html(classes='data', header="true")])

def page6mx():    
    descricao1t=pd.read_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    descricao2t =pd.read_csv('/domino/datasets/local/MD/filtroparamexico.csv')
    descricao2f=descricao1t.merge(descricao2t, how='left', suffixes=['', '_'], indicator=True)
    descricao2d=descricao2t.merge(descricao1t, how='left', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f['_merge']=descricao2f['_merge'].replace("left_only",":Novo")
    descricao2d=descricao2d[descricao2d['_merge']=='left_only']
    descricao2d['_merge']=descricao2d['_merge'].replace("left_only","Atual")
    table=pd.concat([descricao2f, descricao2d])
    
    return render_template("filtromxs.html",table=[table.to_html(classes='data', header="true")])

def page7mx():    
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')
    descricao2t =pd.read_excel('/domino/datasets/local/MD/corpmonitormx.xlsx')
    descricao2f=descricao1t.merge(descricao2t, how='left', suffixes=['', '_'], indicator=True)
    descricao2d=descricao2t.merge(descricao1t, how='left', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f['_merge']=descricao2f['_merge'].replace("left_only",":Novo")
    descricao2d=descricao2d[descricao2d['_merge']=='left_only']
    descricao2d['_merge']=descricao2d['_merge'].replace("left_only","Atual")
    table=pd.concat([descricao2f, descricao2d]) 
    
    return render_template("corpmonitormxs.html",table=[table.to_html(classes='data', header="true")])

def page8mx():    
    descricao1t=pd.read_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    descricao2t =pd.read_csv('/domino/datasets/local/MD/notedescrip1mx.csv')
    descricao2f=descricao1t.merge(descricao2t, how='left', suffixes=['', '_'], indicator=True)
    descricao2d=descricao2t.merge(descricao1t, how='left', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f['_merge']=descricao2f['_merge'].replace("left_only",":Novo")
    descricao2d=descricao2d[descricao2d['_merge']=='left_only']
    descricao2d['_merge']=descricao2d['_merge'].replace("left_only","Atual")
    table=pd.concat([descricao2f, descricao2d])
    
    return render_template("cornnotemxs.html",table=[table.to_html(classes='data', header="true")])

def editar2mx():
    
    if request.method == 'POST':
        desabilita3 = 'disabled'        
        cb1=cb11a
        cb3=cb13c 
        cb4='' 
        cb5='' 
        dados= tabela10.columns
        dados=dados[3:(len(dados)-2)]
        desabilita3 = 'disabled'
        desabilita2 =''
        desabilita1 =''    
        desabilita4 = 'disabled' 
        rec1=''
        info1=''      
        global hab2
        hab2 = 1
        produt1,  pipeline1= atualiza1(filtra1(cb1,cb3,tabela10))
        global tabelas10s
        tabelas10s=filtra1(cb11a, cb13c, tabela10)
        cursor1='autofocus'
        rquer1='required'
    else:
        desabilita3 = ''
        desabilita2 = 'disabled'
        desabilita4 = ''
        hab2 = 0 
    dados1=descricao['descricao']      
    return render_template("paginacornotemx.html", produt1=produt1,pipeline1=pipeline1,cb1=cb1,cb3=cb3,cb4=cb4,dados=dados, hab2=hab2, dados1=dados1,desabilita1=desabilita1,
                           desabilita2=desabilita2,desabilita3=desabilita3,desabilita4=desabilita4,cb5=cb5, rec1=rec1,info1=info1,cursor1=cursor1,rquer1=rquer1 )

def salvar2mx():
    tabela10 = pd.read_csv('/domino/datasets/local/MD/notedescripmx1.csv')
    #salva o valor atual da tablela para backup
    tabela10ssalvar = tabela10.loc[valor10t]
    tabela10ssalvar['Status']= 'old'
    #salva o valor que foi alterado para a tabela atual
    tabela10.loc[valor10t] = tabelas10s
    notedescrip1=pd.concat([tabela10a, tabela10ssalvar]) 
    notedescrip1=notedescrip1.sort_values(by=['Hybrid'])
    hab2 = 0 
    notedescrip1.to_csv('/domino/datasets/local/MD/notedescripmx1.csv',index = False)           
    return render_template("salvo2mx.html")

def filtra1(p,pi,tabela13):
    tabela12=tabela13
    if p != '':
        tabela12=tabela12[tabela12['Hybrid']== p]
    else:
        tabela12=tabela12
    if pi != '':
        tabela12 = tabela12[tabela12['Pipeline'] == pi]
    else:
        tabela12 = tabela12
    
    return tabela12

def atualiza1(tabela10a):
    tabela12=tabela10a
    produt1 = tabela12['Hybrid'].unique()
    pipeline1 = tabela12['Pipeline'].unique()   
    return produt1,  pipeline1
produt1, pipeline1 = atualiza1(tabela10)

def adicionaitem(cb4,story1, tabela10c, info1):
    if len(cb4) > 1:
        if len(story1) > 1:
                tabela10c[cb4] = story1 
                tabela10c['update']=info1
                print(story1)             
                           
    return  tabela10c 

def gestaoprodutosmx():       
    nome=request.headers.get("domino-username")
    cb1=''
    cb2=''
    cb3=''
    cb4=''
    cb5=''
    situacao=''
    desabilita1='' 
    desabilita2='disabled'
    desabilita4='disabled'
    
    return render_template("arquivogestaomx.html",cb2=cb2,cb1=cb1,cb3=cb3,cb4=cb4,cb5=cb5,nome=nome,produto1=" ",bio_tecnologia="",pipeline="",marca=" ",desabilita1=desabilita1,situacao=situacao,
                           desabilita2=desabilita2,desabilita4=desabilita4 )
def salvar1mx():
    datade=daaltera.replace(':','_') 
    datade=datade.replace(' ','_')
    nome=request.headers.get("domino-username")    
    descricao1t=pd.read_csv('/domino/datasets/local/salvar_arquivos/D_N_RECtmpmx.csv')
    descricao1t.to_excel('/domino/datasets/local/MD/exD_N_RECmx.xlsx', index = False)
    descricao2t =pd.read_csv('/domino/datasets/local/MD/DEREC_NREC2mx.csv')
    descricao2t.to_csv('/domino/datasets/local/backup_console/DEREC_NREC2mx'+ nome + datade +'.csv',index = False)
    descricao1t.to_csv('/domino/datasets/local/MD/DEREC_NREC2mx.csv',index = False)
    return render_template("salva1mx.html")

def salvar4mx():
    datade=daaltera.replace(':','_') 
    datade=datade.replace(' ','_')
    nome=request.headers.get("domino-username") 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')    
    descricao2t =pd.read_excel('/domino/datasets/local/MD/fenologia_mx.xlsx') 
    descricao1t.to_excel('/domino/datasets/local/MD/fenologia_mx.xlsx', index = False)
    descricao1t.to_excel('/domino/datasets/local/MD/exfenologia_mx.xlsx', index = False)    
    descricao2t.to_excel('/domino/datasets/local/backup_console/fenologia_mx'+ nome + datade +'.xlsx',index = False)
    
    return render_template("salvo3mx.html")

def salvar5mx():
    datade=daaltera.replace(':','_') 
    datade=datade.replace(' ','_')
    nome=request.headers.get("domino-username")    
    descricao1dt=pd.read_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    descricao1dt.to_excel('/domino/datasets/local/MD/filtroparamexico.xlsx', index = False)
    descricaod2t =pd.read_csv('/domino/datasets/local/MD/filtroparamexico.csv')
    descricaod2t.to_csv('/domino/datasets/local/backup_console/filtroparamexico'+ nome + datade +'.csv',index = False)
    descricao1dt.to_csv('/domino/datasets/local/MD/filtroparamexico.csv',index = False)
    descricaot = descricao1dt
    descricao1n=pd.read_csv('/domino/datasets/local/MD/notedescripmx1.csv')
    descricao1t =pd.read_csv('/domino/datasets/local/MD/doencasdemilhomx.csv')
    descricaot=descricaot[['Product','Pipeline','Marca','situacao']]
    descricaon=descricaot[['Product','Pipeline','situacao']]
    descricaon=descricaon.rename(columns={'Product':'Hybrid'})    
    descricao2n=descricaon
    descricao2t=descricaot
    descricao1nold=descricao1n[descricao1n['Status']=='old']
    descricao1n=descricao1n[descricao1n['Status']!='old']
    descricao1nf=descricao1n
    descricao1old=descricao1t[descricao1t['Status']=='old']
    descricao1t=descricao1t[descricao1t['Status']!='old']
    descricao1f=descricao1t
    #Atualiza plahnilha de doenças
    descricao1t=descricao1t[['Product','Pipeline','Marca']]
    descricao2t=descricao2t[['Product','Pipeline','Marca']]
    descricao2f=descricao1t.merge(descricao2t, how='outer', suffixes=['', '_'], indicator=True)
    descricao2f=descricao2f[descricao2f['_merge']=='left_only']
    descricao2f=descricao2f.drop(columns='_merge')
    descricao2f['situacao']= "desativado"
    descricao2f=pd.concat([descricaot, descricao2f])
    descricao1f=descricao1f.drop(columns='situacao')
    descricao2final=descricao1f.merge(descricao2f, how='outer',on=['Product','Pipeline','Marca'])
    descricao2final=pd.concat([descricao2final, descricao1old])
    descricao2final=descricao2final.drop_duplicates()
    # atualiza planilha do corne note
    descricao1n=descricao1n[['Hybrid','Pipeline']]
    descricao2n=descricao2n[['Hybrid','Pipeline']]
    descricao2nf=descricao1n.merge(descricao2n, how='outer', suffixes=['', '_'], indicator=True)
    descricao2nf=descricao2nf[descricao2nf['_merge']=='left_only']
    descricao2nf=descricao2nf.drop(columns='_merge')
    descricao2nf['situacao']= "desativado"
    descricao2nf=pd.concat([descricaon, descricao2nf])
    descricao1nf=descricao1nf.drop(columns='situacao')
    descricao2nfinal=descricao1nf.merge(descricao2nf, how='outer',on=['Hybrid','Pipeline'])
    descricao2nfinal=pd.concat([descricao2nfinal, descricao1nold])
    descricao2nfinal=descricao2nfinal.drop_duplicates()
    descricao2final.to_csv('/domino/datasets/local/MD/doencasdemilhomx.csv',index = False)
    descricao2nfinal.to_csv('/domino/datasets/local/MD/notedescripmx1.csv',index = False)
    descricao2nfinal.to_excel('/domino/datasets/local/MD/descriptmx1.xlsx', index = False)
    return render_template("salvo3mx.html")

def salvar6mx():
    datade=daaltera.replace(':','_') 
    datade=datade.replace(' ','_')
    nome=request.headers.get("domino-username") 
    descricao1t =pd.read_excel('/domino/datasets/local/salvar_arquivos/tempmx.xlsx')    
    descricao2t =pd.read_excel('/domino/datasets/local/MD/corpmonitormx.xlsx') 
    descricao1t.to_excel('/domino/datasets/local/MD/corpmonitormx.xlsx', index = False)
    descricao1t.to_excel('/domino/datasets/local/MD/excorpmonitormx.xlsx', index = False)    
    descricao2t.to_excel('/domino/datasets/local/backup_console/corpmonitormx'+ nome + datade +'.xlsx',index = False)
    return render_template("salvo3mx.html")

def salvar7mx():
    datade=daaltera.replace(':','_') 
    datade=datade.replace(' ','_')
    nome=request.headers.get("domino-username")    
    descricao1t=pd.read_csv('/domino/datasets/local/salvar_arquivos/tempmx.csv')
    descricao1t.to_excel('/domino/datasets/local/MD/exnotedescrip1mx.xlsx', index = False)
    descricao2t=pd.read_csv('/domino/datasets/local/MD/notedescrip1mx.csv')
    descricao2t.to_csv('/domino/datasets/local/backup_console/notedescrip1mx'+ nome + datade +'.csv',index = False)
    descricao1t.to_csv('/domino/datasets/local/MD/notedescrip1mx.csv',index = False)
    
    return render_template("salvo3mx.html")
