import pandas as pd
df=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='comparativo')
dfd=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Diseases_Table')
dfh=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Hybrid_Description')
dfDN=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='DEREC_NREC')
dfFe=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Fenotype')
dfMB=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='m_b_Cultivio_Brands')
dfStb=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Stability_Cultivio_Brands')
dfh2h=pd.read_excel('arquivo_para_md (2).xlsx', sheet_name='H2H')
dfAg=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Agronomicrisk')
dfcorp=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='Crop_Monitoring')
dftt=pd.read_excel('arquivo_para_md (41).xlsx', sheet_name='TT_cumulative')
dfh=dfh.rename(columns={'Hybrid': 'Product'})
dfh=dfh.rename(columns={'Tecnologia': 'Biotecnologias_disponiveis'})
dfh['Pipeline']=dfh['Pipeline'].str.replace('_',' ')
#dfh['min_den']=dfh['min_den'].str[:-2] 
#dfh['max_den']=dfh['max_den'].str[:-2] 
df1=dfh[['Product','Biotecnologias_disponiveis','Pipeline','min_den','max_den']]
df1md=df1
df=pd.merge(df, df1, how = 'left', on = ['Product','Biotecnologias_disponiveis','Pipeline'])
df['tranfmgy']=df['Pipeline'].str.replace(' ','_')
df['Marca']=df['Marca'].str.upper()
dfout=df
df=df[(df['Marca'] =="DEKALB") | (df ['Marca']=="AGROESTE") | (df ['Marca']=="AGROCERES") | (df ['Marca']=="BAYER")]
df=df[df['tranfmgy']=='Tropical_Highlands_Summer']
df=df.replace('Subtropical_Summer',"(BR-Corn-Subtropical-Verão + BR-Corn-Transição-Verão)")
df=df.replace('Subtropical_Winter',"(BR-Corn-Subtropical-inverno + BR-Corn-Transição-inverno)")
df=df.replace('Tropical_Highlands_Summer',"(BR-Corn-Transição-Verão + BR-Corn-Tropical-Verão)")
df=df.replace('Tropical_Highlands_Winter',"(BR-Corn-Transição-Safrinha / BR-Corn-Tropical-Safrinha-Alto)")
df=df.replace('Tropical_Lowlands_Winter',"(BR-Corn-Tropical-Safrinha-Baixo)")
df['catalog_zone']=df['Pipeline'].str.replace(' ','_')
df=df.replace('Subtropical_Summer',"Verão Subtropical (BR)")
df=df.replace('Subtropical_Winter',"Inverno Subtropical (BR)")
df=df.replace('Tropical_Highlands_Summer',"Verão Tropical (BR)")
df=df.replace('Tropical_Highlands_Winter',"Inverno Tropical alto(BR)")
df=df.replace('Tropical_Lowlands_Winter',"Inverno Tropical baixo (BR)")
dfmdf=df
# nitrogenio e Densidade
dfDN=dfDN.rename(columns={'Hybrid': 'Product'})
dfDN=dfDN.rename(columns={'FIELD_pipeline': 'Pipeline'})
DFDN2=dfDN
df['Pipeline']=df['Pipeline'].str.replace(' ','_')
dfDN['Pipeline']=dfDN['Pipeline'].str.replace(' ','_')
df['Pipeline']=df['Pipeline'].str.upper()
dfDN['Pipeline']=dfDN['Pipeline'].str.upper()
dfdngenerico=dfDN[dfDN['Product']=='Genérico']
dfdngenerico=dfdngenerico[dfdngenerico['Pipeline']=='TROPICAL_HIGHLANDS_SUMMER']
dfDN=pd.merge( df,dfDN, how = 'left', on = ['Product','Pipeline'])
dfdnvazios=dfDN[dfDN['DREC_plantas_m2'].isnull()]
dfdnvazios=dfdnvazios[['Product','Biotecnologias_disponiveis','Pipeline','Marca','commercialName','min_den','max_den','tranfmgy','catalog_zone']]
#dfdngenerico=dfdngenerico.drop(columns=['Product'])
dfDN=dfDN.dropna(subset=['DREC_plantas_m2'])
#dfdnvazios=pd.merge( dfdnvazios,dfdngenerico, how = 'left', on = ['Pipeline'])
#dfdnvazios=dfdnvazios.dropna(thresh=3)
dfdnvazios=dfdngenerico
dfDN=pd.concat([dfDN,dfdnvazios])
dfDN['Product']=dfDN['Product'].str.replace(' ','Genérico')
dfdenc=pd.DataFrame()
dfdenc['ID']=" "
dfdenc['Product']=dfDN['Product']+dfDN['tranfmgy']
dfdenc['type']="recommended"
dfdenc['value']=dfDN['DREC_plantas_m2']
dfdenc['min_enviroment']=dfDN['EI_kg_ha']
dfdenc['max_enviroment']=dfDN['EI_kg_ha'] + 100
#dfdenc['min_enviroment']=dfDN['min_enviroment'].astype(int)
#dfdenc['max_enviroment']=dfDN['max_enviroment'].astype(int)
dfn=dfdenc
dfn=dfn.drop(columns=['type'])
dfn['preliminar'] = "FALSO"
dfn['value']=dfDN['NREC']
dfdc=dfdenc
dfdc['type']=dfDN['Type']
dfdc=dfdc.drop(columns=['value'])
dfdc['B0']=dfDN['B0']
dfdc['B1']=dfDN['B1']
dfdc['B2']=dfDN['B2']
dfdc['B3']=dfDN['B3']
dfdc['B4']=dfDN['B4']
dfdc['B5']=dfDN['B5']
dfdc['B6']=dfDN['B6']
dfdc['dm']=" "
dfdc['eiavg']=" "
dfdc['eimin']=" "
dfdc['a0']=" "
dfdc['a1']=" "
dfdc['a2']=" "
dfdenc=dfdenc.fillna(" ")
dfn=dfn.fillna(" ")
dfdc=dfdc.fillna(" ")
dfdc['Product']=dfdc['Product'].str.replace(' ','Genérico')
# doenças do milho
df['Pipeline']=df['Pipeline'].str.replace(' ','_')
dfd['Pipeline']=dfd['Pipeline'].str.replace(' ','_')
df['Pipeline']=df['Pipeline'].str.upper()
dfd['Pipeline']=dfd['Pipeline'].str.upper()
dfd['Marca']=dfd['Marca'].str.upper()
dfd=pd.merge( df,dfd, how = 'left', on = ['Product','Biotecnologias_disponiveis','Pipeline','Marca'])
dffinal1=pd.DataFrame()
dfd['Pipeline']=dfd['tranfmgy']
dfd['Product']=dfd['Product']
dfd=dfd.drop(columns=['commercialName','min_den','max_den','tranfmgy','catalog_zone'])
df1=dfd['Product'].unique()
df2=dfd['Pipeline'].unique()
for p in df2:
    dfpar=dfd[dfd['Pipeline']==p]
    for prod in df1:
        dffinal=dfpar[dfpar['Product']==prod]
        bio=dffinal['Biotecnologias_disponiveis'].unique()
        separator = ','
        result = [separator.join(bio)]
        dffinal['Biotecnologias_disponiveis']=str(result)[2:-2] 
        dffinal1=pd.concat([dffinal1, dffinal])        
