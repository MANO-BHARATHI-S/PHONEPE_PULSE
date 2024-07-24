import streamlit as st
import pandas as pd
import plotly.express as px
from numerize import numerize
import mysql.connector

st.set_page_config(layout="wide")


@st.cache_data()
def get_data(query):
# connection to mysql    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mano@3221",
        database="phonepe",
    )    
    mycursor = mydb.cursor()
       
    mycursor.execute(query)
    data = mycursor.fetchall()
    colnames = [desc[0] for desc in mycursor.description]
    df = pd.DataFrame(data, columns=colnames)
    mycursor.close()
    mydb.close()
    return df


# Function to execute a query and return the result as a DataFrame
def execute_query(query):
    return get_data(query)

# Getting the data
df = get_data("SELECT * FROM agg_trans")
df2 = get_data("SELECT * FROM agg_user")
df3 = get_data("SELECT * FROM map_trans")
df4 = get_data("SELECT * FROM map_user")
df5 = get_data("SELECT * FROM top_trans")
df6 = get_data("SELECT * FROM top_user")


st.subheader("Phonepe Pulse Data Visualization and Exploration:")
tab1, tab2, tab3, tab4 = st.tabs([":ice_cube: INTRODUCTION", ":ice_cube: DATA VISUALIZATION", ":ice_cube: INSIGHTS", ":ice_cube: CONCLUSION"])

