from dbCon import engine
import pandas as pd
site_code_col = pd.read_sql('SELECT amphurname,amphurcode FROM amphur', engine).dropna().to_dict(orient='records')