dffinal1=dffinal1.replace('MT','2')
dffinal1=dffinal1.replace('MS','4')
dffinal1=dffinal1.replace('M','3')
dffinal1=dffinal1.replace('T','1')
dffinal1=dffinal1.replace('S','5')
dfsepara=dffinal1.drop(columns=['Product','Biotecnologias_disponiveis','Pipeline','Marca'])
dfsepara=dfsepara.columns
dffinal=dffinal1.drop_duplicates()
dffinal=dffinal.reset_index()
#dffinald=pd.DataFrame(columns=['id','product','Biotecnologias_disponiveis','metric','value'])
dffinald=pd.DataFrame(columns=['id','product','metric','value'])
for row in dffinal.index:
    dff=dffinal.loc[[row]]
    for dfsep in dfsepara:        
        id=""
        product=dff['Product'].values[0] + " " + dff['Pipeline'].values[0]
        metric= str(dfsep)
        value=dff[dfsep].values[0] 
        #bio=str(dff['Biotecnologias_disponiveis'].values[0])       
        
        dffinald=dffinald.append({'id':id,'product':product,'metric':metric,'value':value}, ignore_index=True)
               
dffinald= dffinald.dropna() 

dffinald
# Corn note
dfh['Pipeline']=dfh['Pipeline'].str.replace(' ','_')
dfh['Pipeline']=dfh['Pipeline'].str.upper()
dfh=pd.merge( df,dfh, how = 'left', on = ['Product','Biotecnologias_disponiveis','Pipeline'])

