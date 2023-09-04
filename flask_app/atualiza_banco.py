import hvac
import base64
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import pandas_gbq
import sys
import os
import db_dtypes 
import pandas as pd
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

def get_secret_from_vault(approle_id, approle_secret, vault_path):
  client = hvac.Client(url='https://vault.agro.services')
  #client.is_authenticated()
  client.auth_approle(approle_id, approle_secret)
  return client.read(vault_path)

approle_id = os.environ['APPROLEID']
approle_secret=os.environ['APPROLESECRET']

secrets = get_secret_from_vault(approle_id = approle_id,
                                approle_secret = approle_secret,
                                vault_path='secret/csw/service-identities/md-latam-bq-viewers') 

if 'data' in secrets and type(secrets['data']['data']) == str:
  service_account_creds = json.loads(base64.b64decode(secrets['data']['data']))
else:
  # in case credentials are saved directly as json object in vault (not encoded) you can get it directly
  service_account_creds = secrets

bq_credentials = service_account.Credentials.from_service_account_info(service_account_creds)
bq_proj='bcs-market-dev-lake'

bq_client = bigquery.Client(project = bq_proj, credentials = bq_credentials)
bq_query = '''
SELECT *
FROM latam_datasets.stab_brazil_corn
'''
bqresults = pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
def comparativo():
    descricao1 = pd.read_csv('/domino/datasets/local/MD/dadosparafiltro.csv')
    descricao1['situacao']=descricao1['situacao'].str.lower()
    descricao1=descricao1.loc[(descricao1['situacao'] == "ativo") | (descricao1['situacao'] == "lançamento")]
    descricao1=descricao1[['Product','Biotecnologias_disponiveis','Pipeline']]
    descricao1['commercialName']=descricao1['Product']+descricao1['Biotecnologias_disponiveis'] 
    descricao1.to_csv('/domino/datasets/local/MD/comparativobra.csv',index = False)
    comparativo=descricao1
    return comparativo

def stability():
    bq_query = '''
    SELECT *
    FROM latam_datasets.stab_brazil_corn
    '''
    data1= pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    data1['Variable'].unique()
    data2=data1.query('Variable == "YLD"')
    data2=data2.query('Protocol == "FTN"')
    data2=data2.drop(columns=['Protocol','Country','Macroregion','Variable','Other','Other_mean','updated_at'])
    data2=data2.drop_duplicates()
    data2['Head_mean']=(data2['Head_mean'].astype(float))*100
    data2['EI']=(data2['EI'].astype(float))*100    
    data_concorrente = pd.read_excel("/domino/datasets/local/MD/concorrentes.xlsx")
    #separa os hybridos que serão filtrados
    descricao1 = pd.read_csv('/domino/datasets/local/MD/dadosparafiltro.csv')
    descricao1['situacao']=descricao1['situacao'].str.lower()
    descricao1=descricao1.loc[(descricao1['situacao'] == "ativo") | (descricao1['situacao'] == "lançamento")]
    descricao1['produto']=(descricao1['Product']+descricao1['Biotecnologias_disponiveis'])
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Winter","Subtropical Winter Winter")
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Summer","Subtropical Summer Summer")
    safra1=descricao1['Pipeline'].unique()
    descricao1['Marca']=descricao1['Marca'].str.upper()
    
    safra=safra1.tolist()
    dffinal=descricao1
    fdf =dffinal
    nomes = fdf['produto'].tolist()
    pipeline = fdf['Pipeline'].unique().tolist()
    fdf[fdf['Marca']=="LICENSING"]="BAYER"
    fdf[fdf['Marca']=="Bayer"]="BAYER"
    Marca =fdf['Marca'].unique().tolist()
        # faz a união de dois frames
    data_marca=dffinal.query('Marca =="DEKALB" | Marca=="AGROESTE" | Marca=="AGROCERES"')
    dfbayer = dffinal.query('Marca =="BAYER"')
    Marca= ["DEKALB","AGROESTE","AGROCERES"]
    dfferente=dffinal.query('Marca !="DEKALB" & Marca!="AGROESTE" & Marca!="AGROCERES" & Marca !="BAYER"')

    #criar uma tabela com os hibridos concorrentes
    concorrencia_list=(data_concorrente['Hybrids'].tolist() + dfferente['produto'].tolist())
    ps4_list=dfbayer['produto'].tolist()     
    #Filtrando final
    lista_final=(data_marca['produto'].tolist() + concorrencia_list)
    data3=data2.loc[data2['Head'].isin(lista_final)]    
    data3=data3.loc[data3['Pipeline'].isin(safra1)]
   
    descricao1=descricao1.rename(columns = {'produto':'Head'})
    descricao1=descricao1.rename(columns = {'produto':'Head'})
    descricao1=descricao1.drop(columns=['Product','Biotecnologias_disponiveis','Marca','fenotipe'])
    data3=pd.merge(descricao1, data3, how = 'right', on = ['Head','Pipeline'])
    data3['Pipeline']=data3['Pipeline'].str.replace("Subtropical Winter Winter","Subtropical Winter")
    data3['Pipeline']=data3['Pipeline'].str.replace("Subtropical Summer Summer","Subtropical Summer")
    data3['Pipeline']=data3['Pipeline'].str.replace(' ','_')
    data3=data3.loc[(data3['situacao'] == "ativo") | (data3['situacao'] == "lançamento")] 
    data3=data3.drop(columns=['situacao'])
    data4 = data3    
    data4 = data4.rename(columns = {'Year':'Season','Pipeline':'Protocol','FIELD_name':'Field','EI':'Environment','Head_mean':'Check_Mean'})
    data4a=data4
    data4a=data4a.replace(" ","NaN")
    filtro=data4a[data4a['Environment']=="NaN"]
    data4a=data4a.drop(filtro.index)
    data4a.to_csv('Stability_Cultivio_Brands_1602.csv',index = False)
    stability1=data4
    data4a.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_Stability_Cultivio_Brands',
                            if_exists = 'replace')
    return stability1
