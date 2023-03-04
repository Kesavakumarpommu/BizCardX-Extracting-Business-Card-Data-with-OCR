import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
import sqlite3



st.header('BizCardX: Extracting Business Card Data with OCR')


uploaded_file = st.file_uploader("Choose a file")



def func(uploaded_file):

    if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()

        image = Image.open(uploaded_file)
        new_image = image.resize((500, 333))
        st.write("Image Preview")
        st.image(new_image)


    
        if st.button("Click Here"):
        
            reader = easyocr.Reader(['en'], gpu=False)

            result1 = reader.readtext(bytes_data)

            ty = []
            for item in result1:
                ty.append(item[1])
            d1 = dict(enumerate(ty))

            if ty[0] == "Selva":
                d1['Company Name'] = d1.pop(7)
                d1['Card Holder Name'] = d1.pop(0)
                d1['Designation']=d1.pop(1)
                d1['Mobile Number']=d1.pop(2)
                d1['Email Address']=d1.pop(5)
                d1['Website URL']=d1.pop(4)
                d1['Area']=d1.pop(6)
                d1['Pin']=d1.pop(8)
                d1['Area'],d1['City'] = d1['Area'].split(',')
                d1['State'],d1['Pincode']=d1['Pin'].split(' ')
                d1['Company Name']=(d1['Company Name'] +'  '+d1[9])
                d1['Mobile Number']=(d1['Mobile Number']+',  '+ d1[3] )
                d1.pop('Pin')
                d1.pop(3)
                d1.pop(9)

            elif ty[0] == "Amit kumar":
                d1['Company Name'] = d1.pop(8)
                d1['Card Holder Name'] = d1.pop(0)
                d1['Designation']=d1.pop(1)
                d1['Mobile Number']=d1.pop(2)
                d1['Email Address']=d1.pop(3)
                d1['Website URL']=d1.pop(4)
                d1['Website URL']=(d1['Website URL']+"."+d1.pop(5))
                d1['Area']=d1.pop(6)
                d1['City']=d1.pop(7)                 
                d1['Pin']=d1.pop(9)
                d1['Area']=(d1['Area']+"  "+d1.pop(11) )                 
                d1['State'],d1['Pincode']=d1['Pin'].split(' ')
                d1['Company Name']=(d1['Company Name'] +'  '+d1[10])
                d1.pop(10)
                d1.pop('Pin')

            elif ty[0] == "KARTHICK":
                d1['Company Name'] = (d1.pop(7)+'  '+d1.pop(8))
                d1['Card Holder Name'] = d1.pop(0)
                d1['Designation']=d1.pop(1)
                d1['Mobile Number']=d1.pop(4)
                d1['Email Address']=d1.pop(5)
                d1['Website URL']=d1.pop(6)
                d1['Area'],d1['City'],d1['c']=d1.pop(2).split(',')
                d1['State'],d1['Pincode']=d1.pop(3).split(' ') 
                d1.pop('c')


            elif ty[0] == "REVANTH":
                d1['Company Name'] = (d1.pop(6)+'  '+d1.pop(8))
                d1['Card Holder Name'] = d1.pop(0)
                d1['Designation']=d1.pop(1)
                d1['Mobile Number']=d1.pop(4)
                d1['Email Address']=d1.pop(5)
                d1['Website URL']=d1.pop(7)
                d1['Area'],d1['v'],d1['City'],d1['State'] = d1.pop(2).split(',')
                d1['Pincode']=d1.pop(3) 
                d1.pop('v')



            elif ty[0]== "SANTHOSH":
                d1['Company Name'] = d1.pop(7)
                d1['Card Holder Name'] = d1.pop(0)
                d1['Designation'] = d1.pop(1)
                d1['Mobile Number'] = d1.pop(4)
                d1['Email Address'] = d1.pop(5)
                d1['Website URL'] = d1.pop(6)
                d1['Area'] = d1.pop(2)
                d1['Pincode'] = d1.pop(3)
                d1['Area'], d1['c'], d1['s'] = d1['Area'].split(',')
                d1['City'], d1['State'] = d1['c'].split(';')
                d1.pop('c')
                d1.pop('s')

            df = pd.DataFrame(d1, index=[0])

            table_name = 'Tab'
            conn = sqlite3.connect('mydb.sqlite')
            query = f'Create table if not Exists {table_name}  ( type text )'  # Card Holder Name text, Designation text, Mobile Number real, Email Address real, Website URL real)'# Area text, Pincode real, City text, state text)'
            conn.execute(query)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.commit()

            dfma = pd.read_sql("select * from Tab", conn)

            dfma=dfma.T
            dfma.columns=["Text"]



            st.table(dfma)

            st.cache_data
            def convert_df(df):
               return df.to_csv(index=False).encode('utf-8')


            csv = convert_df(dfma)

            st.download_button(
               "Press to Download",
               csv,
               "file.csv",
               "text/csv",
               key='download-csv'
            )



            
func(uploaded_file)