df1=dfh['Product'].unique()
df2=dfh['Pipeline'].unique()
dffinal1=pd.DataFrame()
for p in df2:
    dfpar=dfh[dfh['Pipeline']==p]
    for prod in df1:
        dffinal=dfpar[dfpar['Product']==prod]
        bio=dffinal['Biotecnologias_disponiveis'].unique()
        separator = ','
        result = [separator.join(bio)]
        dffinal['Biotecnologias_disponiveis']=str(result)[2:-2] 
        dffinal1=pd.concat([dffinal1, dffinal]) 
        
data1=pd.DataFrame(columns=['nome'])
data1['nome']=dffinal1.columns 
data1=data1[data1['nome'].str.contains("corn_note_text_pt", regex=False)]
data1=data1.reset_index()
data1d=data1['nome'] 
data2=pd.DataFrame(columns=['nome']) 
data2['nome']=['Product','Biotecnologias_disponiveis','Pipeline','tranfmgy']
data3=pd.concat([data2, data1])
data3=data3.reset_index() 
data3d= data3['nome']   
dffinal1=dffinal1.drop_duplicates() 
dffinal1= dffinal1[data3d] 
dffinal1=dffinal1.reset_index()  
dffinalh=pd.DataFrame(columns=['id','Product','Biotecnologias_disponiveis','text_en','text_es','text_pt','order'])

for row in dffinal1.index:
    dff=dffinal1.loc[[row]]
    numero=0
    for dfsep in data1d:        
        id=""
        product=dff['Product'].values[0] + " " + dff['tranfmgy'].values[0]
        order= numero
        text_pt=dff[dfsep].values[0] 
        bio=str(dff['Biotecnologias_disponiveis'].values[0]) 
        numero=numero + 1
        dffinalh=dffinalh.append({'id':id,'Product':product,'Biotecnologias_disponiveis':bio,'text_pt':text_pt,'order':order}, ignore_index=True)
dffinalh=dffinalh.fillna(" ") 
dffinalh=dffinalh.drop_duplicates()              
dffinalh= dffinalh[dffinalh['text_pt']!= " "]  

# fenoogia
dfFe=dfFe.rename(columns={'commercialName': 'Product'})
dfFe=dfFe.rename(columns={'new_pipeline': 'Pipeline'})
dfFe['Pipeline']=dfFe['Pipeline'].str.replace(' ','_')
dfFe['Pipeline']=dfFe['Pipeline'].str.upper()
dfFe=pd.merge( df,dfFe, how = 'left', on = ['Product','Pipeline'])
dfFe=dfFe.rename(columns={ 'Pipeline':'new_pipeline'})
df1=dfh[['Product','Biotecnologias_disponiveis','Pipeline','short_description_pt','refuge_options']]
df1=df1.rename(columns={'Product': 'commercialName','Pipeline': 'new_pipeline'})
df1['catalog_zone']= dfFe['catalog_zone']
df1['zone']= dfFe['tranfmgy']
dffe=dfFe.rename(columns={'EHT': 'Altura de espiga','P50D': 'Floração Masculina','PHT': 'Altura da planta (cm)','S50D': 'Floração Feminina','TKW': 'Peso de 1000 grãos','RM_Calculated': 'Maturidade Relativa','GDU_S50': 'Emergencia gdu para floração','GDU_Emergence_Flowering': 'florecimento'})
dffe['commercialName']=dffe['Product']
dffe1=dffe[['commercialName','new_pipeline','gdus_to_emergence','Emergencia gdu para floração','gdus_to_maturity']]
dffe1s=dffe1
dffe1s['commercialName']=dffe['Product'] + " " + dffe['tranfmgy']
dffe['commercialName']=dffe['Product'] + dffe['Biotecnologias_disponiveis'] + " " + dffe['tranfmgy']
dffe1c=dffe['commercialName']
dffesalva1=dffe
dffesalva1=dffesalva1.drop(columns=['gdus_to_emergence'])
dffesalva1=dffesalva1.drop(columns=['gdus_to_maturity'])
dffesalva1=dffesalva1.drop(columns=['tranfmgy'])
dffesalva1=dffesalva1.drop(columns=['catalog_zone'])
dffesalva1=dffesalva1.drop(columns=['Product'])
dffesalva1=dffesalva1.drop(columns=['Biotecnologias_disponiveis'])
dffesalva1=dffesalva1.drop(columns=['min_den'])
dffesalva1=dffesalva1.drop(columns=['max_den'])
dffesalva1=dffesalva1.drop(columns=['Marca'])
dffe=dffe.drop(columns=['gdus_to_emergence'])
dffe=dffe.drop(columns=['gdus_to_maturity'])
dffe=dffe.drop(columns=['tranfmgy'])
dffe=dffe.drop(columns=['catalog_zone'])
dffe=dffe.drop(columns=['Product'])
dffe=dffe.drop(columns=['Biotecnologias_disponiveis'])
dffe=dffe.drop(columns=['min_den'])
dffe=dffe.drop(columns=['max_den'])
dffe=dffe.drop(columns=['Marca'])
print(dffe)