def m_b():
    data4=stability()
    data5=data4[['Protocol','Head']]
    data5['valoresun']=(data5['Protocol'] +'_'+ data5['Head'])
    data5['ndata']=data5.groupby('valoresun')['valoresun'].transform('count')
    datapoints=data5[['Protocol','Head','ndata']]
    datapoints=datapoints.drop_duplicates()
    dfb=datapoints[datapoints['ndata']>4]
    hybs5=dfb['Head'].unique().tolist()
    data5=data4.loc[data4['Head'].isin(hybs5)]
    pipe=data5['Protocol'].unique()
    dffinal_df = pd.DataFrame(columns=['Pipeline','commercialName','m','b','r2','p_value'])

    for o in range(len(pipe)):
        df1=data5[data5['Protocol']==pipe[o]]
        names = df1['Head'].unique()
        for n in range(len(names)):
            df2=df1[df1['Head']==names[n]]
            df2['Check_Mean']=df2['Check_Mean'].fillna(0)
            df2['Environment']=df2['Environment'].fillna(0)
            y= pd.DataFrame(df2['Check_Mean'])
            X= pd.DataFrame(df2['Environment'])
            results = smf.ols('Check_Mean~Environment', data=df2).fit()
            lm = linear_model.LinearRegression()
            model = lm.fit(X,y)
            p_value= results.pvalues[1]
            r2=results.rsquared
            b = lm.intercept_
            b=str(b)[1:-1] 
            m = lm.coef_
            m =str(m)[2:-2] 
            commercialName=df2['Head'].unique()
            commercialName=str(commercialName)[2:-2] 
            Pipeline=df2['Protocol'].unique()
            Pipeline=str(Pipeline)[2:-2] 
            dffinal_df.loc[len(dffinal_df)]=[Pipeline,commercialName,m,b,r2,p_value]
    dffinal_df=dffinal_df.dropna(thresh=3)        
    dffinal_df.to_csv('m_b_Cultivio_Brands_1602.csv',index = False)
    m_b1=dffinal_df
    m_b1.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_m_b_Cultivio_Brands',
                            if_exists = 'replace')
    return m_b1