with tab1:
    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[About PhonePe Pulse:] ")
    st.write("##### On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
    st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
    st.markdown("### :violet[About PhonePe:] ")
    st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        

with tab2:


    st.header('Filters and Visualizations')

    user_filter = st.selectbox('Select User', ['--Select--', 'AGGREGATED_TRANSACTION', 'AGGREGATED_USER', 'MAP_TRANSACTION', 'MAP_USER'])

    if user_filter == 'AGGREGATED_TRANSACTION':
        st.subheader('Filters for Aggregated Transactions')
        state_filter = st.multiselect(label='Filter State',
                                      options=df['State'].unique(),
                                      default=df['State'].unique())

        transtype_filter = st.multiselect(label='Filter Transaction_type',
                                          options=df['Transaction_type'].unique(),
                                          default=df['Transaction_type'].unique())

        year_filter = st.multiselect(label='Filter Year',
                                          options=df['Year'].unique(),
                                          default=df['Year'].unique())

        quarter_filter = st.multiselect(label='Filter Quarter',
                                         options=df['Quater'].unique(),
                                         default=df['Quater'].unique())
        
        
        

        df1 = df.query('State == @state_filter & Year == @year_filter & Quater == @quarter_filter & Transaction_type == @transtype_filter')

        total_transactions = float(df1['Transaction_amount'].sum())
        transaction_count = float(df1['Transaction_count'].sum())

        st.subheader('Metrics')
        total1, total2, total3 = st.columns(3, gap='large')

        with total1:
            st.metric(label=':violet[TOTAL TRANSACTIONS]', value=numerize.numerize(total_transactions))

        with total2:
            st.metric(label=':violet[TOTAL COUNT]', value=numerize.numerize(transaction_count))

        st.subheader("Visualizations")

        with st.container():
            df11 = df1.groupby('State')['Transaction_amount'].sum().reset_index()
            fig1 = px.bar(df11, x='State', y='Transaction_amount', 
                          title='OVERALL STATE-WISE PERFORMANCE FROM YEAR 2018 TO 2023',
                          color='State', color_discrete_sequence=px.colors.qualitative.Alphabet)
            st.plotly_chart(fig1)

        with st.container():
            df11 = df1.groupby('Transaction_type')['Transaction_amount'].sum().reset_index()
            fig2 = px.pie(df11, names='Transaction_type', values='Transaction_amount',
                          title='TOTAL TRANSACTION BY TRANSACTION TYPE',
                          color_discrete_sequence=px.colors.qualitative.Safe, hole=0.7)
            st.plotly_chart(fig2)

        with st.container():
            fig3 = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Transaction_amount',
                color_continuous_scale='Earth',
            )

            fig3.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig3)

            
            
            
            
    elif user_filter == 'AGGREGATED_USER':
        st.subheader('Filters for Aggregated Users')
        userbybrand_filter = st.multiselect(label='Filter User by Device Brand',
                                            options=df2['brands'].unique(),
                                            default=df2['brands'].unique())

        userbystate_filter = st.multiselect(label='Filter User by State',
                                             options=df2['State'].unique(),
                                             default=df2['State'].unique())

        userbyyear_filter = st.multiselect(label='Filter User by Year',
                                             options=df2['Year'].unique(),
                                             default=df2['Year'].unique())

        userbyquarter_filter = st.multiselect(label='Filter User by Quarter',
                                              options=df2['Quater'].unique(),
                                              default=df2['Quater'].unique())

        df2 = df2.query('State == @userbystate_filter & Year == @userbyyear_filter & Quater == @userbyquarter_filter & brands == @userbybrand_filter')

        userbybrand_count = float(df2['Count'].sum())

        st.subheader('Metrics')
        
        
        total1, total2, total3 = st.columns(3, gap='large')
        with total1:
            st.metric(label='USERS', value=numerize.numerize(userbybrand_count))
            
            

        st.subheader("Visualizations")

        with st.container():
            df22 = df2.groupby('brands')['Count'].sum().reset_index()
            fig1 = px.bar(df22, x='brands', y='Count', color="brands",
                          title='USERS TRANSACTION BY MOBILE DEVICE BRAND',
                          color_discrete_sequence=px.colors.qualitative.Alphabet)
            st.plotly_chart(fig1)

        with st.container():
            fig3 = px.choropleth(
                df2,
     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Count',
                color_continuous_scale='Earth',
            )

            fig3.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig3)
            
            
            
            
            
            
            

    elif user_filter == 'MAP_TRANSACTION':
        st.subheader('Filters for Map Transactions')
        mapbystate_filter = st.multiselect(label='Filter User by State',
                                           options=df3['State'].unique(),
                                           default=df3['State'].unique())

        mapbyyear_filter = st.multiselect(label='Filter User by Year',
                                          options=df3['Year'].unique(),
                                          default=df3['Year'].unique())

        mapbyquarter_filter = st.multiselect(label='Filter User by Quarter',
                                             options=df3['Quater'].unique(),
                                             default=df3['Quater'].unique())

        mapbydistrict_filter = st.multiselect(label='Filter User by District',
                                              options=df3['District'].unique(),
                                              default=df3['District'].unique())

        df3 = df3.query('State == @mapbystate_filter & Year == @mapbyyear_filter & Quater == @mapbyquarter_filter & District == @mapbydistrict_filter')

        st.subheader("Visualizations")

        with st.container():
            df33 = df3.groupby(['District', 'State'])['count'].sum().reset_index()
            fig3 = px.bar(df33, x='District', y='count', text='count',
                          title='USERS TRANSACTION DISTRICT-WISE',
                          color='State', color_discrete_sequence=px.colors.qualitative.Alphabet)
            st.plotly_chart(fig3)
            
            
            
            
            
            
        
    elif user_filter == 'MAP_USER':
        st.subheader('Filters for Map User')
        mapbystate_filter = st.multiselect(label='Filter User by State',
                                           options=df3['State'].unique(),
                                           default=df3['State'].unique())

        mapbyyear_filter = st.multiselect(label='Filter User by Year',
                                          options=df3['Year'].unique(),
                                          default=df3['Year'].unique())

        mapbyquarter_filter = st.multiselect(label='Filter User by Quarter',
                                             options=df3['Quater'].unique(),
                                             default=df3['Quater'].unique())

        mapbydistrict_filter = st.multiselect(label='Filter User by District',
                                              options=df3['District'].unique(),
                                              default=df3['District'].unique())
        
        
        
        
        df4 = df4.query('State == @mapbystate_filter & Year == @mapbyyear_filter & Quater == @mapbyquarter_filter & District == @mapbydistrict_filter')
        
        st.subheader("Visualizations")
        
        
        with st.container():
            df44 = df4.groupby(['District', 'State'])['RegisteredUser'].sum().reset_index()
            fig4 = px.bar(df44, x='District', y='RegisteredUser', 
                          title='USERS TRANSACTION DISTRICT-WISE',
                          color='State', color_discrete_sequence=px.colors.qualitative.Alphabet)
            st.plotly_chart(fig4)
            
            
        with st.container():
            fig4 = px.choropleth(df4,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='RegisteredUser',
                color_continuous_scale='Earth')

            fig4.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig4)
            

            
