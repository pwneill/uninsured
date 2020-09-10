import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash_daq as daq

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import heroku3
from dash.dependencies import Input, Output

#Ensure dash capabilities are enabled.
#This allows the code to be deployed on an online server.
app = dash.Dash(__name__)
server = app.server


################################################################################
#This code creates a data visualization of the uninsured rate by state.
#The plotly package is used to create the visualization.
#The dash package is used to create an interactive web app.
#If the app is put on a website, use an iframe of height 800 and width 925.
#################################################################################


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("uninsuredByState.csv")
print(df[:5])

# ------------------------------------------------------------------------------
# App layout (create app layout for the web app)
app.layout = html.Div([
    #Create title.
    html.H1("Uninsured Rate for Young Adults Ages 18-34", style={ 'text-align': 'Center','fontFamily':'Arial, serif'}),

    #Display the option from the slider the user selected. (It is currently disabeled. to enable, change the code in the app.callback so that container = "option_slctd")
    html.Div(id='output_container', children=[],style={'text-align': 'Center', 'fontFamily':'Arial, serif'}),
    html.Br(),

    #Creates a Plotly choropleth map graph.
    dcc.Graph(id='uninsured_map', config={
                'displayModeBar': False}),
    html.Br(),

    #Creates a slider, enabling the user to choose the year displayed.
    html.Div([
        daq.Slider(id="slct_year",
            updatemode='drag',
            min=2008,
            max=2018,
            size=750,
            className='slider',
            marks={
                2008: {'label': '2008','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}}, #creates a list with the options
                2009: {'label': '2009','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2010: {'label': "ACA Passed",'style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2011: {'label': '2011','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2012: {'label': '2012','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2013: {'label': '2013','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2014: {'label': 'ACA in Effect','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2015: {'label': '2015','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2016: {'label': '2016','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2017: {'label': '2017','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2018: {'label': '2018','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
            },
            handleLabel={"showCurrentValue": True,
                        'color':'#3D3D3D',
                        'style':{'text-align': 'center', 'fontFamily':'Arial, serif'},
                        'label':'Year:',
                        },
            step=1,
            color={"gradient":True,"ranges":{"gray":[0,6],"gray":[6,8],"gray":[8,10]}},
            value=2010
            )], style={'width': '100%','text-align':'center','justify-content':'center','margin':'0 auto','margin-left':'auto', 'margin-right':'auto','padding-left':'10%'}),

], style={'width': '95%','padding-left':'0%', 'padding-right':'0%'})


# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='uninsured_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)

    #Code to dynamically display the selected option is in the comment below:
    #container = "The year chosen by user was: {}".format(option_slctd)
    container = ""

    #Create a new dataframe that only includes the selected year's values
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff['uninsured'] = dff['uninsured']*100
    dff['uninsuredStr'] = "percent uninsured"
    dff = dff.round(decimals=2)

    # Plotly Express
    # Creates choropleth map of the US with the selected year
    fig = go.Figure(data=go.Choropleth(
        locations=dff['state_code'],
        z=dff['uninsured'],
        locationmode='USA-states',
        #colorscale='Reds', (this is another option)
        colorscale = ["#fff4ee","#FFE0D9","#f9d5d3","#f49494","#e86464","#dd3430","#a6261f","#730c03","#4f0000"], #Creates a custom color scale for the map, using YI's colors.
        autocolorscale=False,
        colorbar_ticksuffix = '%',
        zmax = 40,
        zmin = 0,
        text = dff['uninsuredStr'],
        marker_line_color='white', # line markers between states
        colorbar_title="Percent Uninsured"
    ))


    #Adds custom styling to the chorppleth map of the US.
    fig.update_layout(
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa')),

        annotations = [dict(
            x=0.55,
            y=-.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://usa.ipums.org/usa/" style="color:#dd3430">American Community Survey</a>',
            showarrow = False
            )]

        )

    #Returns the selected value and the figure to be displayed in the web app.
    return container, fig


#Command that ensures dash capabilities are enabled.
#This allows the code to be deployed on an online server.
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