def phenotype():
    #carrega o banco historico
    bq_query = '''
    SELECT *
    FROM latam_datasets.hss_brazil_historical_corn
    WHERE OBS_observationRefCd IN ('YLD','MST','S50D','P50D','EHT','PHT','TKW') AND
    protocolType IN ('FTN') AND
    QC_Flag is null
    '''
    #carrega o banco atual
    data_historical=pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    bq_query ='''
    SELECT *
    FROM latam_datasets.hss_brazil_current_corn
    WHERE OBS_observationRefCd IN ('YLD','MST','S50D','P50D','EHT','PHT','TKW') AND
    protocolType IN ('FTN') AND
    QC_Flag is null
    '''
    data_current=pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    data_historical['OBS_descriptorAbbreviation'].fillna('N/A', inplace=True) 
    data_current['OBS_descriptorAbbreviation'].fillna('N/A', inplace=True) 
    data_historical['OBS_code']=(data_historical['OBS_observationRefCd'] + "." + data_historical['OBS_descriptorAbbreviation'])
    data_current['OBS_code']=(data_current['OBS_observationRefCd'] + "." + data_current['OBS_descriptorAbbreviation'])
    data_current=data_current.drop(columns=['OBS_observationRefCd'])
    data_current=data_current.drop(columns=['OBS_descriptorAbbreviation'])
    data_historical=data_historical.drop(columns=['OBS_observationRefCd'])
    data_historical=data_historical.drop(columns=['OBS_descriptorAbbreviation'])
    data_current=data_current.drop(columns=['midas_germplasm_id'])
    data_historical=data_historical.drop(columns=['midas_germplasm_id'])
    a = data_historical.columns.values.tolist()
    data_historical['OBS_code']=data_historical['OBS_code'].replace("PHT.R1","PHT.N/A")
    data_historical['OBS_code']=data_historical['OBS_code'].replace("PHT.VT","PHT.N/A")
    code=["TKW.N/A","EHT.N/A","MST.N/A","YLD.N/A","S50D.N/A","PHT.N/A","P50D.N/A"]
    data_current=data_current.loc[data_current['OBS_code'].isin(code)]
    data_historical=data_historical.loc[data_historical['OBS_code'].isin(code)]
    #data_current=data_current.loc[a]
    brazil_nonpivot=pd.concat([data_current, data_historical])
    brazil_nonpivot['new_pipeline']=(brazil_nonpivot['FIELD_pipeline']+"_"+brazil_nonpivot['FIELD_seasonName'])
    brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace(' ','_')
    brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace("Tropical_Lowlands_Summer","Tropical_Highlands_Summer")
    #brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace('_',' ')
    descricao1 = pd.read_csv('/domino/datasets/local/MD/dadosparafiltro.csv')
    descricao1['commercialName']=(descricao1['Product']+descricao1['Biotecnologias_disponiveis'])
    prefixo1=descricao1['Biotecnologias_disponiveis'].unique()
    descricao1=descricao1.drop(columns=['Biotecnologias_disponiveis'])
    descricao1=descricao1.dropna(subset=['fenotipe'])
    descricao1=descricao1.drop(columns=['Marca'])
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Winter","Subtropical Winter Winter")
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Summer","Subtropical_Summer_Summer")
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace(' ','_')
    descricao1=descricao1.rename(columns={'Pipeline': 'new_pipeline'})
    brazil_nonpivot=pd.merge(descricao1,brazil_nonpivot, how = 'left', on = ['commercialName','new_pipeline']) 
    
    brazil_nonpivot=brazil_nonpivot[(brazil_nonpivot['situacao']== "ativo") | (brazil_nonpivot['situacao'] == "Lançamento")]    
    descricao1=descricao1.loc[(descricao1['situacao'] == "ativo") | (descricao1['situacao'] == "Lançamento")]
        
    safra1=descricao1['new_pipeline'].unique()
    safra=safra1.tolist()
    dffinal=descricao1
    fdf =dffinal
    nomes = fdf['commercialName'].tolist()
    pipeline = fdf['new_pipeline'].unique().tolist()    
        # faz a união de dois frames
    
        #Filtrando final
    lista_final=(fdf['commercialName'].tolist())
    pipes=safra
    data3=brazil_nonpivot
    data4=data3
    data4=brazil_nonpivot      
    # ver como fazer Fenotipico
    data4=data4[['new_pipeline','commercialName','Product','OBS_code','OBS_numValue']]
    data4=data4.loc[(data4['OBS_code'] != "YLD.N/A") ]
    data4=data4.loc[(data4['OBS_code'] != "MST.N/A") ]
    data4['OBS_code']=data4['OBS_code'].replace("TKW.N/A","TKW")
    data4['OBS_code']=data4['OBS_code'].replace("EHT.N/A","EHT")
    data4['OBS_code']=data4['OBS_code'].replace("S50D.N/A","S50D")
    data4['OBS_code']=data4['OBS_code'].replace("P50D.N/A","P50D")
    data4['OBS_code']=data4['OBS_code'].replace("PHT.N/A","PHT")
  
    data4a=data4
    #data4=data4.drop(columns=['Product'])
    fenotipico=data4.groupby(['new_pipeline','Product','commercialName','OBS_code'])['OBS_numValue'].mean
    fenotipico=data4.pivot_table(index=['commercialName','new_pipeline','Product'], columns='OBS_code',values='OBS_numValue')
    fenotipico.reset_index(inplace=True)
    fenotipico=fenotipico.round(0)    
    fenotipico = fenotipico.drop_duplicates()
    end_piv= fenotipico
    end_piv['new_pipeline']=end_piv['new_pipeline'].str.replace("Subtropical_Summer_Summer","Subtropical_Summer")
    end_piv['new_pipeline']=end_piv['new_pipeline'].str.replace("Subtropical_Winter_Winter","Subtropical_Winter")
    descricao3 = pd.read_excel('/domino/datasets/local/MD/rm_valores.xlsx')
    descricao3=descricao3.drop(columns=['RM'])
    descricao3=descricao3.drop_duplicates()
    descricao3=descricao3.rename(columns={'FIELD pipeline':'new_pipeline'})
    descricao3['new_pipeline']= descricao3['new_pipeline'].str.replace(' ','_')
    descricao3=pd.merge(end_piv,descricao3, how = 'left', on = ['commercialName','new_pipeline'])     
    
    end_piv.to_csv('phenotype22a.csv',index = False)
    #mudança de comercial name para product
    data4a['commercialName']=data4a['Product']
    fenotipicoa=data4a.groupby(['new_pipeline','commercialName','OBS_code'])['OBS_numValue'].mean
    fenotipicoa=data4a.pivot_table(index=['commercialName','new_pipeline'], columns='OBS_code',values='OBS_numValue')
    fenotipicoa.reset_index(inplace=True)
    fenotipicoa=fenotipicoa.round(0)    
    fenotipicoa = fenotipicoa.drop_duplicates()
    end_piva= fenotipicoa
    end_piva['new_pipeline']=end_piva['new_pipeline'].str.replace("Subtropical_Summer_Summer","Subtropical_Summer")
    end_piva['new_pipeline']=end_piva['new_pipeline'].str.replace("Subtropical_Winter_Winter","Subtropical_Winter")
    end_piva.to_csv('phenotype23a.csv',index = False)
    rm1=pd.read_excel("/domino/datasets/local/MD/rm_valores.xlsx")
    brazil_nonpivot['OBS_code']=brazil_nonpivot['OBS_code'].replace("MST.N/A","MST")
    brazil_nonpivot['OBS_code']=brazil_nonpivot['OBS_code'].replace("YLD.N/A","YLD")    
    pipes1=brazil_nonpivot['new_pipeline'].unique()
    pipes=pipes1.tolist()
    data5r=rm1[['commercialName','new_pipeline','RM']]
    df9 = pd.DataFrame()
    d=0
    for o in range(len(pipes)):
            
            dados1=brazil_nonpivot[brazil_nonpivot['new_pipeline']==pipes[o]]        
            trait=["YLD","MST"]
            dados2=dados1.loc[dados1['OBS_code'].isin(trait)]
            seasons=dados2['FIELD_plantingSeason'].unique()
            season=seasons.tolist()
            for s in range(len(season)):
                
                dados3=dados2.loc[dados2['FIELD_plantingSeason']==season[s]]
                data_piv=dados3.pivot_table(index=['FIELD_plantingSeason','new_pipeline','FIELD_field_latitude','FIELD_field_longitude','FIELD_locationName','FIELD_plantingDate','FIELD_name','commercialName'], columns='OBS_code',values='OBS_numValue')

                data_piv.reset_index(inplace=True)

                data4=data_piv[['FIELD_plantingSeason','new_pipeline','FIELD_field_latitude','FIELD_field_longitude','FIELD_locationName','FIELD_plantingDate','FIELD_name','commercialName','MST']]
                data4['new_pipeline']=data4['new_pipeline'].str.replace("Subtropical_Summer_Summer","Subtropical_Summer")
                data4['new_pipeline']=data4['new_pipeline'].str.replace("Subtropical_Winter_Winter","Subtropical_Winter")
                
                pipe1=data4['new_pipeline'].unique()                
                data5=pd.merge(data4, data5r, how = 'left', on = ['commercialName','new_pipeline'])
                datapoints=data5                
                datapoints=datapoints.dropna(subset=['MST'])
                datapoints['ndata']= datapoints.groupby('FIELD_name')['FIELD_name'].transform('count')
                
                dfa=datapoints[datapoints['ndata']>=10]
                bb=dfa['FIELD_name'].unique()
                data5=data5.loc[data5['FIELD_name'].isin(bb)]
                sim=data5
                sim=sim.dropna(subset=['RM']) 
                sim['ndata']= sim.groupby('FIELD_name')['FIELD_name'].transform('count')
                datapoints=sim
                datapoints=datapoints.dropna(subset=['MST'])
                dfa=datapoints[datapoints['ndata']>=4]
                bb=dfa['FIELD_name'].unique()
                bb15=bb
                dados5=data5.loc[data5['FIELD_name'].isin(bb)]
                dados15=dados5 
                
                if(dados5['FIELD_name'].count() > 0):
                    Fields=dados5['FIELD_name'].unique()
                    for i in range(len(Fields)):
                        
                        fld=dados5[dados5['FIELD_name']==Fields[i]] 
                        values=fld['MST'].astype(float) 
                        if(len(values) > 4):                             
                            fld=fld.dropna(subset=['MST']) 
                            fld1=fld          
                            fld1=fld1.dropna(subset=['RM'])
                            fld['RM']=fld['RM'].fillna(0) 
                            fld['RM']=fld['RM'].astype(float)
                            y= pd.DataFrame(fld1['RM'])
                            X= pd.DataFrame(fld1['MST']) 
                            results = smf.ols('MST~ RM', data=fld1).fit()                                        
                            lm = linear_model.LinearRegression()
                            model = lm.fit(X,y) 
                            slope= lm.coef_
                            #slope=str(slope)[2:-2] 
                            slope=float(slope)                       
                            intercept=lm.intercept_
                            #intercept=str(intercept)[1:-1]
                            intercept=float(intercept)                        
                            rsquare=results.rsquared            
                            p_value= results.pvalues[0]            
                            fld['RM_Calculated']=(slope*fld['MST']+intercept)
                            fld['p_value']=p_value
                            fld['rsquare']=rsquare                        
                            df9=pd.concat([df9,fld])                        
                            d=d+1
    df9['concat']=(df9['new_pipeline'] +"_"+ df9['FIELD_plantingSeason'].astype(str) +"_"+ df9['FIELD_name'] ) 
    check=df9.groupby(['new_pipeline','FIELD_plantingSeason','FIELD_name']).mean(['rsquare','p_value']) 
    check.reset_index(inplace=True) 
    check['concat']=(check['new_pipeline'] +"_"+ check['FIELD_plantingSeason'].astype(str) +"_"+ check['FIELD_name'] )  
    dfb=check[check['p_value'] > 0.15]
    dfbb=dfb['concat'].unique() 
    bem=df9.loc[df9['concat'].isin(dfbb)]
    bem=bem[['commercialName','FIELD_plantingSeason','new_pipeline','FIELD_name','RM_Calculated','p_value','rsquare']]
    #mudanca de comercial name para product
    for prefixo in prefixo1:   
        bem['commercialName']= bem['commercialName'].str.replace(prefixo,"")  
    #bem['commercialName']= bem['commercialName'].str.replace("PRO4","")
    #bem['commercialName']= bem['commercialName'].str.replace("PRO2","")
    bem['new_pipeline']=bem['new_pipeline'].str.replace("Subtropical_Summer_Summer","Subtropical_Summer")
    bem['new_pipeline']=bem['new_pipeline'].str.replace("Subtropical_Winter_Winter","Subtropical_Winter")   
    final=bem.groupby(['new_pipeline','commercialName']).mean(['RM_Calculated'])
    final.reset_index(inplace=True)  
    final=final[['new_pipeline','commercialName','RM_Calculated']]
    final1=final[final['RM_Calculated'] < 145.0]
    final1.to_csv('rm_calculated2a.csv',index = False)
    rmcalculated=final1    
    descricao = descricao3
    descricao1r = rmcalculated  
    descricao['commercialName']=descricao['Product']    
    descricao['new_pipeline']= descricao['new_pipeline'].str.replace(' ','_')
    descricao['new_pipeline']=descricao['new_pipeline'].replace("Subtropical_Winter_Winter","Subtropical_Winter")
    descricao['new_pipeline']=descricao['new_pipeline'].replace("Subtropical_Summer_Summer","Subtropical_Summer")    
    descricao2=pd.merge(descricao, descricao1r, how = 'left', on = ['commercialName','new_pipeline'])
    #descricao2=pd.merge(descricao2, descricao3, how = 'left', on = ['commercialName','new_pipeline'])
    descricao2.drop_duplicates()
    descricao2['GDU_S50']= descricao2['GDU_S50'].fillna(-1)
    descricao2['GDU_P50']= descricao2['GDU_P50'].fillna(-1)
    descricao2['GDU_S50']= descricao2['GDU_S50'].astype(int)
    descricao2['GDU_P50']= descricao2['GDU_P50'].astype(int)
    descricao2['GDU_S50']= descricao2['GDU_S50'].astype(str)
    descricao2['GDU_P50']= descricao2['GDU_P50'].astype(str)
    descricao2['GDU_S50']= descricao2['GDU_S50'].str.replace('-1','')
    descricao2['GDU_P50']= descricao2['GDU_P50'].str.replace('-1','')    
    descricao2.columns = ['commercialName','new_pipeline','Product','EHT','P50D','PHT','S50D','TKW','gdus_to_emergence','GDU_S50','GDU_P50','gdus_to_maturity','GDU_Emergence_Flowering','Arquitetura_Foliar','Tipo_de_Grao','Cor_Grao','Empalhamento','Ciclo','Secagem','RM_Calculated']
    descricao2=descricao2[['commercialName','new_pipeline','EHT','P50D','PHT','S50D','TKW','RM_Calculated','gdus_to_emergence','GDU_S50','GDU_P50','gdus_to_maturity','GDU_Emergence_Flowering','Arquitetura_Foliar','Tipo_de_Grao','Cor_Grao','Empalhamento','Ciclo','Secagem']]
    descricao2.to_csv('Fenotype82a.csv',index = False)
    descricao2.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_Fenotype',
                            if_exists = 'replace')
    return fenotipico,rmcalculated,dffinal,descricao2