with tab3:

    st.title(':violet[BASIC INSIGHTS]')
    st.subheader("The basic insights are from the Phonepe Pulse data.")
    options = [
               "Top 10 states based on amount of transaction",
               "Least 10 states based on amount of transaction",
               "Top 10 States and Districts based on Registered Users",
               "Least 10 States and Districts based on Registered Users",
               "Top 10 Districts based on the Transaction Amount",
               "Least 10 Districts based on the Transaction Amount",
               "Top 10 Districts based on the Transaction count",
               "Least 10 Districts based on the Transaction count",
               "Top Transaction types based on the Transaction Amount",
               "Top 10 Mobile Brands based on the User count of transaction"]
    select = st.selectbox(":violet[Select the option]", options)

    if select == "Top 10 states based on amount of transaction":
        query = """select  State, sum(Transaction_amount) AS Total_Transaction_Amount 
                    from top_trans 
                    group BY State 
                    order BY Total_Transaction_Amount DESC limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="State", y="Total_Transaction_Amount", color="State",
                         title="Top 10 States and Districts based on Registered Users",
                         labels={"State": "State", "Total_Transaction_Amount": "Total_Transaction_Amount"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Least 10 states based on amount of transaction":
        query = """select State, SUM(Transaction_amount) AS Total_Transaction_Amount 
                    from top_trans 
                    group BY State
                    order BY Total_Transaction_Amount asc limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="State", y="Total_Transaction_Amount", color="State",
                         title="Least 10 states based on amount of transaction",
                         labels={"State": "State", "Total_Transaction_Amount": "Total_Transaction_Amount"},
                         text_auto=True)
            st.plotly_chart(fig)


    elif select == "Top 10 States and Districts based on Registered Users":
        query = """select State, District, SUM(RegisteredUser) AS Total_Registered_Users 
        from map_user 
        group BY State, District 
        order BY Total_Registered_Users DESC limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Registered_Users", color="State",
                         title="Top 10 States and Districts based on Registered Users",
                         labels={"District": "District", "Total_Registered_Users": "Total Registered Users"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Least 10 States and Districts based on Registered Users":
        query = """ select State, District, sum(RegisteredUser) AS Total_Registered_Users 
                    from map_user 
                    group BY State, District 
                    order BY Total_Registered_Users asc limit 10"""
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Registered_Users", color="State",
                         title="least 10 States and Districts based on Registered Users",
                         labels={"District": "District", "Total_Registered_Users": "Total Registered Users"},
                         text_auto=True)
            st.plotly_chart(fig)


    elif select == "Top 10 Districts based on the Transaction Amount":
        query = """select State, District, sum(amount) AS Total_Transaction_Amount 
                    from map_trans 
                    group BY State, District 
                    order BY Total_Transaction_Amount desc limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Transaction_Amount", color="State",
                         title="Top 10 States and Districts based on Transaction Amount",
                         labels={"District": "District", "Total_Transaction_Amount": "Total_Transaction_Amount"},
                         text_auto=True)
            st.plotly_chart(fig)


    elif select == "Least 10 Districts based on the Transaction Amount":
        query = """select State, District, sum(amount) as Total_Transaction_Amount 
                    from map_trans 
                    group BY State, District 
                    order BY Total_Transaction_Amount asc limit 10"""
        
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Transaction_Amount", color="State",
                         title="least 10 States and Districts based on Transaction Amount",
                         labels={"District": "District", "Total_Transaction_Amount": "Total_Transaction_Amount"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Top 10 Districts based on the Transaction count":
        query = """select State, District, sum(Count) as Total_Transaction_Count 
        from map_trans 
        group BY State, District 
        order BY Total_Transaction_Count desc limit 10"""
        
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Transaction_Count", color="State",
                         title="Top 10 States and Districts based on Transaction Count",
                         labels={"District": "District", "Total_Transaction_Count": "Total_Transaction_Count"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Least 10 Districts based on the Transaction count":
        query = """select District, sum(Count) as Total_Transaction_Count 
        from map_trans 
        group by District 
        order by Total_Transaction_Count asc limit 10"""
        
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="District", y="Total_Transaction_Count", color="State",
                         title="Least 10 States and Districts based on Transaction Count",
                         labels={"District": "District", "Total_Transaction_Count": "Total_Transaction_Count"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Top Transaction types based on the Transaction Amount":
        query = """select Transaction_type, sum(Transaction_amount) as Total_Transaction_Amount 
        from agg_trans 
        group by Transaction_type 
        order by Total_Transaction_Amount desc limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="Transaction_type", y="Total_Transaction_Amount", color="Transaction_type",
                         title="Top Transaction types based on the Transaction Amount",
                         labels={"Transaction_type": "Transaction_type", "Total_Transaction_Amount": "Total_Transaction_Amount"},
                         text_auto=True)
            st.plotly_chart(fig)

    elif select == "Top 10 Mobile Brands based on the User count of transaction":
        query = """select brands, sum(Count) as Total_Count 
        from agg_user 
        group BY brands 
        order BY Total_Count desc limit 10"""
        
        data = execute_query(query)
        col1, col2 = st.columns(2)
        with col1:
            st.write(data)
        with col2:
            fig = px.bar(data, x="brands", y="Total_Count", color="brands",
                         title="Top 10 Mobile Brands based on the User count",
                         labels={"brands": "Brands", "Total_Count": "Total_Count"},
                         text_auto=True)
            st.plotly_chart(fig)

            
with tab4:
    st.write(" ")
    st.write(" ")
    st.subheader(":violet[The Annual Report of Phonepe Pulse data]")
    st.write(" ")
    st.write("##### :green[India's digital payments landscape has transformed dramatically, with 40% of payments now digital, contributing to This growth is driven by UPI-led migration, the pandemic, increased merchant acceptance, and fintech innovations. However, significant growth potential remains in underpenetrated segments, especially in Tier 3-6 locations, which have seen 60-70% of new mobile payment customers recently. Expanding merchant acceptance, value chain digitization, and establishing financial services in these areas will drive rapid growth. The introduction of 5G, IoT, and the Digital Rupee will further boost the market. By 2026, the digital payments market is expected to triple to US 10 trillion dollars, with non-cash transactions comprising 65% of all payments. Merchant payments, particularly in the offline segment, will be the primary growth driver. As digital payments become embedded in commerce, access to credit for small merchants will improve. However, payment players face challenges with thin margins, prompting a shift to high-margin offerings and the development of super app ecosystems. Achieving the US$10 trillion opportunity will require building customer trust, improving fraud management, simplifying onboarding and KYC processes, and strengthening digital infrastructure.]")
    
    with open("C:/Users/manob/OneDrive/Desktop/project2/report.pdf", "rb") as f:
        data = f.read()
    st.download_button("DOWNLOAD REPORT", data, file_name="report.pdf")
