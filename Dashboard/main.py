from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

app = Dash(__name__)

current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, 'Vendas.xlsx')
df = pd.read_excel(file_path)


opcoes_lojas = list(df['ID Loja'].unique())
opcoes_lojas.append("Todas as Lojas")

#Tipos de gráficos
tipos_graficos = ["Barra", "Colunas", "Pizza", "Rosca"]

#Layout do dashboard
app.layout = html.Div(style={
    'backgroundColor': '#f4f4f9', 'padding': '30px', 'fontFamily': 'Arial, sans-serif'
}, children=[

    html.H1(children='Faturamento das Lojas', style={
        'textAlign': 'center', 'color': '#333', 'fontSize': '36px', 'fontWeight': 'bold', 'marginBottom': '20px'
    }),

    html.H2(children='Gráfico com o Faturamento de Todos os Produtos Separados por Loja', style={
        'textAlign': 'center', 'color': '#666', 'fontSize': '24px', 'marginBottom': '20px'
    }),


    html.Div([
        html.Label("Selecione a Loja", style={'fontSize': '18px', 'color': '#333', 'marginBottom': '10px'}),
        dcc.Dropdown(
            opcoes_lojas,
            value='Todas as Lojas',
            id='lista_lojas',
            style={
                'width': '50%', 'margin': '0 auto', 'fontSize': '18px', 'backgroundColor': '#f8f8f8',
                'borderRadius': '8px', 'border': '1px solid #ddd', 'padding': '10px'
            }
        ),
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.Label("Selecione o Tipo de Gráfico", style={'fontSize': '18px', 'color': '#333', 'marginBottom': '10px'}),
        dcc.Dropdown(
            tipos_graficos,
            value='Barra',
            id='tipo_grafico',
            style={
                'width': '50%', 'margin': '0 auto', 'fontSize': '18px', 'backgroundColor': '#f8f8f8',
                'borderRadius': '8px', 'border': '1px solid #ddd', 'padding': '10px'
            }
        ),
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    dcc.Graph(
        id='grafico_quantidade_vendas',
        style={'borderRadius': '12px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
    ),

    html.Div(id='info_faturamento', style={
        'textAlign': 'center', 'color': '#333', 'fontSize': '18px', 'marginTop': '20px'
    })
])

@app.callback(
    [Output('grafico_quantidade_vendas', 'figure'),
     Output('info_faturamento', 'children')],
    [Input('lista_lojas', 'value'),
     Input('tipo_grafico', 'value')]
)
def update_output(loja_selecionada, tipo_grafico):
    if loja_selecionada == "Todas as Lojas":
        dados = df
    else:
        dados = df[df['ID Loja'] == loja_selecionada]

    #Calculao dos faturamentos
    dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']
    faturamento_total = dados['Faturamento'].sum()
    faturamento_por_produto = dados.groupby('Produto')['Faturamento'].sum()

    info_faturamento = [
        html.P(f"Faturamento Total (R$): {faturamento_total:,.2f}", style={'marginBottom': '10px'}),
        html.P("Faturamento por Produto:", style={'marginBottom': '5px'}),
    ]
    info_faturamento.extend([
        html.P(f"- {produto}: R$ {valor:,.2f}") for produto, valor in faturamento_por_produto.items()
    ])

    if tipo_grafico == "Barra":
        if loja_selecionada == "Todas as Lojas":
            fig = px.bar(dados, x="Produto", y="Quantidade", color="ID Loja", barmode="group", 
                         color_discrete_sequence=px.colors.qualitative.Set1)
        else:
            fig = px.bar(dados, x="Produto", y="Quantidade", color="Produto", barmode="group", 
                         color_discrete_sequence=px.colors.qualitative.Set2)
    elif tipo_grafico == "Colunas":
        if loja_selecionada == "Todas as Lojas":
            fig = px.bar(dados, x="Produto", y="Quantidade", color="ID Loja", barmode="stack", 
                         orientation='v', color_discrete_sequence=px.colors.qualitative.Set3)
        else:
            fig = px.bar(dados, x="Produto", y="Quantidade", color="Produto", barmode="stack", 
                         orientation='v', color_discrete_sequence=px.colors.qualitative.Set3)
    elif tipo_grafico == "Pizza":
        fig = px.pie(dados, names="Produto", values="Quantidade", 
                     color_discrete_sequence=px.colors.qualitative.Set1)
    elif tipo_grafico == "Rosca":
        fig = px.pie(dados, names="Produto", values="Quantidade", hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Set1)

    #Layout do gráfico
    fig.update_layout(
        title=f"Quantidade de Produtos Vendidos - {tipo_grafico}",
        title_x=0.5,
        title_font_size=24,
        title_font_family="Arial, sans-serif",
        xaxis_title="Produto" if tipo_grafico in ["Barra", "Colunas"] else None,
        yaxis_title="Quantidade Vendida" if tipo_grafico in ["Barra", "Colunas"] else None,
        showlegend=True
    )

    return fig, info_faturamento

if __name__ == '__main__':
    app.run_server(debug=True)