def h2h():
    bq_query ='''
    SELECT *
    FROM latam_datasets.h2h_brazil_corn
    '''
    data1= pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    data2=data1[data1['Variable'] == "YLD"]
    data2=data2[data2['Macroregion'] == "ALL"]
    data2=data2[data2['Year'] == "ALL"]
    data2=data2[data2['Protocol'] == "FTN"]
    data2['Head_mean']=data2['Head_mean']*100
    data2['diffmean']=data2['diffmean']*100

    descricao1 = pd.read_csv('/domino/datasets/local/MD/dadosparafiltro.csv')
    descricao1['Head']=(descricao1['Product']+descricao1['Biotecnologias_disponiveis'])
    descricao1=descricao1.drop(columns=['Biotecnologias_disponiveis'])

    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Winter","Subtropical Winter Winter")
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace("Subtropical Summer","Subtropical Summer Summer")

    #lista=lista.rename(columns ={'brand':'Head_brand'})
    descricao1=descricao1.rename(columns ={'situacao':'Head_situacao'})
    descricao1=descricao1.rename(columns ={'Product':'Head_p'})
    descricao1['Marca']=descricao1['Marca'].str.upper()
    lista=descricao1
    lista=lista.rename(columns ={'Marca':'Head_brand'})

    data21=pd.merge(data2, lista, how = 'inner', on = ['Head','Pipeline'])
    lista=lista.rename(columns ={'Head':'Other'})
    lista=lista.rename(columns ={'Head_brand':'Other_brand'})
    lista=lista.rename(columns ={'Head_situacao':'Other_situacao'})
    lista=lista.rename(columns ={'Head_p':'Other_p'})
    datafinal=pd.merge(data21, lista, how = 'inner', on = ['Other','Pipeline'])
    dfremove=datafinal[datafinal['Head_p']==datafinal['Other_p']] 
    datafinal=datafinal.drop(dfremove.index)
    dtafinalbay=datafinal[datafinal['Head_brand']=="BAYER"]
    dtafinaldk=datafinal[datafinal['Head_brand']=="DEKALB"]
    index_dk=datafinal[datafinal['Head_brand']=="DEKALB"].index
    datafinal=datafinal.drop(index_dk)
    dtafinalas=datafinal[datafinal['Head_brand']=="AGROESTE"]
    index_as=datafinal[datafinal['Head_brand']=="AGROESTE"].index
    datafinal=datafinal.drop(index_as)
    dtafinalag=datafinal[datafinal['Head_brand']=="AGROCERES"]
    index_ag=datafinal[datafinal['Head_brand']=="AGROCERES"].index
    datafinal=datafinal.drop(index_ag)
    index_dk=dtafinaldk[(dtafinaldk['Other_brand']=="AGROESTE") | (dtafinaldk['Other_brand']=="AGROCERES")].index
    dtafinaldk=dtafinaldk.drop(index_dk)
    index_ag=dtafinalag[(dtafinalag['Other_brand']=="AGROESTE") | (dtafinalag['Other_brand']=="DEKALB")].index
    dtafinalag=dtafinalag.drop(index_ag)
    index_as=dtafinalas[(dtafinalas['Other_brand']=="AGROCERES") | (dtafinalas['Other_brand']=="DEKALB")].index
    dtafinalas=dtafinalas.drop(index_as)
    datafinal1=pd.concat([ dtafinaldk, dtafinalag,dtafinalas,dtafinalbay])
    datafinal1=datafinal1[(datafinal1['Head_situacao']== "ativo") | (datafinal1['Head_situacao'] == "Lançamento")] 
    datafinal1['percent_loss']=(100-datafinal1['percent_wins'])

    datafinal1= datafinal1[["Pipeline","EI","Head","Other","n","pvalue","Head_mean","Other_mean","diffmean","number_wins","percent_wins","percent_loss"]]
    datafinal1=datafinal1.sort_values(['Head'])
    datafinal1['Pipeline']=datafinal1['Pipeline'].str.replace("Subtropical Summer Summer","Subtropical Summer")
    datafinal1['Pipeline']=datafinal1['Pipeline'].str.replace("Subtropical Winter Winter","Subtropical Winter")
    datafinal1['Pipeline']=datafinal1['Pipeline'].str.replace(' ','_')
    datafinal1.to_csv('H2H_final0223a.csv',index = False)
    h2hfinal = datafinal1
    #h2hfinal.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_H2H',
                            #if_exists = 'replace')
    return h2hfinal

