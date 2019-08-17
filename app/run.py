from app import app
import json
import plotly
import pandas as pd


from flask import Flask
from flask import render_template
from plotly.graph_objs import Bar, Scatter, Table



#app = Flask(__name__)


# load data

df_codes = pd.read_csv('http://codefor.ca/wp-content/uploads/2018/06/C4C-dev-challenge-2018.csv')

# Converting dates to datetime objects
df_codes.violation_date = pd.to_datetime(df_codes.violation_date)
df_codes.violation_date_closed = pd.to_datetime(df_codes.violation_date_closed)

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    #First plot
    graph_1 = df_codes.violation_category.value_counts().sort_values(ascending=False)

    #Second plot
    graph_2 = df_codes[['violation_category', 'violation_date']]
    categories = pd.unique(graph_2.violation_category.values)
    df_list = []
    for category in categories:
        df_temp = graph_2.query('violation_category == @category').groupby(
            graph_2.violation_date.dt.to_period('M').rename('date')).count()['violation_date']
        df_temp = pd.DataFrame(df_temp.T)  # .reset_index(inplace=True)
        df_temp.reset_index(inplace=True)
        df_temp.columns = ['validation_date', 'counts']
        df_temp.validation_date = df_temp.validation_date.astype('str')

        df_list.append(df_temp)

    # Table
    df_dates = df_codes.groupby('violation_category').aggregate(['min', 'max'])['violation_date'].reset_index()



    # create visuals
    graphs = [
        {
            'data': [
                Bar(
                    x = graph_1.index.tolist(),
                    y = graph_1.values,
                    #name = 'news',
                    width = 0.8,
                    marker = dict(
                        color='rgb(0,128,128)'
                    )
                    #orientation = 'h'

                )
            ],

            'layout': {
                'title': 'Number of violations by category',
                'yaxis': {
                    'title': 'Count'
                },
                'xaxis': {
                    'title': 'Category'
                },
                #'legend': {
                #    'orientation': 'h',
                #    'x': 0.33,
                #    'y': 1.1
                #},
                'margin': {
                    #'l': 1
                }
                #'width': 740
            }

        },
        {
            'data': [
                Scatter(
                    x=df_list[0].validation_date,
                    y=df_list[0].counts,
                    name = categories[0],
                    #marker= dict(
                    #    color ='LightSkyBlue',
                    #    size = 10,
                    #    opacity=0.7,
                    #    line=dict(
                    #        color='MediumPurple',
                    #        width=2
                    #    )
                        #color = ['rgb(255, 127, 14)']
                    #),
                    mode = 'lines',
                    stackgroup='one'  # define stack group
                ),
                Scatter(
                    x=df_list[1].validation_date,
                    y=df_list[1].counts,
                    name = categories[1],
                    mode = 'lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[2].validation_date,
                    y=df_list[2].counts,
                    name=categories[2],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[3].validation_date,
                    y=df_list[3].counts,
                    name=categories[3],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[4].validation_date,
                    y=df_list[4].counts,
                    name=categories[4],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[5].validation_date,
                    y=df_list[5].counts,
                    name=categories[5],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[6].validation_date,
                    y=df_list[6].counts,
                    name=categories[6],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[7].validation_date,
                    y=df_list[7].counts,
                    name=categories[7],
                    mode='lines',
                    stackgroup='one'
                ),
                Scatter(
                    x=df_list[8].validation_date,
                    y=df_list[8].counts,
                    name=categories[8],
                    mode='lines',
                    stackgroup='one'
                )
            ],

            'layout': {
                'title': 'Violation dates per category',
                'yaxis': {
                    'title': "Count",
                    'showgrid': True,
                    'nticks': 20

                },
                'xaxis': {
                    'title': "Dates",
                    'nticks': 20
                },
                'legend': {
                    'orientation': "h",
                    'x':0.33,
                    'y':1.18
                },
                'automargin': True
            },

        },
        {
            'data': [
                Table(
                    header= {
                        'values': ["Type","Earliest<br>date", "Latest<br>date"]
                    },
                    cells= {
                        'values': [df_dates[k].tolist() for k in df_dates.columns]
                    }
                )
            ],
            'layout': {
                'title': "Violation Dates",
                #'height': 800
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


#def main():
    #app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    #main()
    app.run()