import streamlit as st
import pandas as pd
import pdfplumber
import numpy as np
app_mode = st.sidebar.selectbox('Select Page',['Home','Analysis'])
schemes = {
    'Open ended Schemes': {
        "Income/Debt Oriented Schemes": [
            "Overnight Fund",
            "Liquid Fund",
            "Ultra Short Duration Fund",
            "Low Duration Fund",
            "Money Market Fund",
            "Short Duration Fund",
            "Medium Duration Fund",
            "Medium to Long Duration Fund",
            "Long Duration Fund",
            "Dynamic Bond Fund",
            "Corporate Bond Fund",
            "Credit Risk Fund",
            "Banking and PSU Fund",
            "Gilt Fund",
            "Gilt Fund with 10 year constant duration",
            "Floater Fund",
            "Sub Total - I(i+ii+iii+iv+v+vi+vii+viii+ix+x+xi+xii+xiii+xiv+xv+xvi)"
        ],
        "Growth/Equity Oriented Schemes": [
            "Multi Cap Fund",
            "Large Cap Fund",
            "Large & Mid Cap Fund",
            "Mid Cap Fund",
            "Small Cap Fund",
            "Dividend Yield Fund",
            "Value Fund/Contra Fund",
            "Focused Fund",
            "Sectoral/Thematic Funds",
            "ELSS",
            "Flexi Cap Fund",
            "Sub Total - II (i+ii+iii+iv+v+vi+vii+viii+ix+x+xi)"
        ],
        "Hybrid Schemes": [
            "Conservative Hybrid Fund",
            "Balanced Hybrid Fund/Aggressive Hybrid Fund",
            "Dynamic Asset Allocation/Balanced Advantage Fund",
            "Multi Asset Allocation Fund",
            "Arbitrage Fund",
            "Equity Savings Fund",
            "Sub Total - III (i+ii+iii+iv+v+vi)"
        ],
        "Solution Oriented Schemes": [
            "Retirement Fund",
            "Childrens Fund",
            "Sub Total - IV (i+ii)"
        ],
        "Other Schemes": [
            "Index Funds",
            "GOLD ETF",
            "Other ETFs",
            "Fund of funds investing overseas",
            "Sub Total - V (i+ii+iii+iv)"
        ]
    },
    
    'Close Ended Schemes': {
        "Income/Debt Oriented Schemes": [
            "Fixed Term Plan",
            "Capital Protection Oriented Schemes",
            "Infrastructure Debt Fund",
            "Other Debt Scheme"
        ],
        "Growth/Equity Oriented Schemes": [
            "ELSS",
            "Other Equity Schemes"
        ],
        "Other Schemes": []
    },
    
    'Interval Schemes': {
        "Income/Debt Oriented Schemes": [],
        "Growth/Equity Oriented Schemes": [],
        "Other Schemes": []
    }
}
scheme_data = {
    2: "No. of Schemes",
    3: "No. of Folios",
    4: "Funds Mobilized",
    5: "Repurchase/Redemption",
    6: "Net Assets Under Management",
    7: "Average Net Assets Under Management",
    8: "No. of segregated portfolios created ",
    9: "Net Assets Under Management in segregated portfolio",
    10:"Net Inflow or Outflow",
    11:"Net Asset under Management per Scheme",
    12:"Net Inflow or Outflow per Scheme"}
def fund_selected(filtered_df,fund):
    column_1=filtered_df.columns[1]
    index =filtered_df[filtered_df[column_1] == fund].index.min()
    filtered_df=filtered_df.loc[index]
    return filtered_df
