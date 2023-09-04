from flask_app import app
from flask_app import templates
from flask_app import static
from flask_app.brarquivo import *
from flask_app.brdoencas import *
from flask_app.brnote import *
from flask_app.argdoencas import *
from flask_app.argarquivo import *
from flask_app.argnote import *
from flask_app.mxdoencas import *
from flask_app.mxarquivo import *
from flask_app.mxnote import *
import pandas as pd
from flask import Flask, render_template, redirect, url_for
from flask.globals import request
import time
daaltera=time.ctime()
@app.route("/")
@app.route("/iniciar",methods=['GET', 'POST'])
def iniciar(): 
    if request.method == 'POST': 
        nome = request.headers.get("domino-username")
        pais=request.form['cb1']
        acesso=pd.read_excel("/domino/datasets/local/MD/acesso.xlsx")       
        t = request.form.get('tipo')
        pais=pais.lower()
        nome=nome.lower()
        acesso =acesso[acesso['pais']== pais]        
        acesso =acesso[acesso['usuario']== nome]
        if not(acesso.empty) and acesso['acesso'].values[0]== "s" and t=="on":
            desabilita2 = 'disabled'
            desabilita1 = 'disabled'
            desabilita3 = ''  
            invisivel=''
            if pais == "brasil" :        
                return redirect(url_for("homepage"))
            else:
                if pais == "argentina":
                   return redirect(url_for("homepagear"))
                else:
                   return redirect(url_for("homepagem"))         
        else:
             return render_template("iniciar1.html", invisivel='')
    else:
        invisivel='hidden'                          
    return render_template("iniciar1.html", invisivel=invisivel)

@app.route("/editar2",methods=['POST'])
def editar2(methods=['POST']): 
     return editar2br()
 
@app.route("/editar",methods=['POST'])
def editar(methods=['POST']):      
    return editarbr()

@app.route("/salvar",methods=['POST'])
def salvar(methods=['POST']): 
     return salvarbr()

@app.route("/salvar2",methods=['POST'])
def salvar2(methods=['POST']): 
     return salvar2br()    

@app.route("/doencasmilho",methods=['GET', 'POST'])
def homepage(methods=['GET', 'POST']): 
     return homepagebr()        
   
@app.route("/gestaoprodutos",methods=['GET', 'POST'])
def gestaoprodutos(methods=['GET', 'POST']): 
     return gestaoprodutosbr() 
     
@app.route('/cornote',methods=['GET', 'POST'])
def page1(methods=['GET', 'POST']): 
     return page1br()
@app.route('/DREC_NREC')
def page2(methods=['GET', 'POST']):
    return page2br()
 
@app.route('/pagina_de_descricao')
def page3(methods=['GET', 'POST']): 
     return page3br() 
 
@app.route('/DREC_NREC salvar')
def page4(methods=['GET', 'POST']): 
     return page4br() 
@app.route('/DREC_NREC inicio')
def page4a(methods=['GET', 'POST']): 
     return page4abr() 
 
@app.route('/rm_valoresbr')
def page5(methods=['GET', 'POST']): 
     return page5br() 
 
@app.route('/filtrobr')
def page6(methods=['GET', 'POST']): 
     return page6br()
 
@app.route('/corpmonitorbr')
def page7(methods=['GET', 'POST']): 
     return page7br() 
 
@app.route('/descricaobr')
def page8(methods=['GET', 'POST']): 
     return page8br() 
 
@app.route("/arquivos1",  methods=["GET"])
def get_arquivo(methods=["GET"]):    
    return get_arquivobr()

@app.route("/arquivos2",  methods=["GET"])
def get_arquivo2(methods=["GET"]):   
    return get_arquivo2br()
    
@app.route("/arquivos3",  methods=["GET"])
def get_arquivo3(methods=["GET"]):    
    return get_arquivo3br()
    
@app.route("/arquivos4",  methods=["GET"])
def get_arquivo4(methods=["GET"]):    
    return get_arquivo4br()
    
@app.route("/arquivos5",  methods=["GET"])
def get_arquivo5(methods=["GET"]):    
    return get_arquivo5br()
    
@app.route("/arquivos6",  methods=["GET"])
def get_arquivo6(methods=["GET"]):    
    return get_arquivo6br()

@app.route("/arquivos", methods=["POST"])
def post_arquivo(methods=["POST"]):    
    return post_arquivobr()

@app.route("/arquivos1", methods=["POST"])
def post_arquivo1(methods=["POST"]):    
    return post_arquivobr1()

@app.route("/arquivos2", methods=["POST"])
def post_arquivo2(methods=["POST"]):    
    return post_arquivobr2()

@app.route("/arquivos3", methods=["POST"])
def post_arquivo3(methods=["POST"]):    
    return post_arquivobr3()