descricao2=pd.merge(df1, dffe1, how = 'left', on = ['commercialName','new_pipeline'])
df1f=descricao2['commercialName'].unique()
df2f=descricao2['new_pipeline'].unique()
dffinal1=pd.DataFrame()
for p in df2f:
    dfpar=descricao2[descricao2['new_pipeline']==p]
    for prod in df1f:
        dffinal=dfpar[dfpar['commercialName']==prod]        
        bio=dffinal['Biotecnologias_disponiveis'].unique()
        separator = ','
        result = [separator.join(bio)]
        dffinal['Biotecnologias_disponiveis']=str(result)[2:-2] 
        dffinal1=pd.concat([dffinal1, dffinal])
descricao2= dffinal1 
descricao2f=pd.DataFrame(columns=['id','product','zones','catalog_zone','catalog_order','technologies','short_description_en','short_description_es','short_description_pt','refuge_options','preliminar','published','gdus_to_emergence','gdus_to_flowering','gdus_to_maturity','fungicide_planting_en','fungicide_planting_es','fungicide_planting_pt','fungicide_vegetative_en','fungicide_vegetative_es','fungicide_vegetative_pt','fungicide_reproductive_en','fungicide_reproductive_es','fungicide_reproductive_pt','new_product'])
descricao2f['product']=descricao2['commercialName'] + " / BR"
descricao2f['zones']=descricao2['zone']
descricao2f['short_description_pt']=descricao2['short_description_pt']
descricao2f['technologies']=descricao2['Biotecnologias_disponiveis']
descricao2f['refuge_options']=descricao2['refuge_options']
descricao2f['gdus_to_emergence']=descricao2['gdus_to_emergence']
descricao2f['gdus_to_flowering']=descricao2['Emergencia gdu para floração']
descricao2f['gdus_to_maturity']=descricao2['gdus_to_maturity']
descricao2f['catalog_zone']=descricao2['catalog_zone']
descricao2f['preliminar']='false'
descricao2f['published']='true'
descricao2f
dfsepara=dffe.drop(columns=['commercialName','new_pipeline'])
dfsepara=dfsepara.columns
dffes1=dffe
dffes1['commercialName']=dffe1s['commercialName']
dffinal=dffes1.drop_duplicates()
dffinal=dffinal.reset_index()
df1fe=dffinal
dffinaldfe=pd.DataFrame(columns=['id','product','feature','value_en','value_es','value_pt'])
dffinal=dffes1.drop_duplicates()
dffinal=dffinal.reset_index()
for row in dffinal.index:
    dff=dffinal.loc[[row]]
    for dfsep in dfsepara:        
        id=""
        product=dff['commercialName'].values[0] 
        feature= str(dfsep)
        value_pt=dff[dfsep].values[0]         
        dffinaldfe=dffinaldfe.append({'id':id,'product':product,'feature':feature,'value_en':value_pt,'value_es':value_pt,'value_pt':value_pt}, ignore_index=True)
dffinaldfe=dffinaldfe.drop_duplicates()
dffinaldfe=dffinaldfe.dropna()

