import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import heroku3
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

# python unemploymentDemo.py
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("uninsured.csv")

#df = df.groupby(['year', 'state_code'])[['uninsured']]
#df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Uninsured Rate By State", style={'text-align': 'center'}),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='uninsured_map', figure={},config={
                'displayModeBar': False}),
    html.Br(),
        dcc.Slider(id="slct_year",
            updatemode='drag',
            min=2008,
            max=2018,
            className='slider',
            marks={
                2008: {'label': '2008'},
                2009: {'label': '2009'},
                2010: {'label': '2010'},
                2011: {'label': '2011'},
                2012: {'label': '2012'},
                2013: {'label': '2013'},
                2014: {'label': '2014'},
                2015: {'label': '2015'},
                2016: {'label': '2016'},
                2017: {'label': '2017'},
                2018: {'label': '2018'},
            },
            step=1,
            value=2010
            )

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='uninsured_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    #container = "The year chosen by user was: {}".format(option_slctd)
    container = ""

    dff = df.copy()
    dff = dff[dff["year"] == option_slctd]
    #dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='uninsured',
        color_continuous_scale= px.colors.sequential.YlOrRd,
        range_color = [0,.25],
        hover_data = {'State': True, 'state_code': False, 'uninsured': ':.0%'},
        labels={'uninsured': 'Percent Uninsured'},
        template='plotly_white'
    )

    #fig.update_layout(colorbar = dict( title = 'uninsured', zmin = 0, zmax=0.25))

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
