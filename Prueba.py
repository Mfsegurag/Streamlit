import streamlit as st
import pandas as pd
#import openpyxl
import pip
pip.main(["install", "openpyxl"])

st.title('Titulo')

df = pd.read_excel('Record_cursos.xlsx')