#MB
dfMB['Pipeline']=dfMB['Pipeline'].str.replace(' ','_')
dfMB['Pipeline']=dfMB['Pipeline'].str.upper()
dfMB=pd.merge( dfmdf,dfMB, how = 'left', on = ['commercialName','Pipeline'])
dfdmb=pd.DataFrame()
dfdmb['ID']=" "
dfdmb['Product']=dfMB['Product']+ " "+ dfMB['tranfmgy']
dfdmb['m']=dfMB['m']
dfdmb['b']=dfMB['p_value']
dfdmb['type']="estimated_yield"
dfdmb['min_enviroment']=dfMB['min_den'].astype(str)
dfdmb['max_enviroment']=dfMB['max_den'].astype(str)
dfdmb['is_featured']="VERDADEIRO"
dfdmb=dfdmb.drop_duplicates()
dfdmb=dfdmb.dropna(thresh=3)
#Stability
dfStb=dfStb.rename(columns={'Head': 'commercialName'})
dfStb=dfStb.rename(columns={'Protocol': 'Pipeline'})
dfStb['Pipeline']=dfStb['Pipeline'].str.replace(' ','_')
dfStb['Pipeline']=dfStb['Pipeline'].str.upper()
dfStb=pd.merge( df,dfStb, how = 'left', on = ['commercialName','Pipeline'])
dfdt=pd.DataFrame()
dfdt['ID']=" "
dfdt['Product']=dfStb['commercialName']+ " " + "/BR"
dfdt['zones']=dfStb['tranfmgy']
dfdt['season']=dfStb['Season']
dfdt['field']=dfStb['Field']
dfdt['environment']=dfStb['Environment']
dfdt['result']=dfStb['Check_Mean']
#dfdt['environment']=dfdt['environment'].astype(int)
#dfdt['result']=dfdt['result'].astype(int)
dfdt=dfdt.fillna(" ")

# H2H
df1h=df.rename(columns={'commercialName':'Head' })
df1ou=dfout.rename(columns={'commercialName':'Other' })
df1ou=df1ou.rename(columns={'Marca':'MarcaOther' })
df1ou=df1ou[['Other','MarcaOther']]
dfh2h['Pipeline']=dfh2h['Pipeline'].str.replace(' ','_')
dfh2h['Pipeline']=dfh2h['Pipeline'].str.upper()
dfh2h=pd.merge( df1h,dfh2h, how = 'left', on = ['Head','Pipeline'])
dfh2hs=pd.merge( dfh2h,df1ou, how = 'left', on = ['Other'])
dfh2hs['MarcaOther']=dfh2hs['MarcaOther'].str.upper()
dfh2hs=dfh2hs[dfh2hs['MarcaOther']!='REFUGIOMAX']
dfh2h=pd.DataFrame()
dfh2h['ID']=" "
dfh2h['Head']=dfh2hs['Head']+ " " + "/BR"
dfh2h['other']=dfh2hs['Other']+ " " + "/BR"
dfh2h['zones']=dfh2hs['tranfmgy']
dfh2h['season']=" "
dfh2h['type']="yield"
dfh2h['value']=dfh2hs['diffmean']
dfh2h['result']=dfh2hs['pvalue'].apply(lambda x: "Tie" if x>0.1 else "not Tie") 
dfh2h['result/pt']=" " 
dfh2hcomtie=dfh2h[dfh2h['result']== "Tie"]
dfh2hsemtie=dfh2h[dfh2h['result']== "not Tie"]
dfh2hcomtie['result/pt']="Empate" 
dfh2hsemtie['result/pt']=dfh2hs['percent_wins'].apply(lambda x: "Derrota" if x<50 else "Vitoria")
dfh2h=pd.concat([dfh2hcomtie, dfh2hsemtie])
dfh2h=dfh2h.sort_values(['Head'])
dfh2h['trial_count']=dfh2hs['n']
dfh2h['win_rate']=dfh2hs['percent_wins']
dfh2h['min_environment']=dfh2hs['EI']
dfh2h=dfh2h.replace('<60',"0")
dfh2h=dfh2h.replace('<90',"0")
dfh2h=dfh2h.replace('>120',"12000")
dfh2h=dfh2h.replace('>130',"13000")
dfh2h=dfh2h.replace('>85',"8500")
dfh2h=dfh2h.replace('>90',"9000")
dfh2h=dfh2h.replace('60-85',"6000")
dfh2h=dfh2h.replace('60-90',"6000")
dfh2h=dfh2h.replace('90-120',"9000")
dfh2h=dfh2h.replace('90-130',"9000")
dfh2h=dfh2h.replace('ALL',"0")        
dfh2h['max_environment']=dfh2hs['EI']
dfh2h=dfh2h.replace('<60',"6000")
dfh2h=dfh2h.replace('<90',"9000")
dfh2h=dfh2h.replace('>120'," ")
dfh2h=dfh2h.replace('>130'," ")
dfh2h=dfh2h.replace('>85'," ")
dfh2h=dfh2h.replace('>90'," ")
dfh2h=dfh2h.replace('60-85',"8500")
dfh2h=dfh2h.replace('60-90',"9000")
dfh2h=dfh2h.replace('90-120',"12000")
dfh2h=dfh2h.replace('90-130',"13000")
dfh2h=dfh2h.replace('ALL'," ")
dfh2h['published']="VERDADEIRO"
dfh2h=dfh2h.drop_duplicates()
dfh2h=dfh2h.fillna(" ")
saidadfsb=dfh2h[:20]

