# importando blibliotecas que serão utilizadas #
import builtins
from logging import _STYLES 
from os import path
from time import sleep
from numpy import select
import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px
from streamlit.legacy_caching.caching import cache
from streamlit.proto.PlotlyChart_pb2 import Figure
from web_scrapping import iee_b3, import_ibov, import_ind

#--------------------------------------------------------------#
# variaveis #

indicadores = ['DY', 'PL', 'PEG_RATIO', 'P_PV', 'EV_EBITIDA', 'EV_EBIT', 'P_EBITIDA', 'P_EBIT',
               'VPA', 'P_ATIVO', 'LPA', 'S_SR', 'P_CAP_GIRO', 'P_ATIVO_CIRC_LIQ', 'DIV_LIQUIDA_PL',
               'DIV_LIQUIDA_EBITIDA', 'DIV_LIQUIDA_EBIT', 'PL_ATIVOS', 'PASSIVOS_ATIVOS', 'LIQ_CORRENTE',
               'M_BRUTA', 'M_EBITIDA', 'M_EBIT', 'M_LIQUIDA', 'ROE', 'ROA', 'ROIC', 'GIRO_ATIVOS',
               'CAGR_RECEITAS_5_ANOS', 'CAGR_LUCROS_5_ANOS']
iee = iee_b3()
start_date = datetime.today()-timedelta(days=30) # data de inicio para o grafico de candle  no caso diminuiu 30 dias # 
end_date = datetime.today()  
intervals = ['Daily', 'Weekly', 'Monthly']
dash = ['Dash 1','Dash 2','Dash 3']
intervals = ['Daily', 'Weekly', 'Monthly']
carregar_dados = 0
newDash = st.sidebar.selectbox('Selecione o  Dash', dash) # newDash recebe um seletor de caixa  #
formatacao1 = st.sidebar.markdown("---")

#---------------------------------------------------#
#   Funções   para graficos e pizza etc...        #
#  função definida para plotar grafico de candle  #

def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1] 
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


# ------------------------------------------------------- #
def Dash_2(iee):
    st.sidebar.title('Menu 📰 De Notícias  ') # 
    st.sidebar.markdown('---')
    st.title('  Dash 2 ')
    st.markdown('---')
    
    #stock_select_side = st.sidebar.selectbox("Selecione o ativo:" )
    
    col1,col2,= st.columns(2)
    container2 = st.container()
    col_side1, col_side2, col_side3 = st.sidebar.columns(3)

    
    container3 = st.container()
    container4 = st.container()
    
    #df1, df2 = import_ind(stock_select_side)
    with col1:
        from_date = st.date_input('De:', start_date)  
    with col2:
        to_date = st.date_input('Para:', end_date)
    
    #stock_selec = st.sidebar.selectbox('Escolha a ação')
    #colunas dos valores #
    with container3:
        with col_side1: # Coluna sidebar 1#
            st.metric(label="Price", value=df2.loc[0][1], delta='',delta_color="inverse")
            st.metric("Wind", "9", "-8%")
            st.metric("Wind", "9", "-8%")
            st.metric(label="Price", value=4, delta=-0.5,delta_color="inverse")
            

        with col_side2: # Coluna sidebar 2 #
            st.metric(label="Vale3", value='12%', delta=123,delta_color="off")
            st.metric("Wind", "15", "+8%")
            st.metric("Wind", "9", "-8%")
            st.metric(label="Price", value=4, delta=-0.5,delta_color="inverse")
            
        with col_side3: # Coluna sidebar 3#
            st.metric(label="Wind", value=9, delta='-16%', delta_color="off")
            st.metric("Wind", "17", '8%')
            st.metric(label="Price", value=4, delta=-0.5,delta_color="inverse")
    
            
    #with container4:
    #    with col_side4:
    #        st.metric("Wind", "9", "-8%")
    #    with col_side5:
    #        st.metric("Wind", "15", "+8%")
    #    with col_side6:
    #        st.metric("Wind", "17", '8%')
    
    with container2:
        st.markdown('---')
        stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa])
        df1,df2 = import_ind(iee[iee.Empresa == stock_select].loc[0][1])
        #interval_select = st.selectbox("Selecione o timeframe:", intervals)
        #grafico#
    
    if from_date > to_date:
        st.error('Data de ínicio maior do que data final')
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), 'Daily')
        try : 
            fig = Graftest(df)
            grafico_candle = st.plotly_chart(fig, use_container_width=True) 
            st.markdown('---')
        except Exception as e:
            st.error(e)  
    st.dataframe(df)

    
#----------------------------------------------------------------#

def dash_3():
    
    st.markdown(' ## Novo Dash 3 - Gráficos')
    c = st.container()
    c.markdown(' # Grafico 1')
    c.markdown(' # Grafico 2')
    c.markdown(' # Grafico 3')


#------------------------------------------------------------------#


# ---------------------------int main () --------------------------------#
if newDash == 'Dash 2' :
    Dash_2(iee) # Função Dash 2#
elif newDash == 'Dash 3':
    dash_3()    # Função Dash 3
#   Caso contrario motrar o dash 1   #    
else:
    barra_lateral = st.sidebar.title('Menu 🌫️   ')
    barra_lateral = st.sidebar.empty()
    formatacao1   = st.sidebar.markdown("---")
    
    stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa]) # stock select recebe um seletor de ativo  # 
    formatacao13   = st.markdown("---")
    from_date = st.sidebar.date_input('De:', start_date)  
    to_date = st.sidebar.date_input('Para:', end_date)
    interval_select = st.sidebar.selectbox("Selecione o timeframe:", intervals)
    formatacao2 = st.sidebar.markdown("---")
    grafico_line = st.empty()   #Grafico de linha  recebendo vazio   #
    grafico_candle = st.empty() #Grafico de candle recebendo vazio   #
    grafico_pizza = st.empty()  # grafico de pizza recebendo vazio    #
    if from_date > to_date: #    Se from data for maior que to date     #
        st.sidebar.error('Data de ínicio maior do que data final') 
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), interval_select) #  dataframa recebe a função consultar ação com da iee  com as datas selecionada  # 
        try:
            fig = plotCandleStick(df) # fig recebe a função que mostra o grafico de 
            figpizza = sun_b(stock_select)  # figurapizza com a variavel stock_select que foi selecionada pelo usuario  #
            
            grafico_pizza = st.plotly_chart(figpizza, use_container_width=True) # Grafico de pizza usando a variavel figpizza em que o dataframe foi transformado em figura#

            #grafico_line = st.line_chart(df.Close)  #pegando apenas os dados de df.Close para usar no grafico de linhas#

            container = st.container() 
            with container:
                grafico_candle = st.plotly_chart(fig, use_container_width=True)     # plotando o grafico de candle  #
                carregar_dados = st.sidebar.checkbox('Carregar Dados')  #  caixa de carregar dados  #

            if carregar_dados == 1:  #Se carregar dados for True então faça#
                st.subheader('Dados')
                dados = st.dataframe(df) #Mostra o dataframe de df com seus especificos dados #
                stock_select = st.sidebar.checkbox #    #

        except Exception as e:
            st.error(e)  

