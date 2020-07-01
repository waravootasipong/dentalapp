import json
import operator
import traceback
from datetime import timedelta, datetime
from venv import logger
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pymysql as MySQLdb
import pandas as pd
from dash import Dash
from dash.exceptions import PreventUpdate
from sqlalchemy.sql import functions

from mypandas import site_code_col
import urllib
import re


# mysql connection
cnx = MySQLdb.connect(host='203.157.165.111',
                              database='job_sealant',
                              user='datacentpcu',
                              password='asipong123456', auth_plugin='mysql_native_password',use_unicode=True, charset="utf8")
cursor = cnx.cursor()


# fetch the data from databse to df
stringpara=dict()
stringpara={'SD':'2016-01-01','ED':'2020-12-30'}
sdx=stringpara.get('SD')
edx=stringpara.get('ED')
#sql1='SELECT `user`.pcucode, `user`.username, `user`.`password`, `user`.idcard, `user`.prename, `user`.fname, `user`.lname, `user`.dateupdate FROM `user`'
#sql2='where `user`.dateupdate between %s and %s '
##======sql all province set=====
sql1='SELECT provider_service.provider,provider_service.pcucode,sum(provider_service.`1`) d1,sum(provider_service.`2`) d2,sum(provider_service.`3`) d3,sum(provider_service.`4`) d4,sum(provider_service.`5`) d5,sum(provider_service.`6`) d6,sum(provider_service.`7`) d7,sum(provider_service.`8`) d8,sum(provider_service.`9`) d9,sum(provider_service.`10`) d10,sum(provider_service.`11`) d11,sum(provider_service.`12`) d12,sum(provider_service.`13`) d13,sum(provider_service.`14`) d14,sum(provider_service.`15`) d15,sum(provider_service.`16`) d16,sum(provider_service.`17`) d17,sum(provider_service.`18`) d18,sum(provider_service.`19`) d19,sum(provider_service.`20`) d20,sum(provider_service.`21`) d21,sum(provider_service.`22`) d22,sum(provider_service.`23`) d23,sum(provider_service.`24`) d24,sum(provider_service.`25`) d25,sum(provider_service.`26`) d26,sum(provider_service.`27`) d27,sum(provider_service.`28`) d28,sum(provider_service.`29`) d29,sum(provider_service.`30`) d30,sum(provider_service.`31`) d31,provider_service.mon mon,provider_service.years FROM provider_service'
sql2=' WHERE years between '"%s"' and '"%s"' GROUP BY provider_service.provider'
sql=sql1+sql2

##======sql amphur select========
sql4='SELECT provider_service.provider,provider_service.pcucode,sum(provider_service.`1`) d1,sum(provider_service.`2`) d2,sum(provider_service.`3`) d3,sum(provider_service.`4`) d4,sum(provider_service.`5`) d5,sum(provider_service.`6`) d6,sum(provider_service.`7`) d7,sum(provider_service.`8`) d8,sum(provider_service.`9`) d9,sum(provider_service.`10`) d10,sum(provider_service.`11`) d11,sum(provider_service.`12`) d12,sum(provider_service.`13`) d13,sum(provider_service.`14`) d14,sum(provider_service.`15`) d15,sum(provider_service.`16`) d16,sum(provider_service.`17`) d17,sum(provider_service.`18`) d18,sum(provider_service.`19`) d19,sum(provider_service.`20`) d20,sum(provider_service.`21`) d21,sum(provider_service.`22`) d22,sum(provider_service.`23`) d23,sum(provider_service.`24`) d24,sum(provider_service.`25`) d25,sum(provider_service.`26`) d26,sum(provider_service.`27`) d27,sum(provider_service.`28`) d28,sum(provider_service.`29`) d29,sum(provider_service.`30`) d30,sum(provider_service.`31`) d31,provider_service.mon mon,provider_service.years FROM provider_service'
sql5=' WHERE years between '"%s"' and '"%s"' and provide_service.amphur='"%s"' GROUP BY provider_service.provider'
sqlamp=sql4+sql5