#Agronomicrisk
dfAg=dfAg.rename(columns={'new_pipeline': 'Pipeline'})
dfAg['Pipeline']=dfAg['Pipeline'].str.replace(' ','_')
dfAg['Pipeline']=dfAg['Pipeline'].str.upper()
dfAg=pd.merge( df,dfAg, how = 'left', on = ['Product','Pipeline'])
dfAg['Product']=dfAg['Product'] + " "+ dfAg['tranfmgy']
dfAgs=dfAg
dfAg['min_environment']=dfAgs['EIRange']
dfAg=dfAg.replace('<60',"0")
dfAg=dfAg.replace('<90',"0")
dfAg=dfAg.replace('>120',"12000")
dfAg=dfAg.replace('>130',"13000")
dfAg=dfAg.replace('>85',"8500")
dfAg=dfAg.replace('>90',"9000")
dfAg=dfAg.replace('60-85',"6000")
dfAg=dfAg.replace('60-90',"6000")
dfAg=dfAg.replace('90-120',"9000")
dfAg=dfAg.replace('90-130',"9000")
dfAg=dfAg.replace('ALL',"0")        
dfAg['max_environment']=dfAgs['EIRange']
dfAg=dfAg.replace('<60',"6000")
dfAg=dfAg.replace('<90',"9000")
dfAg=dfAg.replace('>120'," ")
dfAg=dfAg.replace('>130'," ")
dfAg=dfAg.replace('>85'," ")
dfAg=dfAg.replace('>90'," ")
dfAg=dfAg.replace('60-85',"8500")
dfAg=dfAg.replace('60-90',"9000")
dfAg=dfAg.replace('90-120',"12000")
dfAg=dfAg.replace('90-130',"13000")
dfAg=dfAg.replace('ALL'," ")
dfAg['EIRange']=dfAgs['EIRange']
dffinalAG=dfAg[['Product','npositive','prop_win','min_environment','max_environment','averageEI']]

#dfAg.to_csv('convfiltro.csv',index = False)
w=pd.ExcelWriter('planilha_cultivio_changestropical0808.xlsx')
dffinal=dfdenc.drop_duplicates()
dffinal['Product']=dffinal['Product'].str.replace(' ','Genérico')
dffinal.to_excel(w,sheet_name='CornDensity',index=False)
dffinal=dfn.drop_duplicates()
dffinal['Product']=dffinal['Product'].str.replace(' ','Genérico')
dffinal.to_excel(w,sheet_name='CornNitrogenCoefficients',index=False)
dffinal=dfdc.drop_duplicates()
dffinal['Product']=dffinal['Product'].str.replace(' ','Genérico')
dffinal.to_excel(w,sheet_name='CornDensityCoefficient',index=False)
dffinal=dffinalh.drop_duplicates()
dffinal.to_excel(w,sheet_name='CornNote',index=False)
dffinal=dffinald.drop_duplicates()
dffinal.to_excel(w,sheet_name='CornMetricValue',index=False)
dffinal=dfdmb.drop_duplicates()
dffinal.to_excel(w,sheet_name='CornProductRanking',index=False)
dffinal=dffinaldfe.drop_duplicates()
dffinal.to_excel(w,sheet_name='CornFeatureValue',index=False)
dffinal=descricao2f.drop_duplicates()
dffinal.to_excel(w,sheet_name='CornProductProfile',index=False)
dffinal=dfdt.drop_duplicates()
dffinal.to_excel(w,sheet_name='Ensaios_Stability',index=False)
dffinal=dffesalva1.drop_duplicates()
dffinal.to_excel(w,sheet_name='Fenotype',index=False)
dffinal=dfh2h.drop_duplicates()
dffinal.to_excel(w,sheet_name='H2H',index=False)
dffinal=dffinalAG.drop_duplicates()
dffinal.to_excel(w,sheet_name='Agronomicrisk',index=False)
dffinal=dfcorp.drop_duplicates()
dffinal.to_excel(w,sheet_name='Crop_Monitoring',index=False)
dffinal=dftt.drop_duplicates()
dffinal.to_excel(w,sheet_name='TT_cumulative',index=False)
w.save()
print(dffesalva1['commercialName'])
print(DFDN2)