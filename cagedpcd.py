import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, render_template_string, redirect, url_for, request
import numpy as np
import matplotlib.pyplot as plt
import plotly.io
import seaborn as sns
import os
import numpy as np
app = Flask(__name__)


def eixocity():
    data = pd.read_excel('cidade.xlsx')
    lista = []
    for campo in data['cidade'].values:
        lista.append(campo)
    listaCombo = np.array(lista)
    return listaCombo
def eixouf():
    data = pd.read_excel('uf.xlsx')
    lista = []
    for campo in data['estados'].values:
        if campo.strip():
         lista.append(campo)
    listaCombo = np.array(lista)
    return listaCombo
def eixoregiao():
    data = pd.read_excel('regiao.xlsx')
    lista = []
    for campo in data['regiao'].values:
        if campo.strip():
            lista.append(campo)
    listaCombo = np.array(lista)
    return listaCombo

def eixocargos():
    data = pd.read_excel('CBO2002excel.xlsx')
    data.columns = data.columns.str.replace(' ', '')
    lista = []
    for campo in data['TITULO'].values:
        if campo.strip():
            lista.append(campo)
    listaCombo = np.array(lista)
    return listaCombo

def get_plot_pie(acao,wmes,wano,wopcaox,wcombotxt):
    meszero = ''
    rotape = wopcaox
    wtabelaum = ''
    if acao == 'Admissão':
        GK_roi = pd.read_excel('admpcd2023.xlsx')
        if wmes != 'Todos':
           #df_adm = dfpcd.loc[(dfpcd['tipodedeficiência'] !=0) & (dfpcd['tipomovimentação']>31)]
           df_adm = GK_roi.loc[(GK_roi['mes'] == int(wmes)) & (GK_roi['ano'] == int(wano))]
        else:
            df_adm = GK_roi.loc[(GK_roi['ano'] == int(wano))]

    else:
        GK_roi = pd.read_excel('dempcd2023.xlsx')
        if wmes != 'Todos':
           #df_adm = dfpcd.loc[(dfpcd['tipodedeficiência'] !=0) & (dfpcd['tipomovimentação']>31)]
           df_adm = GK_roi.loc[(GK_roi['mes'] == int(wmes)) & (GK_roi['ano'] == int(wano))]
        else:
            df_adm = GK_roi.loc[(GK_roi['ano'] == int(wano))]
    if wmes != 'Todos':
        if int(wmes) < 10:
          meszero = '0'
        else:
            wmes = ''
            meszero = ''

    ###df = df_adm.loc[(df_adm[wtabelaum] == wcombotxt)]
    data = pd.read_excel('cor01023.xlsx')
    labels = data['legenda']
    values = data['raçacor']

    # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
    figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return df_adm

#============================================================================================================

def get_plot(wmenu,wtitulo,acao,wmes,wano,wopcaox):
    meszero = ''
    rotape = wopcaox
    wtabelaum = ''

    if acao == 'Admissão':
     # from GetFixtures2 import GK_roi
        GK_roi = pd.read_excel('admpcd2023.xlsx')
        if wmes != 'Todos':
           #df_adm = dfpcd.loc[(dfpcd['tipodedeficiência'] !=0) & (dfpcd['tipomovimentação']>31)]
           df_adm = GK_roi.loc[(GK_roi['mes'] == int(wmes)) & (GK_roi['ano'] == int(wano))]
        else:
            df_adm = GK_roi.loc[(GK_roi['ano'] == int(wano))]

    else:
        GK_roi = pd.read_excel('dempcd2023.xlsx')
        if wmes != 'Todos':
           #df_adm = dfpcd.loc[(dfpcd['tipodedeficiência'] !=0) & (dfpcd['tipomovimentação']>31)]
           df_adm = GK_roi.loc[(GK_roi['mes'] == int(wmes)) & (GK_roi['ano'] == int(wano))]
        else:
            df_adm = GK_roi.loc[(GK_roi['ano'] == int(wano))]
    if wmes != 'Todos':
        if int(wmes) < 10:
          meszero = '0'
        else:
            wmes = ''
            meszero = ''

    if rotape == '01':
        wtabelaum = 'estados'
        #if wcombo != 'Estados':
            #df_adm = df_adm.loc[(df_adm['estados'] == wcombo)]
    if rotape == '02':
        wtabelaum = 'regiao'
    if rotape == '03':
        wtabelaum = 'cidade'
    if rotape == '04':
        wtabelaum = 'TITULO'

    country_type_counts = df_adm.groupby([wtabelaum, wmenu]).size().unstack().fillna(0)
  #  if wopcaox == '02':
  #    country_type_counts = df_adm.groupby(['regiao', wmenu]).size().unstack().fillna(0)

    # Calculando contagens totais para cada país para encontrar os 10 primeiros
    if rotape == '01' or rotape == '02':
        top_countries = country_type_counts.sum(axis=1).sort_values(ascending=False)
    if rotape == '03' or rotape == '04':
        top_countries = country_type_counts.sum(axis=1).sort_values(ascending=False).head(20)

    # Filtrando dados para incluir apenas os estados
    top_country_data = country_type_counts.loc[top_countries.index]

    # Calculando porcentagem
    top_country_data_percentage = top_country_data.div(top_country_data.sum(axis=1), axis=0) * 100