print(sql)
def get_data():
    try:

        df = pd.read_sql(sql, cnx,params=[sdx,edx])

        return df
    except Exception as e:
        print("Excel File Generate Error: \n", traceback.format_exc())


def get_data_recover(xx,yy):
    try:
        dfx = pd.read_sql(sql, cnx,params=[xx,yy])

        table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i, "deletable": True}
                     for i in dfx.columns],
            data=dfx.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=True,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={'overflowX': 'scroll'},
            style_header={
                'backgroundColor': 'green',
                'fontWeight': 'bold'
            },
            style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'width' :'auto',
    }
        )

        return table
    except Exception as e:
        print("Excel File Generate Error: \n", traceback.format_exc())


def List_amp():

        dfmenu = pd.read_sql(sql, cnx,params=[sdx,edx])
        return dfmenu

def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """

  if value < 50:
    color = 'green'
  elif value > 50:
    color = 'red'
  else:
    color = 'black'

  return 'color: %s' % color


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("คู่มือและนิยาม", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu(...เมนู...)",
            children=[
                dbc.DropdownMenuItem("รายการข้อมูล 1"),
                dbc.DropdownMenuItem("รายการข้อมูล 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("รายการข้อมูล 3"),
            ],
        ),
    ],
    color="dark",
    brand="ICT_dash",
    brand_href="#",
    sticky="top",
    dark=True
)
# body
body = dbc.Container(
    [
        dbc.Container([

            html.H3("รายการข้อมูล"),
            html.Br([]),html.H5("เลือกรายการข้อมูลระหว่างช่วงเวลา"),dcc.DatePickerRange(
             id='my-date-picker-range',
	         min_date_allowed=datetime(2010, 1, 1),
             max_date_allowed=datetime.now(),
             initial_visible_month=datetime.now(),
             start_date=datetime.now() ,
             end_date=datetime.now()
            ), html.Div(id='output-container-date-picker-range'),
            html.Br([]),html.Label('กรุณาเลือกอำเภอหากต้องการ'),

    dcc.Dropdown(
        id="scInput",
        options=[{'label': i['amphurname'], 'value': i['amphurcode']} for i in site_code_col],
        style=dict(
                    width='40%',
                    verticalAlign="left"
                ),
        value="MTL"
    ),
            html.Br([]),html.Label('ส่งออกข้อมูลที่เลือกไป xlsx'),
            html.Div(dash_table.DataTable(id='my-table',
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            page_current=0,
            page_size=15,
 ##--------------fix collums-------------

  ##====export option
     export_format='xlsx',
     export_headers='ids',
     merge_duplicate_headers=True,
  ##===end export option
            style_table={
                 'overflowX': 'scroll',
                'maxHeight': '50ex',
                'width': '100%',
                'minWidth': '100%'
                                    },
                 style_header={ 'fontWeight': 'bold',
                'backgroundColor': 'green',
                'fontWeight': 'bold' },
                style_cell={
                   'whiteSpace': 'normal',
                    'height': 'auto'
                                      }

             ))
        ]),

     ]
)


app.layout = html.Div([
    navbar,
    body])



@app.callback(
   dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')
     ])
def update_output(start_date, end_date):
    string_prefix = 'คุณเลือกช่วงข้อมูลระหว่าง วันที่: '

    if start_date is not None:
        start_date = datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        stringpara['SD']=start_date.strftime('%Y-%m-%d')
        string_prefix = string_prefix + 'วันเริ่มต้น: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        stringpara['ED']=end_date.strftime('%Y-%m-%d')

        string_prefix = string_prefix + 'วันสิ้นสุด: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(
    [dash.dependencies.Output('my-table', 'data'),
    dash.dependencies.Output('my-table', 'columns')],
    [
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')
     ])

def update_data(start_date,end_date):

        start_date = datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        end_date = datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        sz=start_date.strftime('%Y')
        ez=end_date.strftime('%Y')
        #print(sz)
        df = pd.read_sql(sql, cnx,params=[sz,ez])
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns]
        data=df.to_dict('records')
        return data,columns



if __name__ == '__main__':
    app.run_server(debug=True)

