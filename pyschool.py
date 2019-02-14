
# coding: utf-8

# In[3]:


from IPython.display import display
from IPython.display import HTML
import IPython.core.display as di # Example: di.display_html('<h3>%s:</h3>' % str, raw=True)

# This line will hide code by default when the notebook is exported as HTML
di.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)

# This line will add a button to toggle visibility of code blocks, for use with the HTML export version
di.display_html('''<button onclick="jQuery('.input_area').toggle(); jQuery('.prompt').toggle();">Toggle code</button>''', raw=True)


# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# Block Warnings from printing
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"


# Read School and Student Data File and store into Pandas Data Frames
school_df = pd.read_csv(school_data_to_load)
student_df = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
complete = pd.merge(student_df, school_df, how="left", on=["school_name", "school_name"])
# complete.columns

school_df.columns = ['School ID', 'School Name', 'School Type', 'Total Students', 'Total Budget']
complete.columns = ['Student ID', 'Student Name', 'Gender', 'Grade', 'School Name',       'Reading Score', 'Math Score', 'School ID', 'School Type', 'Total Students', 'Total Budget']
student_df.columns = ['Student ID', 'Student Name', 'Gender', 'Grade', 'School Name', 'Reading Score',                 'Math Score']
# algorithm already set using orignal column names


# ## District Summary

# In[4]:


total_schools = school_df['School Name'].count()
total_students = school_df['Total Students'].sum()
total_budget = school_df['Total Budget'].sum()
avg_math = student_df['Math Score'].mean()
avg_read = student_df['Reading Score'].mean()
passing_r8 = (avg_math + avg_read)/2

foo = student_df[student_df['Reading Score'] >= 70].count()/student_df['Student Name'].count()
reading_pass = foo.get('Grade')*100

bar = student_df[student_df['Math Score'] >= 70].count()/student_df['Student Name'].count()
math_pass = bar.get('Grade')*100

district_summary = pd.DataFrame({'Total Schools': [total_schools],
                                'Total Students': [total_students],
                                'Total Budget': [f'${total_budget:,.2f}'],
                                 'Average Math':[str(round(avg_math,4)) + '%'],
                                 'Average Reading':[str(round(avg_read,4)) + '%'],
                                 '% Passing Math': [str(round(math_pass,4)) + '%'],
                                 '% Passing Reading': [str(round(reading_pass,4)) + '%'],
                                 '% Overall Passing Rate': [str(round(passing_r8, 4)) + '%']
                                })
district_summary


# Interesting to see that students on <u>average score a 79% on math</u> , but only <u>75% of the student population passes math</u>.  Looking at <u>average reading scores of 82%</u>, it is nice to see that <u>86% of the student poppulation are passing reading</u>.

# ## School Summary

# In[6]:


# Grab nececessary columns
school_data = complete[['School Name', 'Total Students', 'Total Budget',                       'Math Score', 'Reading Score']]

# counting those who have pass reading/math and not counting those who have failed
# then calculating % passing the perspective field
passing_percentages = school_data[['School Name', 'Math Score', 'Reading Score']]
passing_percentages['% Passing Math'] = np.where(passing_percentages['Math Score'] >= 70, 1,0)
passing_percentages['% Passing Reading'] = np.where(passing_percentages['Reading Score'] >= 70, 1,0)

group = passing_percentages.groupby('School Name')
# calculating averages for each school
school_performance = pd.DataFrame(group.mean())
school_performance['% Overall Passing Rate'] = 100*(school_performance['% Passing Math']+school_performance['% Passing Reading'])/2

# remove SCHOOL ID from df
school = school_df[['School Name', 'School Type', 'Total Students',
       'Total Budget']]

school['Per Student Budget'] = school['Total Budget']/school['Total Students']

school = school.set_index('School Name')

school_stats = pd.merge(school, school_performance,  how = 'outer', left_index = True, right_index = True)
school_stats.columns = ['School Type', 'Total Students', 'Total Budget', 'Per Student Budget',
       'Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading',
       '% Overall Passing Rate']

