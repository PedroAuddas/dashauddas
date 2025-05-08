import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Carregar dados
df = pd.read_excel("fluxo_financeiro_abril2025_com_grafico.xlsx")

# Garantir que os valores sejam formatados em R$
df['Recebido'] = df['Recebido'].apply(lambda x: f"R$ {x:,.2f}")
df['Pago'] = df['Pago'].apply(lambda x: f"R$ {x:,.2f}")
df['Saldo Diário'] = df['Saldo Diário'].apply(lambda x: f"R$ {x:,.2f}")

# Inicializar app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Fluxo Financeiro"

app.layout = dbc.Container([
    html.H2("Dashboard Interativo - Fluxo Financeiro Abril/2025", className="my-4"),

    dbc.Row([
        dbc.Col(html.Div([
            html.H5("Total Recebido"),
            html.H4(f"{df['Recebido'].sum()}"),
        ]), width=3),
        dbc.Col(html.Div([
            html.H5("Total Pago"),
            html.H4(f"{df['Pago'].sum()}"),
        ]), width=3),
        dbc.Col(html.Div([
            html.H5("Saldo Acumulado"),
            html.H4(f"{df['Saldo Diário'].sum()}"),
        ]), width=3),
        dbc.Col(html.Div([
            html.H5("Antecipações de Lucro"),
            html.H4("25,04%"),
        ]), width=3),
    ], className="mb-4"),

    # Gráfico interativo de Recebido x Pago
    dcc.Graph(
        id='grafico_fluxo',
        figure=px.bar(
            df,
            x='Data Formatada',
            y=['Recebido', 'Pago'],
            barmode='group',
            labels={'value': 'Valor (R$)', 'variable': 'Tipo'},
            title='Fluxo Diário: Recebido x Pago',
            hover_data={'Data Formatada': True, 'Recebido': True, 'Pago': True, 'Saldo Diário': True}
        ).update_layout(
            xaxis_title="Data",
            yaxis_title="Valor (R$)",
            template="plotly_white",
            hovermode="x unified"
        )
    ),

    html.Hr(),

    html.H4("Tabela de Dados"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'rgb(240,240,240)', 'fontWeight': 'bold'}
    )
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
