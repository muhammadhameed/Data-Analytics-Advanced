import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import numpy as np
from scipy import stats
from sklearn import preprocessing,metrics
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from matplotlib.backends.backend_pdf import PdfPages

def read_excel(filename):
    df = pd.read_excel(filename)
    df = df.dropna(how='all', axis=1)
    return df


df = read_excel("data.xlsx")
df2 = read_excel("zohodata.xlsx")
df2=df2.drop(['Candidate Id',
            'Area of Study',
            'Candidate ID',
            'Candidate Stage',
            'Fresh Candidate',
            'Reason for Rejected Offer',
            'Round 3 Interviewer',
            'Round 1 Notes',
            'Round 2 Interviewer',
            'Is Attachment Present',
            'First Name',
            'Last Name',
            'Full Name',
            "Email",
            "Mobile",
            "City",
            'Created By',
            'Modified By',
            'Created Time',
            'Modified Time',
            'Last Activity Time',
            'Last emailed',
            'Associated any Social Profiles',
            'Candidate Owner ID',
            'Source',
            'Is Hot Candidate',
            'Is Locked',
            'Candidate Status',
            'Career Page Invite Status',
            'Layout',
            'Opt-In Status',
            'I Agree',
            'Origin',
            'Area',
            'Univ. Start Date',
            'Univ. End Date',
            'School Start Date',
            'School End Date',
            'Work Start Date',
            'Work End Date',
            'Previously Worked Start Date',
            'Referral Name',
            'Previously Worked End Date',
            'LinkedIn',
            'Round 1 Interview date',
            'Round 1 Interviewer',
            'Round 2 Interview date',
            'Notice Period / Joining date',
            'Round 3 Interview Date',
            'CV',
            'University End Date',
            'Email Opt Out',
            'Candidate Rating',
            'Number of Applications',
            'Round 2 Notes',
            'Is Unqualified',
            'Do you know anyone who is working at Intellia',
            'Round 2 Decision',
            'Current Compensation',
            'Round 1 Decision',
            'Position Fit',
            'Relocation or Remote (if based out of Lahore)',
            'Round 3 Decision',
            'Round 3 Notes',
            'If rejected, reason for rejecting',
            'Offer Status',
            'Business judgement',
            'Working with data',
            'Problem solving',
            'Microsoft Excel (advanced)',
            'Country of Employment',
            'Skills',
            'Experience Level',
            'Nationality',
            'I work here',
            ], axis=1)

combined_df=pd.merge(
    df,
    df2,
    how="inner",
    on=['Country',
  'University Name',
  'School',
  'School Qualification',
  'Job Title',
  'Employer',
  'Degree/Qualification',
  'GPA / GPA Equivalent',
  'Additional Languages',
  'Status',
  'Position Applied',
  'Have you previously worked at Intellia',
  'Were you referred by anyone?',
  'Total Experience - Years',
  'Overall Score',
  'Department',
  'Industry'],

)

avg_gpa=round(combined_df['GPA / GPA Equivalent'].dropna().mean(), 2)
avg_score=round(combined_df['Overall Score'].dropna().mean(), 0)
combined_df['Have you previously worked at Intellia']=combined_df['Have you previously worked at Intellia'].fillna(0)
combined_df['Country']=combined_df['Country'].fillna('Pakistan')
combined_df['University Name']=combined_df['University Name'].fillna('Lahore University of Management Sciences')
combined_df['GPA / GPA Equivalent']=combined_df['GPA / GPA Equivalent'].fillna(avg_gpa)
combined_df['Additional Languages']=combined_df['Additional Languages'].fillna('English')
combined_df['Were you referred by anyone?']=combined_df['Were you referred by anyone?'].fillna('No')
combined_df['Overall Score']=combined_df['Overall Score'].fillna(avg_score)
combined_df['Total Experience - Years']=combined_df['Total Experience - Years'].fillna(0)
combined_df['School Qualification']=combined_df['School Qualification'].replace(['GCE A-levels','A-Levels','IGCSE A Levels'],'A-Levels')
combined_df['Were you referred by anyone?']=combined_df['Were you referred by anyone?'].replace(['No', 'Yes'],[0,1])


combined_df['Have you previously worked at Intellia']=combined_df['Have you previously worked at Intellia'].replace(['No', 'Yes'],[0,1])

replacement_values = ['Rejected - Screening']

combined_df['Status'] = combined_df['Status'].apply(lambda x: 0 if x in replacement_values else 1)

combined_df['GPA / GPA Equivalent']=combined_df['GPA / GPA Equivalent'].replace(33,3)
print(combined_df)
combined_df['Position Applied']=combined_df['Position Applied'].replace(['Senior_Analyst','Senior Analyst'],'Senior Analyst')
combined_df['Position Applied']=combined_df['Position Applied'].replace(['Senior_Associate','Senior Associate'],'Senior Associate')
combined_df['Position Applied']=combined_df['Position Applied'].replace(['Engagement_Manager','Engagement Manager'],'Engagement Manager')