#https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
    cm = 1 / 2.54
    fig, ax = plt.subplots(figsize=(10, 8))
    #fig.subplots_adjust

    #fig.subplots_adjust(right=0.8)
    top_country_data_percentage.plot(kind='bar', stacked=True, ax=plt.gca())

    #plt.figure(figsize=(10, 6))
    if rotape == '01' or rotape == '02':
        plt.title(str(acao)+' de PCD por '+str(wtabelaum)+' do Brasil\n'
              'com porcentagem por '+str(wtitulo) + ' - CAGED BRASIL '+str(meszero)+str(wmes)+' / ' +wano)
    if rotape == '03' or rotape == '04':
        plt.title(str(acao)+' de PCD dos(das) 20 maiores '+str(wtabelaum)+' do Brasil\n'
              'com porcentagem por '+str(wtitulo) + ' - CAGED BRASIL '+str(meszero)+str(wmes)+' / ' +wano)


    plt.xlabel(wtabelaum)
    plt.ylabel('Porcentagem')
    plt.legend(title=wtitulo, labels=country_type_counts)
    plt.xticks(rotation=90, ha='right', fontsize=10)
    fig.tight_layout() #isso resolveu o tamanho da figura
    return fig

@app.route('/')
@app.route('/', methods=['GET','POST'])
def home():
    reglist    = eixoregiao()
    uflist     = eixouf()
    citylist   = eixocity()
    cargolist  = eixocargos()
    return render_template('visual.html',reglist=reglist,uflist=uflist,citylist=citylist,cargolist=cargolist)