@app.route("/arquivos4", methods=["POST"])
def post_arquivo4(methods=["POST"]):    
    return post_arquivobr4()

@app.route("/salvo")
def salvo():
    return render_template("salvo.html")
    
@app.route("/salvo3")
def salvo3():
    return render_template("salvo3.html")   
    
@app.route("/salvo1", methods=["POST"])
def salvo1():
    return salvarbr1()
@app.route("/salvo4", methods=["POST"])
def salvo4():
    return salvarbr4()
@app.route("/salvo5", methods=["POST"])
def salvo5():
    return salvarbr5()
@app.route("/salvo6", methods=["POST"])
def salvo6():
    return salvarbr6()
@app.route("/salvo7", methods=["POST"])
def salvo7():
    return salvarbr7()

@app.route("/salvo2")
def salvo2():
    return render_template("salvo2.html")

@app.route("/editar2ar",methods=['POST'])
def editar2ar(methods=['POST']): 
     return editar2arg() 
@app.route("/editarar",methods=['POST'])
def editarar(methods=['POST']):      
    return editararg()
@app.route("/doencasmilhoar",methods=['GET', 'POST'])
def homepagear(methods=['GET', 'POST']): 
     return homepagearg()   
@app.route("/gestaoprodutosar",methods=['GET', 'POST'])
def gestaoprodutosar(methods=['GET', 'POST']): 
     return gestaoprodutosarg()     
@app.route('/cornotear',methods=['GET', 'POST'])
def page1ar(methods=['GET', 'POST']): 
     return page1arg()
@app.route('/DREC_NRECar')
def page2ar(methods=['GET', 'POST']):
    return page2arg() 
@app.route('/pagina_de_descricaoar')
def page3ar(methods=['GET', 'POST']): 
     return page3arg() 
@app.route('/DREC_NREC salvarar')
def page4ar(methods=['GET', 'POST']): 
     return page4arg()
@app.route('/DREC_NREC inicioar')
def page4aar(methods=['GET', 'POST']): 
     return page4aarg() 
@app.route('/rm_valoresar')
def page5ar(methods=['GET', 'POST']): 
     return page5arg() 
@app.route('/filtroar')
def page6ar(methods=['GET', 'POST']): 
     return page6arg() 
@app.route('/corpmonitorar')
def page7ar(methods=['GET', 'POST']): 
     return page7arg() 
@app.route('/descricaoar')
def page8ar(methods=['GET', 'POST']): 
     return page8arg()
 
@app.route("/arquivos1ar",  methods=["GET"])
def get_arquivoar(methods=["GET"]):    
    return get_arquivoarg()
@app.route("/arquivos2ar",  methods=["GET"])
def get_arquivo2ar(methods=["GET"]):   
    return get_arquivo2arg()    
@app.route("/arquivos3ar",  methods=["GET"])
def get_arquivo3ar(methods=["GET"]):    
    return get_arquivo3arg()    
@app.route("/arquivos4ar",  methods=["GET"])
def get_arquivo4ar(methods=["GET"]):    
    return get_arquivo4arg()    
@app.route("/arquivos5ar",  methods=["GET"])
def get_arquivo5ar(methods=["GET"]):    
    return get_arquivo5arg()    
@app.route("/arquivos6ar",  methods=["GET"])
def get_arquivo6ar(methods=["GET"]):    
    return get_arquivo6arg()

@app.route("/arquivosar", methods=["POST"])
def post_arquivoar(methods=["POST"]):    
    return post_arquivoarg()
@app.route("/arquivos1ar", methods=["POST"])
def post_arquivo1ar(methods=["POST"]):    
    return post_arquivo1arg()
@app.route("/arquivos2ar", methods=["POST"])
def post_arquivo2ar(methods=["POST"]):    
    return post_arquivo2arg()
@app.route("/arquivos3ar", methods=["POST"])
def post_arquivo3ar(methods=["POST"]):    
    return post_arquivo3arg()
@app.route("/arquivos4ar", methods=["POST"])
def post_arquivo4ar(methods=["POST"]):    
    return post_arquivo4arg()

@app.route("/salvararg",methods=['POST'])
def salvarar(methods=['POST']): 
     return salvararg()
     
@app.route("/salvar1ar",methods=['POST'])
def salvar1ar(methods=['POST']): 
     return salvar1arg()
@app.route("/salvar2ar",methods=['POST'])
def salvar2ar(methods=['POST']): 
     return salvar2arg()
@app.route("/salvoar")
def salvoar():
    return render_template("salvoar.html")
@app.route("/salvo3ar")
def salvo3ar():
    return render_template("salvo3arg.html")    
@app.route("/salvo1ar", methods=["POST"])
def salvo1ar():
    return salvar1arg()
