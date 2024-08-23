import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from scipy.stats import chi2_contingency
from matplotlib.backends.backend_pdf import PdfPages
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import hashlib
import datetime
from plotly.subplots import make_subplots
import streamlit as st
import toml


# Define a secure username and password
import os
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", )
st.markdown(
    """
    <style>
    .centered {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
f = False
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file):
    # Check if file is allowed
    if file and allowed_file(file.name):
        # Save the file
        filepath = os.path.join( file.name)
        with open(filepath, 'wb') as f:
            f.write(file.getbuffer())
        
        while True:
            try:
                # Check if the file is an Excel file
                if not pd.ExcelFile(filepath).sheet_names:
                    os.remove(filepath)  # Remove the invalid file
                    st.error('Invalid Excel file')
                    return
                
                # Load the Data.xlsx file
                data_filepath = 'Data.xlsx'
                data_df = pd.read_excel(data_filepath)
                
                # Load the new file
                new_df = pd.read_excel(filepath)
                
                # Check if 'Email' column exists in the new file
                if 'Email' not in new_df.columns:
                    os.remove(filepath)  # Remove the invalid file
                    st.error('Invalid file format: Missing "Email" column')
                    file = st.file_uploader('Choose another Excel file', type=ALLOWED_EXTENSIONS)
                    if file is not None:
                        process_file(file)
                    else:
                        st.warning('No file selected')
                        break  # Break the loop if the user doesn't select another file
                    return
                
                # Find new emails and add them to Data.xlsx
                new_emails = set(new_df['Email']) - set(data_df['Email'])
                new_rows = new_df[new_df['Email'].isin(new_emails)]
                
                if not new_rows.empty:
                    data_df = pd.concat([data_df, new_rows])
                    data_df.to_excel(data_filepath, index=False)
                    st.success('New rows added to Data.xlsx')
                    
                
                os.remove(filepath)  # Remove the uploaded file after processing
                break  # Break the loop if the code runs successfully
            
            except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
                os.remove(filepath)  # Remove the invalid file
                st.error('Invalid file format or missing data')
                file = st.file_uploader('Choose another Excel file', type=ALLOWED_EXTENSIONS)
                if file is not None:
                    process_file(file)
                else:
                    st.warning('No file selected')
                    break  # Break the loop if the user doesn't select another file
    else:
        st.error('Invalid file format')


def main():
    # Title of the application
    pp = PdfPages('Data_Plots.pdf')
    all_dfs=[]
    st.markdown("<h2 style='text-align: center;'>Data Analytics Intellia Advisors</h2>", unsafe_allow_html=True)
    upload_choice = st.radio('Do you want to upload a file?', ('No', 'Yes'))
    
    if upload_choice == 'No':
        st.info('Continuing without file upload')
        # Further code execution
        
    elif upload_choice == 'Yes':
        file = st.file_uploader('Choose an Excel file', key='file_uploader', type=ALLOWED_EXTENSIONS)
        
        if file is not None:
            process_file(file)
            st.info('New rows added. Continuing further')
            
            # Perform data processing on Data.xlsx
            data_filepath = 'Data.xlsx'
            data_df = pd.read_excel(data_filepath)
    
    


   

    # Read the Excel file into a DataFrame


    st.markdown("<h2 style='text-align: center;'>Hiring Form Data</h2>", unsafe_allow_html=True)
    df = pd.read_excel('Data.xlsx')
    df = df[['Country',
  'University Name',
  'School Qualification',
  'Degree/Qualification',
  'GPA / GPA Equivalent',
  'Additional Languages',
  'Consulting Experience',
  'Status',
  'Position Applied',
  'Were you referred by anyone?',
  'Total Experience - Years',
  'Department',
  'Industry',
  'Gender',
  'Skills',
  'Area of Study',
  'Assessment Overall Score',
  'Grad University Name',
  'Grad Area of Study',
  'Round 1 Notes',
  'Round 1 Decision',
  'Round 2 Notes',
  'Round 2 Decision',
  'Round 3 Notes',
  'Round 3 Decision',
  'Created Time',
  'How did you hear about Intellia?'
  ]]
    # Display the entire DataFrame
    st.write(df)
    filtered_data = df[df['Department'].isna() | df['Industry'].isna()]

    excel_writer = pd.ExcelWriter('filtered_Data.xlsx', engine='xlsxwriter')

    filtered_data.to_excel(excel_writer, index=False, sheet_name='Filtered Rows')

    excel_writer.close()

    experience_mapping = {
        range(0, 2): 'Analyst',
        range(2, 4): 'Senior Analyst',
        range(4, 6): 'Associate',
        range(6, 8): 'Senior Associate',
        range(8, 40): 'Engagement Manager'
    }
    

    for index, row in df.iterrows():
        if pd.isnull(row['Position Applied']):
            years_of_experience = row['Total Experience - Years']
            for experience_range, position in experience_mapping.items():
                if years_of_experience in experience_range:
                    df.loc[index, 'Position Applied'] = position
                    break

    mean_gpa = df['GPA / GPA Equivalent'].mean()
    missing_gpa = df['GPA / GPA Equivalent'].isnull()
    df.loc[missing_gpa, 'GPA / GPA Equivalent'] = mean_gpa
    filtered_data = df[df['Department'].isna() | df['Industry'].isna()]

    excel_writer = pd.ExcelWriter('filtered_Data.xlsx', engine='xlsxwriter')

    filtered_data.to_excel(excel_writer, index=False, sheet_name='Filtered Rows')

    excel_writer.close()

    experience_mapping = {
        range(0, 2): 'Analyst',
        range(2, 4): 'Senior Analyst',
        range(4, 6): 'Associate',
        range(6, 8): 'Senior Associate',
        range(8, 40): 'Engagement Manager'
    }

    for index, row in df.iterrows():
        if pd.isnull(row['Position Applied']):
            years_of_experience = row['Total Experience - Years']
            for experience_range, position in experience_mapping.items():
                if years_of_experience in experience_range:
                    df.loc[index, 'Position Applied'] = position
                    break

    top_10_values = df['Industry'].value_counts().head(22).index.to_list()
    print("Top 22 occurring values in the 'Industry' column:")
    print(top_10_values)
    filtered_df = df[~df['Industry'].isin(top_10_values)] 

    output_file_path = 'filled_Data.xlsx'  

    filtered_df.to_excel(output_file_path, index=False)
    top_10_values = df['Department'].value_counts().head(10).index.to_list()
    print("Top 22 occurring values in the 'Industry' column:")
    print(top_10_values)
    filtered_df = df[~df['Department'].isin(top_10_values)] 

    output_file_path = 'filled_data_Department.xlsx'  

    filtered_df.to_excel(output_file_path, index=False)

    mapping_df = pd.read_excel('Dept Industry Mapping.xlsx', sheet_name='Department')


    for _, row in mapping_df.iterrows():
        department_value = row['Department']
        mapping_value = row['Map']
        if pd.isna(department_value):
            continue

        matching_rows = df[df['Department'] == department_value]

        df.loc[matching_rows.index, 'Department'] = mapping_value

        

    mapping_df = pd.read_excel('Dept Industry Mapping.xlsx', sheet_name='Industry')


    for _, row in mapping_df.iterrows():
        department_value = row['Industry']
        mapping_value = row['Map to']
        if pd.isna(department_value):
            continue

        matching_rows = df[df['Industry'] == department_value]

        df.loc[matching_rows.index, 'Industry'] = mapping_value


    corc = df[['Area of Study', 'Degree/Qualification', 'Position Applied', 'Department']]
    corc_cleaned = corc.dropna()

    categorical_columns = corc_cleaned.columns[corc_cleaned.dtypes == object].drop('Department')

    association_results = {}
    for column in categorical_columns:
        contingency_table = pd.crosstab(corc_cleaned['Department'], corc_cleaned[column])
        chi2, p_value, _, _ = chi2_contingency(contingency_table)
        association_results[column] = {'chi2': chi2, 'p-value': p_value}

    best_option = min(association_results, key=lambda x: association_results[x]['p-value'])
    # print(best_option)
    mapped_values = corc_cleaned[[best_option, 'Department']].drop_duplicates().reset_index(drop=True)

    department_mapping = dict(mapped_values.values)
    # print(department_mapping)
    i = 0
    for index, row in df.iterrows():
        if pd.isna(row['Department']):
            # print('he')
            correlated_value = row[best_option]
            # print(correlated_value.split(';')[0])
            
            if correlated_value.split(';')[0] in department_mapping:
                i+=1
                # print('here')
                df.at[index, 'Department'] = department_mapping[correlated_value.split(';')[0]]


    corc = df[['Area of Study', 'Degree/Qualification', 'Position Applied','Industry']]
    corc_cleaned = corc.dropna()

    categorical_columns = corc_cleaned.columns[corc_cleaned.dtypes == object].drop('Industry')

    association_results = {}
    for column in categorical_columns:
        contingency_table = pd.crosstab(corc_cleaned['Industry'], corc_cleaned[column])
        chi2, p_value, _, _ = chi2_contingency(contingency_table)
        association_results[column] = {'chi2': chi2, 'p-value': p_value}

    best_option = min(association_results, key=lambda x: association_results[x]['p-value'])
    # print(best_option)
    mapped_values = corc_cleaned[[best_option, 'Industry']].drop_duplicates().reset_index(drop=True)

    department_mapping = dict(mapped_values.values)
    # print(department_mapping)
    i = 0
    for index, row in df.iterrows():
        if pd.isna(row['Industry']):
            # print('he')
            correlated_value = row[best_option]

            # print(correlated_value)
            # try:
            if correlated_value.split(';')[0] in department_mapping:
                i+=1
                # print('here')
                df.at[index, 'Industry'] = department_mapping[correlated_value.split(';')[0]]
    

    df['consulting_exp_yes_no'] = np.where(df['Consulting Experience'].notna(), 1, 0)
    df['referal_yes_no'] = np.where(df['Consulting Experience'].notna(), 1, 0)

    # df = df.drop(columns= 'Consulting Experience')
    new_cands = df[df['Status'] == 'New']
    df = df[df['Status'] != 'New']
    df['Additional Languages'] = df['Additional Languages'].fillna('English')
    df['Additional Languages'] = df['Additional Languages'].str.replace(r',+$', 'English', regex=True)
    df['num_langs'] = df['Additional Languages'].str.split(',').apply(lambda x: len(x))
    df = df.drop(columns= 'Additional Languages')
    df['University Name']=df['University Name'].replace(['Lahore University of Management Sciences, Lahore'],'Lahore University of Management Sciences')
    df['University Name']=df['University Name'].replace(['Institute of Business Administration, Karachi'],'Institute of Business Administration')
    df['University Name']=df['University Name'].replace(['Lahore School of Economics, Lahore'],'Lahore School of Economics')
    df['Degree/Qualification']=df['Degree/Qualification'].replace(['Bachelor of Science (B.S.)'],'Bachelor of Science (BS)')
    df['Area of Study'] = df['Area of Study'].str.rstrip(';')
    df = df[df['Status'] != 'Cancelled Application']
    
    upload_choice1 = st.radio('Do you want to add date filter?', ('No', 'Yes'))
    if upload_choice1 =='Yes':
        start_date = st.date_input("Pick start Date", datetime.date(2019, 7, 6))
        end_date = st.date_input("Pick end Date", datetime.date(2022,7,1))
        df['Created Time'] = pd.to_datetime(df['Created Time']).dt.date
        
        df = df[(df['Created Time'] >= start_date) & (df['Created Time'] <= end_date)]

    # Display the filtered DataFrame

    # Stage_1 = ['Rejected - Screening']
    # Stage_2 = ['Rejected - Screening','Rejected - Assessment']
    # Stage_3 = ['Rejected - Screening','Rejected - Assessment','Assessment - invited','Rejected - Interview 1']
    # Stage_4 = ['Rejected - Screening','Rejected - Assessment','Assessment - invited','Rejected - Interview 1','Round 1 - invited','Round 1 - Interview Booked','Rejected - Interview 2']
    # Stage_5 = ['Rejected - Screening','Rejected - Assessment','Assessment - invited','Rejected - Interview 1','Round 1 - invited','Round 1 - Interview Booked','Rejected - Interview 2','Round 2 - Invited']
    stage = st.selectbox("Select a stage", ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"])

    # Define the replacement values based on the selected stage
    if stage == "Stage 1":
        replacement_values = ['Rejected - Screening']
    elif stage == "Stage 2":
        replacement_values = ['Rejected - Screening', 'Rejected - Assessment']
    elif stage == "Stage 3":
        replacement_values = ['Rejected - Screening', 'Rejected - Assessment', 'Assessment - invited', 'Rejected - Interview 1']
    elif stage == "Stage 4":
        replacement_values = ['Rejected - Screening', 'Rejected - Assessment', 'Assessment - invited', 'Rejected - Interview 1', 'Round 1 - invited', 'Round 1 - Interview Booked', 'Rejected - Interview 2']
    elif stage == "Stage 5":
        replacement_values = ['Rejected - Screening', 'Rejected - Assessment', 'Assessment - invited', 'Rejected - Interview 1', 'Round 1 - invited', 'Round 1 - Interview Booked', 'Rejected - Interview 2', 'Round 2 - Invited']
    # Get the list of column names
    df['Status'] = df['Status'].apply(lambda x: 0 if x in replacement_values else 1)
    st.write('Number of Applicants who have passed this stage: ',len(df[df['Status'] == 1]))
    st.write('Number of Applicants who have failed this stage: ',len(df[df['Status'] == 0]))
    st.write('Percentage Accepted: ',round(100*len(df[df['Status'] == 1])/(len(df[df['Status'] == 0])+len(df[df['Status'] == 1])),2),'%')
    status_labels = {1: 'Accepted', 0: 'Rejected'}
    position_counts = df['Position Applied'].value_counts()

    st.subheader("Bar Chart for Position Applied")
    fig = px.bar(position_counts, x=position_counts.index, y=position_counts.values, labels={'x': 'Position', 'y': 'Count'})
    st.plotly_chart(fig)
    df['Position Applied']=df['Position Applied'].replace(['Senior_Analyst','Senior Analyst'],'Analyst')
    df['Position Applied']=df['Position Applied'].replace(['Senior_Associate','Senior Associate'],'Associate')
    df['Position Applied']=df['Position Applied'].replace(['Engagement_Manager','Engagement Manager'],'Associate')
    df['Status_Label'] = df['Status'].map(status_labels)

    # Calculate status counts
    status_counts = df['Status_Label'].value_counts()

    # Create a DataFrame for plotly
    chart_data = pd.DataFrame({'Status': status_counts.index, 'Count': status_counts.values})

    # Create the pie chart using plotly
    fig = px.pie(chart_data, values='Count', names='Status', title='Accepted vs Rejected in at this stage')

    # Make the pie chart touchable
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Display the pie chart using Streamlit
    st.plotly_chart(fig)

    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]

    # Count the positions for accepted and rejected
    position_counts = pd.concat(
        [df_accepted['Position Applied'].value_counts().rename('accepted'),
         df_rejected['Position Applied'].value_counts().rename('rejected')],
        axis=1)

    # Create the bar chart using plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=position_counts.index, y=position_counts['accepted'], name='Accepted'))
    fig.add_trace(go.Bar(x=position_counts.index, y=position_counts['rejected'], name='Rejected'))

    fig.update_layout(title='Comparison of Accepted and Rejected Positions at this stage',
                      xaxis_title='Position',
                      yaxis_title='Count')

    # Display the bar chart using Streamlit
    st.plotly_chart(fig)
    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]

    # Group the accepted and rejected DataFrames by 'Position Applied'
    accepted_grouped = df_accepted.groupby('Position Applied').size()
    rejected_grouped = df_rejected.groupby('Position Applied').size()

    # Get the unique positions applied
    positions = df['Position Applied'].unique()

    # Create individual pie charts for each position
    for position in positions:
        accepted_count = accepted_grouped.get(position, 0)
        rejected_count = rejected_grouped.get(position, 0)
        total_count = accepted_count + rejected_count
        accepted_percent = accepted_count / total_count * 100
        rejected_percent = rejected_count / total_count * 100

        # Create the pie chart using plotly
        fig = go.Figure(data=[go.Pie(labels=['Accepted', 'Rejected'],
                                     values=[accepted_count, rejected_count],
                                     textinfo='percent',
                                     hovertemplate='Count: %{value}<br>Percentage: %{percent:.1f}%')])

        fig.update_layout(title=f"Position: {position}")

        # Display the pie chart using Streamlit
        st.plotly_chart(fig)
    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]

    # Count the positions for accepted and rejected by gender
    accepted_counts = df_accepted['Gender'].value_counts()
    rejected_counts = df_rejected['Gender'].value_counts()

    # Get all unique genders
    genders = df['Gender'].unique()

    # Create a bar chart for accepted and rejected positions by gender using plotly
    fig = go.Figure()
    for gender in genders:
        accepted_count = accepted_counts.get(gender, 0)
        rejected_count = rejected_counts.get(gender, 0)
        fig.add_trace(go.Bar(name=gender, x=['Accepted', 'Rejected'], y=[accepted_count, rejected_count]))

    fig.update_layout(title='Comparison of Accepted and Rejected Positions Applied Screening',
                      xaxis_title='Position',
                      yaxis_title='Count')

    # Display the bar chart using Streamlit
    st.plotly_chart(fig)
    
    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]
    accepted_grouped = df_accepted.groupby(['Position Applied', 'Gender']).size().unstack()
    rejected_grouped = df_rejected.groupby(['Position Applied', 'Gender']).size().unstack()

    # Get the unique positions applied
    positions = df['Position Applied'].unique()

    # Create a dropdown to select the position
    selected_position = st.selectbox('Select a Position', positions)

    # Retrieve the data for the selected position
    male_accepted_count = accepted_grouped.loc[selected_position, 'Male']
    male_rejected_count = rejected_grouped.loc[selected_position, 'Male']
    male_total_count = male_accepted_count + male_rejected_count

    female_accepted_count = accepted_grouped.loc[selected_position, 'Female']
    female_rejected_count = rejected_grouped.loc[selected_position, 'Female']
    female_total_count = female_accepted_count + female_rejected_count

    # Create the pie chart
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Male Pie Chart
    ax1 = axes[0]
    if pd.isna(male_accepted_count) or pd.isna(male_rejected_count) or pd.isna(male_total_count):
        ax1.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax1.axis('off')
    else:
        male_accepted_percent = (male_accepted_count / male_total_count) * 100
        male_rejected_percent = (male_rejected_count / male_total_count) * 100
        ax1.pie([male_accepted_percent, male_rejected_percent], labels=['Accepted', 'Rejected'],
                autopct=lambda p: f'{p:.1f}%\n({int(male_total_count * p / 100)})', startangle=90)
        ax1.set_title(f"Position Applied: {selected_position} (Male)")
        ax1.axis('equal')

    # Female Pie Chart
    ax2 = axes[1]
    if pd.isna(female_accepted_count) or pd.isna(female_rejected_count) or pd.isna(female_total_count):
        ax2.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax2.axis('off')
    else:
        female_accepted_percent = (female_accepted_count / female_total_count) * 100
        female_rejected_percent = (female_rejected_count / female_total_count) * 100
        ax2.pie([female_accepted_percent, female_rejected_percent], labels=['Accepted', 'Rejected'],
                autopct=lambda p: f'{p:.1f}%\n({int(female_total_count * p / 100)})', startangle=90)
        ax2.set_title(f"Position Applied: {selected_position} (Female)")
        ax2.axis('equal')

    # Display the chart
    st.pyplot(fig)
    d = dict()
    categories = ['0-2 Years', '2-5 Years', '5-10 Years', '10+ Years']

    df['Experience Category'] = pd.cut(df['Total Experience - Years'], bins=[0, 2, 5, 10, np.inf], labels=categories, right=False)

    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]

    accepted_grouped = df_accepted.groupby(['Position Applied', 'Experience Category']).size().unstack()
    rejected_grouped = df_rejected.groupby(['Position Applied', 'Experience Category']).size().unstack()

    # Get the unique positions applied
    positions = df['Position Applied'].unique()

    # Create side-by-side pie charts for each position applied, differentiated by experience category
    for position in positions:
        fig, axes = plt.subplots(1, 4, figsize=(30, 5))
        
        for i, category in enumerate(categories):
            ax = axes[i]
            accepted_count = accepted_grouped.loc[position, category]
            rejected_count = rejected_grouped.loc[position, category]
            total_count = accepted_count + rejected_count
            
            if np.isnan(accepted_count) or np.isnan(rejected_count) or np.isnan(total_count):
                ax.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', fontsize=24)
                ax.axis('off')
            else:
                accepted_percent = (accepted_count / total_count) * 100
                rejected_percent = (rejected_count / total_count) * 100
                ax.pie([accepted_percent, rejected_percent], labels=['Accepted', 'Rejected'],
                        autopct=lambda p: f'{p:.1f}%\n({math.ceil(total_count * p / 100)})', startangle=90,
                        textprops={'fontsize': 24})  # Increase the font size
                ax.set_title(f"Position Applied: {position}\nExperience: {category}", fontsize=24)  # Increase the font size
                ax.axis('equal')
        
        plt.suptitle("Accepted and Rejected Applicants by Experience Category", fontsize=34, y=1.05)
        plt.tight_layout()
    # Display the figure using Streamlit
        st.pyplot(fig)
    print(d)
    for position in positions[:1]:
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Accepted Pie Chart
        ax1 = axes[0]
        accepted_counts = accepted_grouped.loc[position]
        total_accepted_count = accepted_counts.sum()
        if np.isnan(total_accepted_count) or accepted_counts.isnull().all():
            ax1.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', fontsize=16)
            ax1.axis('off')
        else:
            accepted_percentages = (accepted_counts / total_accepted_count) * 100
            ax1.pie(accepted_percentages, labels=accepted_counts.index,
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})  # Increase the font size
            
            ax1.set_title(f"Position Applied: {position}\nAccepted Applicants", fontsize=16)  # Increase the font size
            ax1.axis('equal')
        
        # Rejected Pie Chart
        ax2 = axes[1]
        rejected_counts = rejected_grouped.loc[position]
        total_rejected_count = rejected_counts.sum()
        if np.isnan(total_rejected_count) or rejected_counts.isnull().all():
            ax2.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', fontsize=16)
            ax2.axis('off')
        else:
            rejected_percentages = (rejected_counts / total_rejected_count) * 100
            ax2.pie(rejected_percentages, labels=rejected_counts.index,
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})  # Increase the font size
            ax2.set_title(f"Position Applied: {position}\nRejected Applicants", fontsize=16)  # Increase the font size
            ax2.axis('equal')
        
        plt.suptitle("Accepted and Rejected Applicants by University Name (Top 4 Universities)", fontsize=18, y=1.05)  # Increase the font size
        plt.tight_layout()
        
        # Display the figure using Streamlit
        st.pyplot(fig)

    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]
    st.title("Pie charts for Top 4 values from the selected column and filter based on Position Applied")

    # Get the top 5 universities based on count of applicants
    columns = ['University Name', 'Degree/Qualification', 'Area of Study','School Qualification','Department','Industry','num_langs','Were you referred by anyone?','consulting_exp_yes_no']
    selected_column = st.selectbox('Select a column', columns)
    x = [1, 2, 3, 4, 5,6,7,8,9,10]

    if selected_column == 'consulting_exp_yes_no' or selected_column == 'Were you referred by anyone?':
        x = [1,2]

    # Select how many top values to display
    selected_column1 = st.selectbox(f"How many {selected_column} do you want?", x)
    top_5_universities = df[selected_column].value_counts().nlargest(selected_column1).index.tolist()

    # Get the unique positions applied
    positions = df['Position Applied'].unique()
    position = st.selectbox('Select a position', positions)

    # Iterate over each position and each university
    # for position in selected_position:
        # print(position)
    for university in top_5_universities:
        
        # Filter the DataFrame for the specific position and university
        df_position_uni = df[(df['Position Applied'] == position) & (df[selected_column] == university)]
        
        # Count the number of accepted and rejected applicants
        accepted_count = df_position_uni[df_position_uni['Status'] == 1].shape[0]
        rejected_count = df_position_uni[df_position_uni['Status'] == 0].shape[0]
        total_count = accepted_count + rejected_count
        
        # Calculate the percentages
        accepted_percentage = (accepted_count / total_count) * 100
        rejected_percentage = (rejected_count / total_count) * 100
        
        # Create labels and values for the pie chart
        labels = ['Accepted', 'Rejected']
        values = [accepted_count, rejected_count]
        percentages = [accepted_percentage, rejected_percentage]
        
        # Create a pie chart using Plotly
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        
        # Add custom hovertext with count and percentage information
        hovertext = [f'{label}: {value} ({percentage:.1f}%)' for label, value, percentage in zip(labels, values, percentages)]
        fig.update_traces(hovertext=hovertext, textposition='outside', textinfo='label+percent')
        
        # Customize the layout and appearance
        fig.update_layout(
            title=f"Position: {position}<br>{selected_column}: {university}<br>Total Applicants: {total_count}",
            title_font_size=18,
            font_size=14,
            height=500,
            width=500,
            showlegend=False
        )
        
        # Display the plotly figure using Streamlit
        d[university]=[accepted_count,rejected_count,total_count]

        st.plotly_chart(fig)
    print(d)
    percentages = {}
    for key, values in d.items():
        accepted = values[0]
        total = values[-1]
        percentage = (accepted / total) * 100
        percentages[key] = percentage

    # Convert the data into lists
    keys = list(percentages.keys())
    values = list(percentages.values())

    # Create the bar chart using Plotly
    fig = go.Figure(data=go.Bar(x=keys, y=values))

    # Customize the layout
    fig.update_layout(
        title='Percentage of Accepted Applicants',
        xaxis_title='Degree',
        yaxis_title='Percentage Accepted'
    )

    # Render the chart using Streamlit
    st.plotly_chart(fig)
    percentages = {}
    for key, values in d.items():
        accepted = values[1]
        total = values[-1]
        percentage = (accepted / total) * 100
        percentages[key] = percentage

    # Convert the data into lists
    keys = list(percentages.keys())
    values = list(percentages.values())

    # Create the bar chart using Plotly
    fig = go.Figure(data=go.Bar(x=keys, y=values))

    # Customize the layout
    fig.update_layout(
        title='Percentage of Rejected Applicants',
        xaxis_title='Degree',
        yaxis_title='Percentage Rejected'
    )

    # Render the chart using Streamlit
    st.plotly_chart(fig)
    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]

    # Define the numerical range bins and labels for GPA/GPA Equivalent
    gpa_bins = [0, 2, 2.5, 3, 3.2, 3.4, 3.6, 3.8, 4, float('inf')]
    gpa_labels = ['<2.0', '2.0-2.49', '2.5-2.99', '3.0-3.19', '3.2-3.39', '3.4-3.59', '3.6-3.79', '3.8-3.99', '4.0+']

    # Get the unique positions applied
    positions = df['Position Applied'].unique()

    # Initialize Streamlit page
    st.title("Numerical Range Plots for GPA/GPA Equivalent")

    # Iterate over each position and create the numerical range plot for GPA/GPA Equivalent
    for position in positions:
        # Filter the DataFrame for the specific position
        df_position = df[df['Position Applied'] == position]
        
        # Assign GPA ranges to each row
        df_position['GPA Range'] = pd.cut(df_position['GPA / GPA Equivalent'], bins=gpa_bins, labels=gpa_labels, right=False)
        
        # Group by GPA Range and count the number of accepted and rejected applicants
        group_counts = df_position.groupby(['GPA Range', 'Status']).size().unstack(fill_value=0)
        
        # Reset the index to convert the group_counts DataFrame to long format
        group_counts = group_counts.reset_index()
        group_counts = group_counts.melt(id_vars='GPA Range', var_name='Status', value_name='Count')
        group_counts['Status'] = group_counts['Status'].map({0: 'Rejected', 1: 'Accepted'})

        
        # Create the numerical range plot using Plotly
        fig = px.bar(group_counts, x='GPA Range', y='Count', color='Status', barmode='group',
                    labels={'GPA Range': 'GPA Range', 'Count': 'Count', 'Status': 'Status'},
                    title=f"Position: {position}\nNumerical Range Plot: GPA/GPA Equivalent")
        
        # Display the plot in Streamlit
        st.plotly_chart(fig)
    top_universities = df['University Name'].value_counts().nlargest(5).index

# Filter the DataFrame for the top 5 universities
    top_universities = df['University Name'].value_counts().nlargest(5).index

    # Filter the DataFrame for the top 5 universities
    df_top_universities = df[df['University Name'].isin(top_universities)]

    # Group the data by 'University Name', 'Position Applied', and calculate the average assessment score
    grouped_data = df_top_universities.groupby(['University Name', 'Position Applied'])['Assessment Overall Score'].mean().reset_index()

    # Create a bar plot for each position applied, showing the average assessment score for the top 5 universities
    for position in df_top_universities['Position Applied'].unique():
        data = grouped_data[grouped_data['Position Applied'] == position]
        fig = px.bar(data, x='University Name', y='Assessment Overall Score', color='University Name',
                    labels={'Assessment Overall Score': 'Average Assessment Score'},
                    title=f'Average Assessment Score for Position: {position}')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
    column_names = df.columns.tolist()
    column_names = df.columns.tolist()

    # Dropdown menu to select number of columns for the new DataFrame
    num_columns = st.selectbox("Select number of columns for new DataFrame", range(1, len(column_names) + 1))

    if num_columns:
        # Multiselect to choose columns for the new DataFrame
        selected_columns = st.multiselect("Select columns", column_names, key="multiselect")

        if selected_columns and len(selected_columns) == num_columns:
            # Create a new DataFrame with the selected columns
            new_df = df[selected_columns]

            # Display the new DataFrame
            st.write(new_df)
    # Multiselect to select multiple columns
    correlation_heat_map = df[['University Name', 'Degree/Qualification','Assessment Overall Score','GPA / GPA Equivalent', 'Area of Study','Department','Industry','num_langs','Were you referred by anyone?','consulting_exp_yes_no','Status']]
    color_maps = ['Blues', 'Greens', 'Oranges', 'Purples']
    columnss = ['University Name', 'Degree/Qualification', 'Area of Study','Department','Industry','num_langs','Were you referred by anyone?','consulting_exp_yes_no']
    selected = st.selectbox('Select a column', columnss)
    # Step 2: Select the top 4 universities
    top_4_universities = correlation_heat_map[selected].value_counts().index[:4]

    # Iterate over each university
    for i, university in enumerate(top_4_universities):
        one_hot_encoded_df = pd.get_dummies(correlation_heat_map[selected].where(df[selected] == university))
        encoded_df = pd.concat([one_hot_encoded_df, correlation_heat_map['Assessment Overall Score'], correlation_heat_map['GPA / GPA Equivalent'], correlation_heat_map['Status']], axis=1)
        correlation_matrix = encoded_df.corr()

        # Create Plotly heatmap figure
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale=color_maps[i],
            colorbar=dict(title="Correlation"),
        ))

        # Add annotations to show correlation values
        for i, row in enumerate(correlation_matrix.values):
            for j, val in enumerate(row):
                fig.add_annotation(
                    x=correlation_matrix.columns[j],
                    y=correlation_matrix.columns[i],
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(color="white" if abs(val) > 0.5 else "black"),
                )

        # Update layout
        fig.update_layout(
            title=f"Correlation Heatmap - {university}",
            xaxis=dict(title="Variables"),
            yaxis=dict(title="Variables"),
        )

        # Display the plotly figure using Streamlit
    st.plotly_chart(fig)
    df_accepted = df[df['Status'] == 1]
    df_rejected = df[df['Status'] == 0]
    value_counts = df_accepted['Consulting Experience'].value_counts().head(5)

# Create a pie chart
    plt.figure(figsize=(8, 8))
    sns.set(style="whitegrid")
    sns.set_palette("pastel")
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)

    # Add a title
    plt.title("Percentage of Accepted People in Each Consulting Experience Category")

    # Display the pie chart in Streamlit
    st.pyplot(plt)
    value_counts = df_rejected['Consulting Experience'].value_counts().head(5)

# Create a pie chart
    plt.figure(figsize=(8, 8))
    sns.set(style="whitegrid")
    sns.set_palette("pastel")
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)

    # Add a title
    plt.title("Percentage of Rejected People in Each Consulting Experience Category")

    # Display the pie chart in Streamlit
    st.pyplot(plt)
    value_counts = df['How did you hear about Intellia?'].value_counts().head(5)

    plt.figure(figsize=(8, 8))
    sns.set(style="whitegrid")
    sns.set_palette("pastel")
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)

    # Add a title
    plt.title("Percentage of People in by 'How did you hear about Intellia?'")

    # Display the pie chart in Streamlit
    st.pyplot(plt)

if __name__ == '__main__':
    credentials = toml.load("credentials.toml")["credentials"]

    # Define the correct username and password hash
    correct_username_hash = credentials["username_hash"]
    correct_password_hash = credentials["password_hash"]

    # Store a flag to track if authentication is successful
    authenticated = False
    st.image("Group 3523.jpg")

    # Prompt the user to enter their username and password
    placeholder = st.empty()
    with placeholder.container():
        username = st.text_input("Enter your username:", key="username_input")
        password = st.text_input("Enter your password:", type="password", key="password_input")
        s = st.button("Login")
    if s:
        # Hash the entered username and password
        entered_username_hash = hashlib.sha256(username.encode()).hexdigest()
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Verify the entered username and password against the stored hashes
        if entered_username_hash == correct_username_hash and entered_password_hash == correct_password_hash:
            authenticated = True
   
            # Clear the current page
            

            placeholder.empty()            
            main()
        elif entered_username_hash == correct_username_hash:
            st.error("Incorrect password. Please try again.")
        else:
            st.error("Username does not exist.")
    
    # Conditionally render the username and password fields