def convert_pdf_to_csv(pdf_file, page=0,selected_scheme=[],selected_sub_schemes=[],selected_fund=''):
    # Open the PDF file
    with pdfplumber.open(pdf_file) as pdf:
        table = pdf.pages[page].extract_table()
        header = 1
        columns = []
        for column in table[header]:
            if column is not None and len(column) > 1:
                columns.append(column)
        df = pd.DataFrame(table[header + 1:], columns=columns)
        column_num=[2,3,4,5,6,7,8,9]
      
        for col in column_num:
            column_name=df.columns[col]
            df[column_name] = df[column_name].str.replace(' ', '').str.replace(',', '')
            df[column_name] = df[column_name].astype(str)
            df[column_name] = pd.to_numeric(df[column_name],errors='coerce')
        
        column_2=df.columns[2]
        column_4=df.columns[4]
        column_5=df.columns[5]
        column_6=df.columns[6]
        
        df["Net Inflow or Outflow"] = df[column_4]-df[column_5]
        df["Net Asset under Management per Scheme"]=df[column_6]/df[column_2]
        df["Net Inflow or Outflow per Scheme"]=df["Net Inflow or Outflow"]/df[column_2]
        if selected_scheme:
            if "Open ended Schemes" in selected_scheme:
                start_index = df[df['Sr'] == 'A'].index.min() 
                end_index = df[df['Sr'] == 'B'].index.min()  
                filtered_df = df.loc[start_index:end_index-1]
                st.write("Open ended Schemes")
                st.write(months[page])
                if selected_sub_schemes:
                    if "Income/Debt Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Income/Debt Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index.min()
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Growth/Equity Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Growth/Equity Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[1]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Hybrid Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Hybrid Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[2]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Solution Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Solution Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[3]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Other Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Other Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[4]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                return filtered_df
                
            elif "Close Ended Schemes" in selected_scheme:
                start_index = df[df['Sr'] == 'B'].index.min()  
                end_index = df[df['Sr'] == 'C'].index.min()'
                filtered_df = df.loc[start_index:end_index-1]
                st.write("Close Ended Schemes")
                if selected_sub_schemes:
                    if "Income/Debt Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Income/Debt Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[0]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Growth/Equity Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Growth/Equity Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[1]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                        
                    elif "Other Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Other Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[2]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                
                return filtered_df
            elif "Interval Schemes" in selected_scheme:
                start_index = df[df['Sr'] == 'C'].index.min() 
                filtered_df = df.loc[start_index:]
                st.write("Interval Schemes")
                if selected_sub_schemes:
                    if "Income/Debt Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Income/Debt Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[0]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Growth/Equity Oriented Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Growth/Equity Oriented Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[1]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                    elif "Other Schemes" in selected_sub_schemes:
                        column_1=df.columns[1]
                        start_index = filtered_df[filtered_df[column_1] == 'Other Schemes'].index.min()
                        end_index = filtered_df[filtered_df[column_1] == ''].index[2]
                        filtered_df = filtered_df.loc[start_index:end_index-1]
                        if selected_fund:
                            filtered_df=fund_selected(filtered_df,selected_fund)
                return filtered_df
    return df
months=['March', 'February', 'January','December', 'November', 'October', 'September',
    'August', 'July', 'June', 'May',
    'April']
funds = [""]
selected_sub_schemes=[]

def main():
    st.title('Mutual fund schemes across financial years')

    st.header('Upload PDF file')
    uploaded_file = st.file_uploader('Choose a PDF file', type='pdf')
    
    
    selected_months=st.multiselect('choose a month',months)
    selected_scheme=[]
    selected_sub_schemes=[]
    selected_fund=''
    if selected_months:
        selected_scheme = st.multiselect('Choose a scheme', list(schemes.keys()))
        if len(selected_scheme)>1:
            st.error("Enter one scheme!!")
        

    if selected_scheme:
        sub_schemes = [sub_scheme for scheme in selected_scheme for sub_scheme in schemes[scheme]]
        selected_sub_schemes = st.multiselect('Choose a sub-scheme', sub_schemes)
        if selected_sub_schemes:
            
            for sub_scheme in selected_sub_schemes: 
                for scheme in selected_scheme: 
                    if sub_scheme in schemes[scheme]:
                        funds.extend(schemes[scheme][sub_scheme])
    if selected_sub_schemes:
        selected_fund=st.selectbox('Select Your Fund',funds)
    page=[]
    for month in selected_months:
        page_number = months.index(month) 
        page.append(page_number)
    if uploaded_file is not None:
       for i in page:
            if selected_fund:
                csv_file = convert_pdf_to_csv(uploaded_file,i,selected_scheme,selected_sub_schemes,selected_fund)
                st.write(csv_file)
            elif selected_sub_schemes:
                csv_file = convert_pdf_to_csv(uploaded_file,i,selected_scheme,selected_sub_schemes)
                st.write(csv_file)
            elif selected_scheme:
                csv_file = convert_pdf_to_csv(uploaded_file,i,selected_scheme)
                st.write(csv_file)
            else:
                csv_file = convert_pdf_to_csv(uploaded_file,i)
                st.write(csv_file)
def main2():
    st.title('Visualization of mutual funds throughout the year ')
    st.header('Upload PDF file')
    uploaded_file = st.file_uploader('Choose a PDF file', type='pdf')
    option=st.selectbox('choose a category to visualize',scheme_data.values())
    for key, value in scheme_data.items():
        if value == option:
            k=key
    values=[]
    if uploaded_file is not None:
        for i in range(12):
            dg = convert_pdf_to_csv(uploaded_file,i)
            column_1=dg.columns[1]
            column_analyse=dg.columns[k]
            ex=dg.loc[dg[column_1] =="Grand Total",column_analyse].values[0]
            values.append(ex)

        data ={
        'Month':months,
        'option':values
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index("Month"))

    
    
    

if app_mode=='Home':
    main()
if app_mode=='Analysis':
    main2()

