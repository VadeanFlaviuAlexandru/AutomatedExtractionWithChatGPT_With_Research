import pandas as pd
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from tempfile import NamedTemporaryFile
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.llms import HuggingFaceHub

prompt = """
     Raspunde la urmatoarele intrebari  folo     Raspunde la urmatoarele intrebari folosind urmatorul format:
     [intrebarea primita]->[raspunsul oferit de catre tine]
     Intrebarile sunt:
     Cate Unitati a vandut martha, in medie, in anul 2018?
     Luand in considerare unitatile vandute de catre Martha in data de 1/6/17 si 1/6/18, cate unitati o sa vanda in 1/6/19?
     Cine a vandut mai multe unitati in anul 2019?
     Cine a vandut mai multe unitati dintre Batman si Superman?
"""

load_dotenv()
st.set_page_config(page_title="ExtragereCicada - XLS/XLSX", page_icon="📈")
st.header("Extragere Conținut - XLS/XLSX")
xls = st.file_uploader("Incarca XLS:", type=["xlsx", "xls"])

if xls is not None:
    buttonPressed = st.button("Fa o predictie!")
    st.write("-------------------------------")
    if buttonPressed:
        with st.spinner("Se citeste... 📄🤔... o secunda, te rog..."):
            with NamedTemporaryFile(mode='w+b', suffix='.xls', delete=False) as f:
                f.write(xls.getvalue())
                f.flush()
                dataForConversion = pd.ExcelFile(f.name)
                pathsArray = []
                for sheet_name in dataForConversion.sheet_names:
                    clean_sheet_name = sheet_name.replace(" ", "_")
                    dataFrame = dataForConversion.parse(sheet_name)
                    path = f'{clean_sheet_name}.csv'
                    pathsArray.append(path)
                    dataFrame.to_csv(path, index=False)
                dataForConversion.close()
                llm = OpenAI(temperature=0)
                agent = create_csv_agent(llm, pathsArray, verbose=False)
                st.write(agent.run(prompt))
                for path in pathsArray:
                    os.remove(path)