def filtradoencas():     
    tabela1 = pd.read_csv('/domino/datasets/local/MD/doecasmcompleta.csv')
    tabela1=tabela1.loc[tabela1['Status'] != "old"]     
    tabela1=tabela1.loc[(tabela1['situacao'] == "ativo") | (tabela1['situacao'] == "Lançamento")]   
    data_dados=tabela1.drop_duplicates()   
    data_dados=data_dados.iloc[:,0:15] 
    data_dados['Pipeline']=data_dados['Pipeline'].str.replace(' ','_')
    data_dados=data_dados.drop_duplicates()
    data_dados.to_csv('Diseases_Tablea.csv',index = False)
    Diseases_Table=data_dados
    Diseases_Table.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_Diseases_Table',
                            if_exists = 'replace')
    return Diseases_Table
def notadohibrido(): 
    tabela1 = pd.read_csv('/domino/datasets/local/MD/notedescrip1.csv')
    tabela1=tabela1.loc[tabela1['Status'] != "old"]      
    tabela1=tabela1.loc[(tabela1['situacao'] == "ativo") | (tabela1['situacao'] == "Lançamento")]   
    data_dados=tabela1.drop_duplicates()
    data_dados=data_dados.iloc[:,0:27]     
    data_dados['Pipeline']=data_dados['Pipeline'].str.replace(' ','_')
    data_dados=data_dados.drop_duplicates()
    data_dados.to_csv('Hybrid_Descriptiona.csv',index = False)
    hybrid_descript=data_dados
    hybrid_descript.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_Hybrid_Description',
                            if_exists = 'replace')
    
    return hybrid_descript
