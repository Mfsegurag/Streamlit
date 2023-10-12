import streamlit as st
import pandas as pd

import pip
pip.main(["install","openpyxl"])

st.title('Titulo')

df = pd.read_excel('DATA_PRUEBA.xlsx')

#st.write(df)