@app.route("/salvo4ar", methods=["POST"])
def salvo4ar():
    return salvar4arg()
@app.route("/salvo5ar", methods=["POST"])
def salvo5ar():
    return salvar5arg()
@app.route("/salvo6ar", methods=["POST"])
def salvo6ar():
    return salvar6arg()
@app.route("/salvo7ar", methods=["POST"])
def salvo7ar():
    return salvar7arg()    
@app.route("/salvo2ar")
def salvo2ar():
    return render_template("salvo2ar.html")

@app.route("/editar2m",methods=['POST'])
def editar2m(methods=['POST']): 
     return editar2mx() 
@app.route("/editarm",methods=['POST'])
def editarm(methods=['POST']):      
    return editarmx()
@app.route("/doencasmilhom",methods=['GET', 'POST'])
def homepagem(methods=['GET', 'POST']): 
     return homepagemx()   
@app.route("/gestaoprodutosm",methods=['GET', 'POST'])
def gestaoprodutosm(methods=['GET', 'POST']): 
     return gestaoprodutosmx()     
@app.route('/cornotem',methods=['GET', 'POST'])
def page1m(methods=['GET', 'POST']): 
     return page1mx()
@app.route('/DREC_NRECm')
def page2m(methods=['GET', 'POST']):
    return page2mx() 
@app.route('/pagina_de_descricaom')
def page3m(methods=['GET', 'POST']): 
     return page3mx() 
@app.route('/DREC_NREC salvarm')
def page4m(methods=['GET', 'POST']): 
     return page4mx()
@app.route('/DREC_NREC iniciom')
def page4am(methods=['GET', 'POST']): 
     return page4amx()  
@app.route('/rm_valoresm')
def page5m(methods=['GET', 'POST']): 
     return page5mx() 
@app.route('/filtrom')
def page6m(methods=['GET', 'POST']): 
     return page6mx() 
@app.route('/corpmonitorm')
def page7m(methods=['GET', 'POST']): 
     return page7mx() 
@app.route('/descricaom')
def page8m(methods=['GET', 'POST']): 
     return page8mx()
 
@app.route("/arquivos1m",  methods=["GET"])
def get_arquivom(methods=["GET"]):    
    return get_arquivomx()
@app.route("/arquivos2m",  methods=["GET"])
def get_arquivo2m(methods=["GET"]):   
    return get_arquivo2mx()    
@app.route("/arquivos3m",  methods=["GET"])
def get_arquivo3m(methods=["GET"]):    
    return get_arquivo3mx()    
@app.route("/arquivos4m",  methods=["GET"])
def get_arquivo4m(methods=["GET"]):    
    return get_arquivo4mx()    
@app.route("/arquivos5m",  methods=["GET"])
def get_arquivo5m(methods=["GET"]):    
    return get_arquivo5mx()    
@app.route("/arquivos6m",  methods=["GET"])
def get_arquivo6m(methods=["GET"]):    
    return get_arquivo6mx()

@app.route("/arquivosm", methods=["POST"])
def post_arquivom(methods=["POST"]):    
    return post_arquivomx()
@app.route("/arquivos1m", methods=["POST"])
def post_arquivo1m(methods=["POST"]):    
    return post_arquivo1mx()
@app.route("/arquivos2m", methods=["POST"])
def post_arquivo2m(methods=["POST"]):    
    return post_arquivo2mx()
@app.route("/arquivos3m", methods=["POST"])
def post_arquivo3m(methods=["POST"]):    
    return post_arquivo3mx()
@app.route("/arquivos4m", methods=["POST"])
def post_arquivo4m(methods=["POST"]):    
    return post_arquivo4mx()

@app.route("/salvarm",methods=['POST'])
def salvarm(methods=['POST']): 
     return salvarmx()
@app.route("/salvar2m",methods=['POST'])
def salvar2m(methods=['POST']): 
     return salvar2mx()

@app.route("/salvo3m")
def salvo3m():
    return render_template("salvo3mx.html")    
@app.route("/salvo1m", methods=["POST"])
def salvo1m():
    return salvar1mx()
@app.route("/salvo4m", methods=["POST"])
def salvo4m():
    return salvar4mx()
@app.route("/salvo5m", methods=["POST"])
def salvo5m():
    return salvar5mx()
@app.route("/salvo6m", methods=["POST"])
def salvo6m():
    return salvar6mx()
@app.route("/salvo7m", methods=["POST"])
def salvo7m():
    return salvar7mx() 
@app.route("/salvom")
def salvom():
    return render_template("salvomx.html")   
@app.route("/salvo2m")
def salvo2m():
    return render_template("salvo2mx.html")
    
@app.route("/salvar1m", methods=["POST"])
def salvar1m():
    return salvar1mx()