@app.route('/result',methods = ['POST', 'GET'])
def result():

   if request.method == 'POST':
      combotxt = ''
      result = request.form
      nivel = request.form.get('options')
      status = request.form.get('demi')
      mes = request.form.get('mes')
      ano = request.form.get('ano')
      opcaox = request.form.get('comboregiao')
      comboum = request.form.get("estad")
      combodois = request.form.get("reg")
      combotres = request.form.get("cid")
      comboquatro = request.form.get("carg")

      afazer = ''
      tabela = ''
      if opcaox == '01':
          combotxt = comboum
          campo   = 'estados'
      if opcaox == '02':
          combotxt = combodois
          campo = 'regiao'
      if opcaox == '03':
          combotxt = combotres
          campo = 'cidade'
      if opcaox == '04':
          combotxt = comboquatro
          campo = 'TITULO'

      if nivel == 'Cor':# and combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
          if  combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
            plot = get_plot('cor', 'Cor - Raça',status,mes,ano,opcaox)

          # Save the figure in the static directory

            plot.savefig(os.path.join('static', 'plot.png'))

          #recupera opções
            reglist = eixoregiao()
            uflist = eixouf()
            citylist = eixocity()
            cargolist = eixocargos()

            return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
          else:
              titulo = (str(status)+' de PCD --> '+str(combotxt)+' por COR\n'
              'CAGED BRASIL - '+str('Período:')+str(mes)+' / ' +ano)

              data = get_plot_pie(status,mes,ano,opcaox,combotxt) # pd.read_excel('cor01023.xlsx')
              data = data.loc[(data[campo] == combotxt)]
              labels = data['cor']
              values = data['raçacor']
              reglist = eixoregiao()
              uflist = eixouf()
              citylist = eixocity()
              cargolist = eixocargos()
              # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
              figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
              return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist,titulo=titulo)

      #diferente de estado,regiões,cidades e cargos

      #fim cor

      if nivel == 'Tipo de Deficiência':# and combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
          if combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
            plot = get_plot('defic_x', 'Tipo de Deficiência',status,mes,ano,opcaox)

           # Save the figure in the static directory

            plot.savefig(os.path.join('static', 'plot.png'))

            reglist = eixoregiao()
            uflist = eixouf()
            citylist = eixocity()
            cargolist = eixocargos()
            return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
          else:
               titulo = (str(status) + ' de PCD --> ' + str(combotxt) + ' por Tipo de Deficiência\n'
               'CAGED BRASIL - ' + str('Período:') + str(mes) + ' / ' + ano)

               data = get_plot_pie(status, mes, ano, opcaox, combotxt)  # pd.read_excel('cor01023.xlsx')
               data = data.loc[(data[campo] == combotxt)]
               labels = data['defic_x']
               values = data['tipodedeficiência']
               reglist = eixoregiao()
               uflist = eixouf()
               citylist = eixocity()
               cargolist = eixocargos()
            # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
               figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
               return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist, citylist=citylist,
                                   cargolist=cargolist, titulo=titulo)

      if nivel == 'Nível Escolar':# and combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
          if combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
            plot = get_plot('curso','Nível Escolar',status,mes,ano,opcaox)

          # Save the figure in the static directory

            plot.savefig(os.path.join('static', 'plot.png'))

            reglist = eixoregiao()
            uflist = eixouf()
            citylist = eixocity()
            cargolist = eixocargos()
            return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
          else:
               titulo = (str(status) + ' de PCD --> ' + str(combotxt) + ' por Nível Escolar\n'
                                                                       'CAGED BRASIL - ' + str('Período:') + str(
                  mes) + ' / ' + ano)

               data = get_plot_pie(status, mes, ano, opcaox, combotxt)  # pd.read_excel('cor01023.xlsx')
               data = data.loc[(data[campo] == combotxt)]
               labels = data['curso']
               values = data['graudeinstrução']
               reglist = eixoregiao()
               uflist = eixouf()
               citylist = eixocity()
               cargolist = eixocargos()
              # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
               figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
               return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist,
                                     citylist=citylist,
                                     cargolist=cargolist, titulo=titulo)

      if nivel == 'Faixa Etária':
         #### data = pd.read_excel('cor01023.xlsx')
         #### labels = data['legenda']
         #### values = data['raçacor']

          # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
         #### figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
         #### return render_template("pie.html", plot=figura.to_html())
         if combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
           plot = get_plot('faixa','Faixa Etária',status,mes,ano,opcaox)

          # Save the figure in the static directory

           plot.savefig(os.path.join('static', 'plot.png'))

           reglist = eixoregiao()
           uflist = eixouf()
           citylist = eixocity()
           cargolist = eixocargos()
           return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
         else:
              titulo = (str(status) + ' de PCD --> ' + str(combotxt) + ' por Faixa Etária\n'
                                                                      'CAGED BRASIL - ' + str('Período:') + str(
                 mes) + ' / ' + ano)

              data = get_plot_pie(status, mes, ano, opcaox, combotxt)  # pd.read_excel('cor01023.xlsx')
              data = data.loc[(data[campo] == combotxt)]
              labels = data['faixa']
              values = data['idade']
              reglist = eixoregiao()
              uflist = eixouf()
              citylist = eixocity()
              cargolist = eixocargos()
             # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
              figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
              return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist,
                                    citylist=citylist,
                                    cargolist=cargolist, titulo=titulo)

      if nivel == 'Faixa Salarial':
          if combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
            plot = get_plot('faixasal','Faixa Salarial',status,mes,ano,opcaox)

          # Save the figure in the static directory

            plot.savefig(os.path.join('static', 'plot.png'))
            reglist = eixoregiao()
            uflist = eixouf()
            citylist = eixocity()
            cargolist = eixocargos()
            return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
          else:
               titulo = (str(status) + ' de PCD --> ' + str(combotxt) + ' por Faixa Salarial\n'
                                                                       'CAGED BRASIL - ' + str('Período:') + str(
                  mes) + ' / ' + ano)

               data = get_plot_pie(status, mes, ano, opcaox, combotxt)  # pd.read_excel('cor01023.xlsx')
               data = data.loc[(data[campo] == combotxt)]
               labels = data['faixasal']
               values = data['estados']
               reglist = eixoregiao()
               uflist = eixouf()
               citylist = eixocity()
               cargolist = eixocargos()
              # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
               figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
               return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist,
                                     citylist=citylist,
                                     cargolist=cargolist, titulo=titulo)

      if nivel == 'Sexo':
          if combotxt == 'Estados' or combotxt == 'Regiões' or combotxt == 'Cidades' or combotxt == 'Cargos':
            plot = get_plot('legenda','Sexo',status,mes,ano,opcaox)

          # Save the figure in the static directory

            plot.savefig(os.path.join('static', 'plot.png'))

            reglist = eixoregiao()
            uflist  = eixouf()
            citylist = eixocity()
            cargolist = eixocargos()
            return render_template('visual.html', reglist=reglist, uflist=uflist, citylist=citylist, cargolist=cargolist)
          else:
               titulo = (str(status) + ' de PCD --> ' + str(combotxt) + ' por Sexo\n'
                                                                       'CAGED BRASIL - ' + str('Período:') + str(
                  mes) + ' / ' + ano)

               data = get_plot_pie(status, mes, ano, opcaox, combotxt)  # pd.read_excel('cor01023.xlsx')
               data = data.loc[(data[campo] == combotxt)]
               labels = data['legenda']
               values = data['sexo']
               reglist = eixoregiao()
               uflist = eixouf()
               citylist = eixocity()
               cargolist = eixocargos()
              # fig = go.Figure([go.Bar(x=data['pcd'], y=data['tipodedeficiência'])])
               figura = go.Figure(data=[go.Pie(labels=labels, values=values)])
               return render_template("pie.html", plot=figura.to_html(), reglist=reglist, uflist=uflist,
                                     citylist=citylist,
                                     cargolist=cargolist, titulo=titulo)


      elif nivel != 'Cor' or nivel != 'Tipo de Deficiência' or nivel != 'Nível Escolar':
            afazer = 'Em Desenvolvimento - FRONT END'
            return render_template("visual.html", afazer=afazer, nivel=nivel)


if __name__ == '__main__':
    app.run(debug=True)