df_accepted=combined_df[combined_df['Status']==1]
df_rejected=combined_df[combined_df['Status']==0]
pp = PdfPages('Data_Plots.pdf')
all_dfs=[]
position_all=pd.concat(
    [df_accepted['Position Applied'].value_counts().rename('accepted'), df_rejected['Position Applied'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(position_all.plot(kind='bar', title='Comparison of Accepted and Rejected Positions Applied').get_figure(),bbox_inches='tight')

position_all['rejected']=position_all['rejected'].fillna(0)
position_all['accepted']=position_all['accepted'].fillna(0)
position_all['total']=position_all['rejected']+position_all['accepted']
position_all['Accepted%']=(position_all['accepted']/position_all['total'])*100
pp.savefig(position_all['Accepted%'].plot(kind='bar', title='Position percentage accepted').get_figure(),bbox_inches='tight')
all_dfs.append(position_all)
department=pd.concat(
    [df_accepted['Department'].value_counts().rename('accepted'), df_rejected['Department'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(department.head(10).plot(kind='bar', title='Comparison of applicants Departments Applied').get_figure(),bbox_inches='tight')

position_accepted = (df_accepted['Department'].value_counts()).head(10)
position_rejected = (df_rejected['Department'].value_counts()).head(10)

# Plotting the pie chart for accepted positions
plt.figure(figsize=(8, 6))  # Adjust the figure size as desired
plt.pie(position_accepted, labels=position_accepted.index, autopct='%1.1f%%')

plt.title('Accepted Departments')
plt.axis('equal')  
pp.savefig(bbox_inches='tight')

# plt.show()
plt.figure(figsize=(8, 6))  # Adjust the figure size as desired
plt.pie(position_rejected, labels=position_rejected.index, autopct='%1.1f%%')

plt.title('Rejected Departments')
plt.axis('equal')  # Ensures the pie chart is circular

# Save the figure to PDF using PdfPages

pp.savefig(bbox_inches='tight')
department['rejected']=department['rejected'].fillna(0)
department['accepted']=department['accepted'].fillna(0)
department['total']=department['rejected']+department['accepted']
department['Accepted%']=(department['accepted']/department['total'])*100
department=department[(department['Accepted%']!=0) & (department['total']>10)]
department['Accepted%'].plot(kind='bar', title='percentage accepted')
pp.savefig(department['Accepted%'].plot(kind='bar', title='Departments percentage accepted').get_figure(),bbox_inches='tight')
all_dfs.append(department)
all_jobs=pd.concat(
    [df_accepted['Industry'].value_counts().rename('accepted'), df_rejected['Industry'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(all_jobs[0:7].plot(kind='bar', title='Industry of Employers Comparison').get_figure(),bbox_inches='tight')
all_jobs['rejected']=all_jobs['rejected'].fillna(0)
all_jobs['accepted']=all_jobs['accepted'].fillna(0)
all_jobs['total']=all_jobs['rejected']+all_jobs['accepted']
all_jobs['Accepted%']=(all_jobs['accepted']/all_jobs['total'])*100
all_jobs['Rejected%']=(all_jobs['rejected']/all_jobs['total'])*100

all_jobs=all_jobs[(all_jobs['Accepted%']!=0) & (all_jobs['total']>10)]
pp.savefig(all_jobs['Accepted%'].plot(kind='bar', title='Accepted industry percentage').get_figure(),bbox_inches='tight')
all_dfs.append(all_jobs)
all_unis=pd.concat(
    [df_accepted['University Name'].value_counts().rename('accepted'), df_rejected['University Name'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(all_unis[0:10].plot(kind='bar', title='University Comparison').get_figure(),bbox_inches='tight')
all_unis['rejected']=all_unis['rejected'].fillna(0)
all_unis['accepted']=all_unis['accepted'].fillna(0)
all_unis['total']=all_unis['rejected']+all_unis['accepted']
all_unis['Accepted%']=(all_unis['accepted']/all_unis['total'])*100
all_unis=all_unis[(all_unis['Accepted%']!=0) & (all_unis['total']>10)]
all_unis['Accepted%'].plot(kind='bar', title='percentage accepted')
pp.savefig(all_unis['Accepted%'].plot(kind='bar', title='Accepted University Percentage').get_figure(),bbox_inches='tight')
all_dfs.append(all_unis)
all_school_qualifications=pd.concat(
    [df_accepted['School Qualification'].value_counts().rename('accepted'), df_rejected['School Qualification'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(all_school_qualifications[0:10].plot(kind='bar', title='School Qualification Comparison').get_figure(),bbox_inches='tight')
all_school_qualifications['rejected']=all_school_qualifications['rejected'].fillna(0)
all_school_qualifications['accepted']=all_school_qualifications['accepted'].fillna(0)
all_school_qualifications['total']=all_school_qualifications['rejected']+all_school_qualifications['accepted']
all_school_qualifications['Accepted%']=(all_school_qualifications['accepted']/all_school_qualifications['total'])*100
all_school_qualifications=all_school_qualifications[(all_school_qualifications['Accepted%']!=0) & (all_school_qualifications['total']>10)]
pp.savefig(all_school_qualifications['Accepted%'].plot(kind='bar', title='Accepted School Qualifications percentage').get_figure(),bbox_inches='tight')
all_dfs.append(all_school_qualifications)
all_degrees=pd.concat(
    [df_accepted['Degree/Qualification'].value_counts().rename('accepted'), df_rejected['Degree/Qualification'].value_counts().rename('rejected')],
    axis=1)
pp.savefig(all_degrees[0:10].plot(kind='bar', title='Degree/Qualification Comparison').get_figure(),bbox_inches='tight')
all_degrees['rejected']=all_degrees['rejected'].fillna(0)
all_degrees['accepted']=all_degrees['accepted'].fillna(0)
all_degrees['total']=all_degrees['rejected']+all_degrees['accepted']
all_degrees['Accepted%']=(all_degrees['accepted']/all_degrees['total'])*100
all_degrees=all_degrees[(all_degrees['Accepted%']!=0) & (all_degrees['total']>10)]
pp.savefig(all_degrees['Accepted%'].plot(kind='bar', title='Accepted Degree percentages').get_figure(),bbox_inches='tight')
all_dfs.append(all_degrees)
all_gpa=pd.concat(
    [df_accepted['GPA / GPA Equivalent'].rename('accepted'), df_rejected['GPA / GPA Equivalent'].rename('rejected')],
    axis=1)
all_dfs.append(all_gpa.describe())
q1 = df_accepted['GPA / GPA Equivalent'].quantile(0.25)
q3 = df_accepted['GPA / GPA Equivalent'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

filtered_data = df_accepted[(df_accepted['GPA / GPA Equivalent'] >= lower_bound) & (df_accepted['GPA / GPA Equivalent'] <= upper_bound)]


plt.figure(figsize=(8, 6))  # Adjust the figure size as desired
plt.boxplot(filtered_data['GPA / GPA Equivalent'])

plt.title('Accepted Applicants GPA (Outliers Removed)')
plt.xlabel('GPA / GPA Equivalent')

pp.savefig(bbox_inches='tight')
pp.savefig(df_rejected['GPA / GPA Equivalent'].plot(kind='box', title='Rejected applicants GPA').get_figure(),bbox_inches='tight')
pp.savefig(all_gpa.plot(kind='box', title='Comparison applicants GPA').get_figure(),bbox_inches='tight')
all_years=pd.concat(
    [df_accepted['Total Experience - Years'].rename('accepted'), df_rejected['Total Experience - Years'].rename('rejected')],
    axis=1)

all_dfs.append(all_years.describe())
pp.savefig(df_accepted['Total Experience - Years'].plot(kind='box', title='Accepted Applicants Experience').get_figure(),bbox_inches='tight')
pp.savefig(df_rejected['Total Experience - Years'].plot(kind='box', title='Rejected applicants Experience').get_figure(),bbox_inches='tight')
pp.savefig(all_years.plot(kind='box', title='Comparison applicants Experience').get_figure(),bbox_inches='tight')
all_referals=pd.concat([df_accepted['Were you referred by anyone?'].value_counts().rename('accepted'), df_rejected['Were you referred by anyone?'].value_counts().rename('rejected')],axis=1)
pp.savefig(all_referals.plot(kind='bar', title='Referral Comparison').get_figure(),bbox_inches='tight')
all_referals['rejected']=all_referals['rejected'].fillna(0)
all_referals['accepted']=all_referals['accepted'].fillna(0)
all_referals['total']=all_referals['rejected']+all_referals['accepted']
all_referals['Accepted%']=(all_referals['accepted']/all_referals['total'])*100
all_referals=all_referals[(all_referals['Accepted%']!=0) & (all_referals['total']>10)]
pp.savefig(all_referals['Accepted%'].plot(kind='bar', title='Accepted Referred Applicants Percentage').get_figure(),bbox_inches='tight')
all_dfs.append(all_referals)
referral=combined_df['Were you referred by anyone?'].value_counts()[0:10]
pp.savefig(referral.plot(kind='bar', title='Referred Applicants').get_figure(),bbox_inches='tight')
referral_accepted=df_accepted['Were you referred by anyone?'].value_counts()[0:10]
pp.savefig(referral_accepted.plot(kind='bar', title='Accepted Referred Applicants').get_figure(),bbox_inches='tight')
referral_rejected=df_rejected['Were you referred by anyone?'].value_counts()[0:10]
pp.savefig(referral_rejected.plot(kind='bar', title='Rejected Referred Applicants').get_figure(),bbox_inches='tight')
pp.close()
pd.concat(all_dfs).to_csv('data.csv')