# make a copy for readibility purposes then edit
school_stats_string = school_stats.copy()
school_stats_string['Average Math Score'] = round(school_stats_string['Average Math Score'], 4)
school_stats_string['Average Reading Score'] = round(school_stats_string['Average Reading Score'], 4)
school_stats_string['% Overall Passing Rate'] = round(school_stats_string['% Overall Passing Rate'], 4)
school_stats_string['% Passing Math'] = round(school_stats_string['% Passing Math'], 6)*100
school_stats_string['% Passing Reading'] = round(school_stats_string['% Passing Reading'], 6)*100
school_stats_string['Total Budget'] = school_stats_string['Total Budget'].astype(float).map('${:,.2f}'.format) 
school_stats_string['Per Student Budget'] = school_stats_string['Per Student Budget'].astype(float).map('${:,.2f}'.format) 
# school_stats_string.head()


# ## Top Performing Schools (By Passing Rate)

# In[41]:


top5 = school_stats_string.sort_values(by = '% Overall Passing Rate', ascending=False).head(5)
top5


# Pena High School has the most interesting stats out of the group.
# 
# has the highest math passing rate and average math score out of the group, but though theirsurprisingly has only a 1% difference when comparing students passing math to those passing reading.  This is something to further investagate through qualitative research.

# ## Bottom Performing Schools (By Passing Rate)

# In[42]:


bottom5 = school_stats_string.sort_values(by = '% Overall Passing Rate', ascending = False).tail(5)
bottom5


# In[43]:


budget = [x.strip('$')[0:3] for x in top5['Per Student Budget']]
top5_avg_budget = np.array(budget).astype(int).mean()

budget = [x.strip('$')[0:3] for x in bottom5['Per Student Budget']]
bottom5_avg_budget =np.array(budget).astype(int).mean()


# In[ ]:


average_comparison = pd.DataFrame(columns = 'Avg Cost Per Student': [top5_avg_budget, bottom5_avg_budget])


# ## Math Scores by Grade

# In[7]:


math_scores = student_df[['Grade', 'School Name', 'Math Score']]

ninth_grade = math_scores.loc[math_scores['Grade'] == '9th']
ninth_grade = ninth_grade.groupby('School Name')
ninth_grade = pd.DataFrame(ninth_grade.mean())
ninth_grade.columns = ['9th']

tenth_grade = math_scores.loc[math_scores['Grade'] == '10th']
tenth_grade = tenth_grade.groupby('School Name')
tenth_grade = pd.DataFrame(tenth_grade.mean())
tenth_grade.columns = ['10th']

eleventh_grade = math_scores.loc[math_scores['Grade'] == '11th']
eleventh_grade = eleventh_grade.groupby('School Name')
eleventh_grade = pd.DataFrame(eleventh_grade.mean())
eleventh_grade.columns = ['11th']

twelve_grade = math_scores.loc[math_scores['Grade'] == '12th']
twelve_grade = twelve_grade.groupby('School Name')
twelve_grade = pd.DataFrame(twelve_grade.mean())
twelve_grade.columns = ['12th']

# combine dataframes based on grade Series
math_grades = pd.concat([ninth_grade, tenth_grade, eleventh_grade, twelve_grade], axis = 1)
math_grades


# ## Reading Score by Grade 

# In[8]:


reading_scores = student_df[['Grade', 'School Name', 'Reading Score']]

ninth_grade = reading_scores.loc[math_scores['Grade'] == '9th']
ninth_grade = ninth_grade.groupby('School Name')
ninth_grade = pd.DataFrame(ninth_grade.mean())
ninth_grade.columns = ['9th']

tenth_grade = reading_scores.loc[math_scores['Grade'] == '10th']
tenth_grade = tenth_grade.groupby('School Name')
tenth_grade = pd.DataFrame(tenth_grade.mean())
tenth_grade.columns = ['10th']

eleventh_grade = reading_scores.loc[math_scores['Grade'] == '11th']
eleventh_grade = eleventh_grade.groupby('School Name')
eleventh_grade = pd.DataFrame(eleventh_grade.mean())
eleventh_grade.columns = ['11th']

twelve_grade = reading_scores.loc[math_scores['Grade'] == '12th']
twelve_grade = twelve_grade.groupby('School Name')
twelve_grade = pd.DataFrame(twelve_grade.mean())
twelve_grade.columns = ['12th']

# combine dataframes based on grade Series
reading_grades = pd.concat([ninth_grade, tenth_grade, eleventh_grade, twelve_grade], axis = 1)
reading_grades


# ## Scores by School Spending

# In[9]:


spending_performance = school_stats[['Per Student Budget',
       'Average Math Score', 'Average Reading Score', '% Passing Math',
       '% Passing Reading', '% Overall Passing Rate']]

money_bins = list(range(575,700, 25))
group_names = ["$578 - 600", "$601 - 625", "$626 - 650", "$651-655"]

spending_performance['Spending Ranges (Per Student)'] = pd.cut(spending_performance['Per Student Budget'],                                                               bins = money_bins, labels = group_names)
spending_performance = spending_performance.drop('Per Student Budget', axis = 1)

spending_performance_stats = spending_performance.groupby('Spending Ranges (Per Student)')
spending_performance_stats = pd.DataFrame(spending_performance_stats.mean())
spending_performance_stats.iloc[:,2] = spending_performance_stats.iloc[:,2]*100
spending_performance_stats.iloc[:,3] = spending_performance_stats.iloc[:,3]*100
spending_performance_stats.round(4)


# ## Scores by School Size

# In[10]:


performance_x_size = school_stats[['Total Students',       'Average Math Score', 'Average Reading Score', '% Passing Math',
       '% Passing Reading', '% Overall Passing Rate']]

# based on performance_x_size['Total Students'].describe()
size_bins = [400, 1600, 3200, 5000]
group_names = ["Small (<1600)", "Medium (1600-3200)", "Large (3200-5000)"]

performance_x_size['School Size'] = pd.cut(performance_x_size['Total Students'], bins = size_bins, labels = group_names)
performance_x_size = performance_x_size.drop('Total Students', axis = 1)
performance_size_stats = performance_x_size.groupby('School Size')
performance_size_stats = pd.DataFrame(performance_size_stats.mean())
performance_size_stats.iloc[:,2] = performance_size_stats.iloc[:,2]*100
performance_size_stats.iloc[:,3] = performance_size_stats.iloc[:,3]*100
performance_size_stats.round(4)


# ## Scores by School Type

# In[11]:


performance_x_type = school_stats[['School Type','Average Math Score', 'Average Reading Score',                                   '% Passing Math','% Passing Reading', '% Overall Passing Rate']]
performance_type_stats = performance_x_type.groupby('School Type')
performance_type_stats = pd.DataFrame(performance_type_stats.mean())
performance_type_stats.iloc[:,2] = performance_type_stats.iloc[:,2]*100
performance_type_stats.iloc[:,3] = performance_type_stats.iloc[:,3]*100
performance_type_stats.round(4)


# <font size="12"><head><center><b> Conclusion </b></center></head></font>
# _____
# <body>
# Before discussing the findings, let's get a bit more granular withschool size and type to get a better understanding of what is happening with the world's future.
# </body>

# In[12]:


performance = school_stats[['School Type', 'Total Students', 'Per Student Budget', 'Average Math Score', 'Average Reading Score',                                   '% Passing Math','% Passing Reading', '% Overall Passing Rate']]

size_bins = [400, 1000, 2000, 3000, 4000, 5000]
group_names = ['X-Small (<1000)', 'Small (1001-2000)', 'Medium (2001-3000)', 'Large (3001-4000)', 'X-Large (4001-5000)']
performance['School Size'] = pd.cut(performance['Total Students'], bins = size_bins, labels = group_names)
performance = performance.drop('Total Students', axis = 1)

money_bins = list(range(575,700, 25))
group_names = ["$578 - 600", "$601 - 625", "$626 - 650", "$651-655"]
performance['Cost Per Student'] = pd.cut(performance['Per Student Budget'],                                                               bins = money_bins, labels = group_names)
performance = performance.drop('Per Student Budget', axis = 1)


performance = performance.groupby(['School Type', 'School Size', 'Cost Per Student'])

performance_stats = pd.DataFrame(performance.mean())

# Way too many NAs, but that chart is hard to compare values when NA values are dropped.
performance_stats.dropna(axis = 0)


# Ok, as we see size doesn't really effect performance. It is clearly the type of education structure a student has.  The can only compare the school types at the medium size level, so let's look.

# In[13]:


performance_stats.loc[performance_stats.index.get_level_values(1).values == 'Medium (2001-3000)']


# As we see, not only do charter schools provide a better value for our country's children but cost at least $25 dollars cheaper allowing that extra money to go else where to further improve the education system.  With students at the charter school level performing a whole letter grade above their district counter parts, with further investegation, it might be that the Charter system is a better system.