def nderc(): 
    tabela1 = pd.read_csv('/domino/datasets/local/MD/DEREC_NREC2.csv')
    tabela1.rename(columns = {'EI (kg/ha)': 'EI_kg_ha', 'DREC (plantas/m2)': 'DREC_plantas_m2'}, inplace = True)  

    
    tabela1.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_DEREC_NREC',
                            if_exists = 'replace')
    
    return tabela1

def agronomicrisk():
    bq_query = '''
    SELECT *
    FROM latam_datasets.hss_brazil_historical_corn
    WHERE OBS_observationRefCd IN ('YLD','MST','S50D','P50D','EHT','PHT','TKW') AND
    protocolType IN ('FTN') AND
    QC_Flag is null
    '''
    #carrega o banco atual
    data_historical=pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    bq_query ='''
    SELECT *
    FROM latam_datasets.hss_brazil_current_corn
    WHERE OBS_observationRefCd IN ('YLD','MST','S50D','P50D','EHT','PHT','TKW') AND
    protocolType IN ('FTN') AND
    QC_Flag is null
    '''
    data_current=pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
    data_historical['OBS_descriptorAbbreviation'].fillna('N/A', inplace=True) 
    data_current['OBS_descriptorAbbreviation'].fillna('N/A', inplace=True) 
    data_historical['OBS_code']=(data_historical['OBS_observationRefCd'] + "." + data_historical['OBS_descriptorAbbreviation'])
    data_current['OBS_code']=(data_current['OBS_observationRefCd'] + "." + data_current['OBS_descriptorAbbreviation'])
    data_current=data_current.drop(columns=['OBS_observationRefCd'])
    data_current=data_current.drop(columns=['OBS_descriptorAbbreviation'])
    data_historical=data_historical.drop(columns=['OBS_observationRefCd'])
    data_historical=data_historical.drop(columns=['OBS_descriptorAbbreviation'])
    data_current=data_current.drop(columns=['midas_germplasm_id'])
    data_historical=data_historical.drop(columns=['midas_germplasm_id'])
    a = data_historical.columns.values.tolist()
    data_historical['OBS_code']=data_historical['OBS_code'].replace("PHT.R1","PHT.N/A")
    data_historical['OBS_code']=data_historical['OBS_code'].replace("PHT.VT","PHT.N/A")
    code=["TKW.N/A","EHT.N/A","MST.N/A","YLD.N/A","S50D.N/A","PHT.N/A","P50D.N/A"]
    data_current=data_current.loc[data_current['OBS_code'].isin(code)]
    data_historical=data_historical.loc[data_historical['OBS_code'].isin(code)]
        #data_current=data_current.loc[a]
    brazil_nonpivot=pd.concat([data_current, data_historical])
    brazil_nonpivot['new_pipeline']=(brazil_nonpivot['FIELD_pipeline']+"_"+brazil_nonpivot['FIELD_seasonName'])
    brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace(' ','_')
    brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace("Tropical_Lowlands_Summer","Tropical_Highlands_Summer")
        #brazil_nonpivot['new_pipeline']= brazil_nonpivot['new_pipeline'].str.replace('_',' ')
    descricao1 = pd.read_csv('/domino/datasets/local/MD/dadosparafiltro.csv')
    descricao1['commercialName']=(descricao1['Product']+descricao1['Biotecnologias_disponiveis'])
    descricao1=descricao1.drop(columns=['Biotecnologias_disponiveis'])
    descricao1=descricao1.drop(columns=['Marca'])
    descricao1['Pipeline']=descricao1['Pipeline'].replace("Subtropical Winter","Subtropical Winter Winter")
    descricao1['Pipeline']=descricao1['Pipeline'].replace("Subtropical Summer","Subtropical_Summer_Summer")
    descricao1['Pipeline']=descricao1['Pipeline'].str.replace(' ','_')
    descricao1=descricao1.rename(columns={'Pipeline': 'new_pipeline'})
    brazil_nonpivot=pd.merge(descricao1,brazil_nonpivot, how = 'left', on = ['commercialName','new_pipeline']) 
    brazil_nonpivot=brazil_nonpivot[(brazil_nonpivot['situacao']== "ativo") | (brazil_nonpivot['situacao'] == "Lançamento")]    
    descricao1=descricao1.loc[(descricao1['situacao'] == "ativo") | (descricao1['situacao'] == "Lançamento")]
    safra1=descricao1['new_pipeline'].unique()
    safra=safra1.tolist()
    dffinal=descricao1
    fdf =dffinal
    nomes = fdf['commercialName'].tolist()
    pipeline = fdf['new_pipeline'].unique().tolist()    
            # faz a união de dois frames

            #Filtrando final
    lista_final=(fdf['commercialName'].tolist())
    pipes=safra
    data3=brazil_nonpivot
    data4=data3
    data4=brazil_nonpivot    
    data4=data4.loc[(data4['OBS_code'] == "YLD.N/A") ]
    output1 = pd.DataFrame()
    for o in range(len(pipeline)):
        dados1=data4[data4['new_pipeline']==pipeline[o]] 
        eirgf = dados1['EIRange'].unique()
        eirgb=[not pd.isnull(number) for number in eirgf]
        eirg = eirgf[eirgb]
        for s in range(len(eirg)):
            dados2=dados1.loc[dados1['EIRange']==eirg[s]]
            temp=dados2.groupby(['Product','new_pipeline','FIELD_plantingSeason','UniqueName','FIELD_name']).mean(['OBS_numValue'])
            temp.reset_index(inplace=True)
            temp2 = pd.DataFrame()
            temp2=temp[['Product','new_pipeline']]
            temp2['yld_calc'] = temp['OBS_numValue'] - temp['EI']
            temp2['positive']=temp2['yld_calc'].apply(lambda x: 0 if x <0 else 1)
            temp2['npositive']=temp2.groupby('Product')['positive'].transform('sum')
            temp2['ndata']=temp2.groupby('Product')['Product'].transform('count')
            temp2['prop_win']=(temp2['npositive'] / temp2['ndata'])*100
            temp2['prop_win']=temp2['prop_win'].round(2)
            temp2['EIRange']=eirg[s]
            temp2['averageEI']=temp.groupby('Product')['EI'].transform('mean')
            output1=pd.concat([output1,temp2])

    #output1.to_csv('agronomictotal.csv',index = False)
    output2=output1[['Product','new_pipeline','npositive','prop_win','EIRange','averageEI']]
    output2=output2.drop_duplicates()
    output2['new_pipeline']=output2['new_pipeline'].str.replace('_',' ')
    output2['new_pipeline']=output2['new_pipeline'].str.replace("Subtropical Winter Winter","Subtropical Winter")
    output2['new_pipeline']=output2['new_pipeline'].str.replace("Subtropical Summer Summer","Subtropical Summer")
    output2['new_pipeline']=output2['new_pipeline'].str.replace(' ','_')
    output2.reset_index(inplace=True)
    output2=output2.drop(columns=['index'])
    output2=output2.drop_duplicates()
    output2.to_csv('agronomicrisk.csv',index = False)
    agronomicrisk=output2
    agronomicrisk.to_gbq(project_id = bq_proj, credentials = bq_credentials,destination_table = 'bcs-market-dev-lake.latam_md_corn.BRA_T_Agronomicrisk',
                            if_exists = 'replace')   
    
    return agronomicrisk

def  geraplanilha()
    listas=['''Diseases_Table''','''DEREC_NREC''','''Hybrid_Description''','''Fenotype''','''Agronomicrisk''','''m_b_Cultivio_Brands''','''Stability_Cultivio_Brands''','''H2H''','''Crop_Monitoring''','''TT_cumulative''']
    w=pd.ExcelWriter("/domino/datasets/local/salvar_arquivos/arquivo_para_md.xlsx")

    for lista in listas:
         bq_query = '''
         SELECT *
         FROM bcs-market-dev-lake.latam_md_corn.BRA_T_'''+ lista 

         df=pd.read_gbq(bq_query, project_id = bq_proj, credentials = bq_credentials, use_bqstorage_api = True)
         nome=str(lista)
         print(nome)
         df.to_excel(w,sheet_name=nome,index=False)
    df=pd.read_csv('/domino/datasets/local/MD/comparativo.csv')    
    df.to_excel(w,sheet_name='comparativo',index=False)    
    w.save() 
    return df