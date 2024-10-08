# -*- coding: utf-8 -*-
"""Capstone.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19MyGBJpql8FfCPF1PBW1H2pMFgnuBymi
"""

import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,mean_squared_error, mean_absolute_error, r2_score

from google.colab import files

Hospital =  pd.read_csv('https://raw.githubusercontent.com/RajuMopidevi/Machine-Learning-and-Artificial-Intelligence/main/01-01_EDA/Hospitalisation%20details.csv')
Medical = pd.read_csv('https://raw.githubusercontent.com/RajuMopidevi/Machine-Learning-and-Artificial-Intelligence/main/01-01_EDA/Medical%20Examinations.csv')
Names = pd.read_csv('https://raw.githubusercontent.com/RajuMopidevi/Machine-Learning-and-Artificial-Intelligence/main/01-01_EDA/Names.csv')

Hospital.head()

Medical.head()

Names.head()

#1. Merging all three files using inner merge
MP = pd.merge(Hospital, Medical, on='Customer ID', how ='inner')
HP = pd.merge(MP, Names, on='Customer ID', how ='inner')

HP.head()

HP.describe()

HP.info()

# 2. missing values
HP.isna().sum()

HP

# 3. find the rows that have question mark symbol and drop the rows
HPD = HP.drop(HP[HP.isin(['?']).any(axis=1)].index)

HPD

# 4. use necessary transformation methods to deal with nominal amd ordinal categorical data
HPD['year'] = HPD['year'].astype(int)
HPD['month'] = HPD['month'].astype(str)

# Slicing for state
HPD['State ID'] = HPD['State ID'].astype(str)
HPD['State ID'] = HPD['State ID'].str[1:5]

# Handle empty strings (replace with a placeholder or drop those rows)
HPD['State ID'] = HPD['State ID'].replace('', -1) # Replace empty strings with -1
HPD['State ID'] = HPD['State ID'].astype(int) # Now convert to int

# 5. replace no major surgery with 0
HPD['NumberOfMajorSurgeries'] = HPD['NumberOfMajorSurgeries'].replace('No major surgery', 0)
HPD['NumberOfMajorSurgeries'] = HPD['NumberOfMajorSurgeries'].astype(int)

# replace YES with 1 & NO with 0
HPD['Heart Issues'] = HPD['Heart Issues'].replace('No', 0)
HPD['Heart Issues'] = HPD['Heart Issues'].replace('yes', 1)
HPD['Any Transplants'] = HPD['Any Transplants'].replace('No', 0)
HPD['Any Transplants'] = HPD['Any Transplants'].replace('yes', 1)
HPD['Cancer history'] = HPD['Cancer history'].replace('No', 0)
HPD['Cancer history'] = HPD['Cancer history'].replace('Yes', 1)
HPD['smoker'] = HPD['smoker'].replace('No', 0)
HPD['smoker'] = HPD['smoker'].replace('yes', 1)

HPD['Heart Issues'] = HPD['Heart Issues'].astype(int)
HPD['Any Transplants'] = HPD['Any Transplants'].astype(int)
HPD['Cancer history'] = HPD['Cancer history'].astype(int)
HPD['NumberOfMajorSurgeries'] = HPD['NumberOfMajorSurgeries'].astype(int)
HPD['smoker'] = HPD['smoker'].astype(int)
HPD.info()

# remove 'tier - ' from Hospital tier column
HPD['Hospital tier'] = HPD['Hospital tier'].str.replace('tier - ', '')
HPD['Hospital tier'] = HPD['Hospital tier'].astype(int)

# remove 'tier - ' from Hospital tier column
HPD['City tier'] = HPD['City tier'].str.replace('tier - ', '')
HPD['City tier'] = HPD['City tier'].astype(int)

HPD.info()

# 7.Ageappears to be a significant factor in this analysis. Calculate the patients' ages based on their dates of birth.
# a. get date of birth from the year, date and month columns
HPD['Date of Birth'] = pd.to_datetime(HPD['date'].astype(str) + '-' + HPD['month'].astype(str) + '-' + HPD['year'].astype(str))
#b. arrive current age from the date of birth and todays date
HPD['Age'] = (pd.to_datetime('today').year - HPD['Date of Birth'].dt.year)

# 8. Gender of the pateient from the salutation of names like "exRiveros Gonzalez, Mr.  Juan D. Sr." and "Graves - Rostro, Ms.  Lindy" etc..
HPD['Gender'] = HPD['name'].str.contains('Mr.')
HPD['Gender'] = HPD['Gender'].replace(True, 'Male')
HPD['Gender'] = HPD['Gender'].replace(False, 'Female')
HPD['Gender'] = HPD['Gender'].replace('Male', 1)
HPD['Gender'] = HPD['Gender'].replace('Female',0)

# downloading dataset

#HPD.to_csv('merged_dataset.csv', index=False)
#  files.download('merged_dataset.csv')

# 9. Visualization of the distribution of costs using a histogram
plt.figure(figsize=(10, 6))
plt.hist(HPD['charges'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Charges')
plt.xlabel('Charges')
plt.ylabel('Frequency')

# 9b. Visualization of the distribution of costs using a Box plt
plt.figure(figsize=(10, 6))
sns.boxplot(x=HPD['charges'])
plt.title('Distribution of Charges')
plt.xlabel('Charges')

# 9c. Visualization of the distribution of costs using a whisker plt
plt.figure(figsize=(10, 6))
sns.violinplot(x=HPD['charges'])
plt.title('Distribution of Charges')
plt.xlabel('Charges')

# 9d. Visualization of the distribution of costs using a swarm plt
plt.figure(figsize=(10, 6))
sns.swarmplot(x=HPD['charges'])
plt.title('Distribution of Charges')
plt.xlabel('Charges')

# 10. State how the distribution is different across gender and tiers of hospitals.
plt.figure(figsize=(10, 6))
sns.boxplot(x='Gender', y='charges', hue='Hospital tier', data=HPD)
plt.title('Distribution of Charges by Gender and Hospital Tier')

# 11. Radar chart to showcase the median hospitalization cost for each tier of hospitals using
Median_Charges = HPD.groupby('Hospital tier')['charges'].median()
categories = list(Median_Charges.index)
values = list(Median_Charges.values)
fig, ax = plt.subplots(figsize=(8,8),subplot_kw=dict(polar=True))
num_vars = len(categories)
angles = np.linspace(0, 2 * np.pi,num_vars, endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

ax.fill(angles, values, color='b',alpha=0.25)
ax.plot(angles, values, color='b',linewidth=2)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

plt.title('Median Hospitalization Cost by Hospital Tier')
plt.show()

#12. A frequency table and a stacked bar chart to visualize the count of people in the different tiers of cities and hospitals
# 12a. get the count of people (customer ID) in the different tiers of cities and hospitals using groupby function
HPD_count = HPD.groupby(['City tier','Hospital tier']).count()['Customer ID']
HPD_count

# 12b. stacked bar chart using HPD_Count
HPD_count.plot(kind='bar', stacked=True)
plt.title('Count of People in Different Tiers of Cities and Hospitals')
plt.xlabel('City Tier')
plt.ylabel('Count')

# 13a null Hypothesis: The average hospitalization costs for the three types of hospitals are not significantly different
n_hospital_1 = HPD[HPD['Hospital tier'] == 1]['charges']
n_hospital_2 = HPD[HPD['Hospital tier'] == 2]['charges']
n_hospital_3 = HPD[HPD['Hospital tier'] == 3]['charges']

anova_result = stats.f_oneway(n_hospital_1, n_hospital_2, n_hospital_3)
print(anova_result)
if anova_result.pvalue < 0.05:
  print('The average hospitalization costs for the three types of hospitals are significantly different')
else:
  print('The average hospitalization costs for the three types of hospitals are not significantly different')

# 13b null Hypothesis: The average hospitalization costs for the three types of cities are not significantly different
n_city_1 = HPD[HPD['City tier'] == 1]['charges']
n_city_2 = HPD[HPD['City tier'] == 2]['charges']
n_city_3 = HPD[HPD['City tier'] == 3]['charges']

anova_result = stats.f_oneway(n_city_1, n_city_2, n_city_3)
print(anova_result)
if anova_result.pvalue < 0.05:
  print('The average hospitalization costs for the three types of cities are significantly different')
else:
  print('The average hospitalization costs for the three types of cities are not significantly different')

# 13c null Hypothesis: The average hospitalization cost for smokers is not significantly different from the average cost for nonsmokers.
n_smoker = HPD[HPD['smoker'] == 1]['charges']
n_nonsmoker = HPD[HPD['smoker'] == 0]['charges']

#t-test
t_result = stats.ttest_ind(n_smoker, n_nonsmoker)
print(t_result)
if t_result.pvalue < 0.05:
  print('The average hospitalization cost for smokers is significantly different from the average cost for nonsmokers')
else:
  print('The average hospitalization cost for smokers is not significantly different from the average cost for nonsmokers')

#13d. Smoking and heart issues are independent
n_smoker = HPD[HPD['smoker'] == 1]['Heart Issues']
n_nonsmoker = HPD[HPD['smoker'] == 0]['Heart Issues']

#chi-square test
chi_result = stats.chi2_contingency(pd.crosstab(HPD['smoker'], HPD['Heart Issues']))
print(chi_result)
if chi_result[1] < 0.05:
  print('Smoking and heart issues are not independent')
else:
  print('Smoking and heart issues are independent')

"""## 2. MACHINE LEARNING"""

#1. correlation between predictors to identify highly correlated predictors using heatmap
plt.figure(figsize=(20, 10))
HPD_num = HPD.select_dtypes(include=['int64', 'int32','float64'])
sns.heatmap(HPD_num.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation between Predictors')
plt.show()

HPD_num.info()

#2 Linear regression model
# splitting data
X = HPD_num.drop(['charges'], axis=1)
y = HPD_num['charges']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Data Standardization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr_scores = cross_val_score(lr, X_train_scaled,y_train,cv=5,scoring='neg_mean_squared_error')
lr_rmse_scores = (-lr_scores)** 0.5


print("Linear Regression RMSE scores : ", lr_rmse_scores)
print("Linear Regression Mean RMSE: ", lr_rmse_scores.mean())

# 2.3. Incorporate sklearn-pipelines to streamline the workflow
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

pipeline = Pipeline([('scaler', StandardScaler()), ('lr', LinearRegression())])

# Use cross_val_score directly on the pipeline
# no need to access best_estimator_
pileline_scores = cross_val_score(pipeline, X_train_scaled,y_train,cv=5, scoring='neg_mean_squared_error')
pipeline_rmse_scores = (-pileline_scores)** 0.5

print("Pipeline RMSE scores :", pipeline_rmse_scores)
print("Pipeline Mean RMSE :", pipeline_rmse_scores.mean()) # calculate the mean of the scores

# 2.4. Ridge Regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

ridge = Ridge()
# define the parameter grid for the search
param_grid = {'alpha': [0.1, 1.0, 10.0]}
ridge_search = GridSearchCV(ridge, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error') # add param_grid to the function call
ridge_search.fit(X_train_scaled,y_train)
ridge_best = ridge_search.best_estimator_
ridge_scores = cross_val_score(ridge_best, X_train_scaled,y_train,cv=5, scoring='neg_mean_squared_error')
ridge_rmse_scores = (-ridge_scores)** 0.5


print("Ridge Regression RMSE scores :", ridge_rmse_scores)
print("Ridge Regression Mean RMSE :", ridge_rmse_scores.mean())

#2.6. # Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor

gb = GradientBoostingRegressor()
gb_scores = cross_val_score(gb, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
gb_rmse_scores = (-gb_scores) ** 0.5

# Fitting the model to get feature importance
gb.fit(X_train_scaled, y_train)
feature_importances = gb.feature_importances_

print("Gradient Boosting RMSE Scores :", gb_rmse_scores)
print("Gradient Boosting Mean RMSE :", gb_rmse_scores.mean())

# Displaying Feature Importances
FI_df = pd.DataFrame({
    'Feature' : X.columns,
    'Importance' : feature_importances
}).sort_values(by='Importance',ascending=False)

print("Feature Importances:")
print(FI_df)

# 3.Estimate the cost of hospitalization of Jaya

# 4. Find the predicted hospitalization cost using the best models
# Ensure jayna_df has the same columns and is in the same order as the data used to fit the scaler
jayna_df = pd.DataFrame({
    'year':[1988],
    'date':[28],
    'children': [2],
    'Hospital tier': [1],
    'City tier': [1],
    'State ID': [1011],
    'BMI': [29.5],
    'HBA1C': [5.8],
    'Heart Issues': [0],
    'Any Transplants': [0],
    'Cancer history': [0],
    'NumberOfMajorSurgeries': [0],
    'smoker': [1],
    'Age': [36],
    'Gender': [0],
})

jayna_df

# Standardize the features
jayna_scaled = scaler.transform(jayna_df)

#4a. predict the cost for Ms. Jayna with linear regression model
# Fit the linear regression model to your training data
lr.fit(X_train_scaled, y_train)

#4a. predict the cost for Ms. Jayna with linear regression model
jayna_pred = lr.predict(jayna_scaled)
print('Linear Regression predicted cost for Ms. Jayna: {}'.format(jayna_pred))

# Fit the Pipeline model to your training data
pipeline.fit(X_train_scaled, y_train)

#4a. predict the cost for Ms. Jayna with linear regression model
jayna_pred = pipeline.predict(jayna_scaled)
print('Pipeline predicted cost for Ms. Jayna: {}'.format(jayna_pred))

# Fit the ridge model to your training data
ridge_best.fit(X_train_scaled, y_train)

#4a. predict the cost for Ms. Jayna with linear regression model
jayna_pred = ridge_best.predict(jayna_scaled)
print('Ridge predicted cost for Ms. Jayna: {}'.format(jayna_pred))

# Fit the gradient boosting model to your training data
gb.fit(X_train_scaled, y_train)

#4a. predict the cost for Ms. Jayna with linear regression model
jayna_pred = gb.predict(jayna_scaled)
print('Gradient Boosting predicted cost for Ms. Jayna: {}'.format(jayna_pred))

# Model evaluation using the Models _ mean_squared, mean_absolute error & r2 score
## a. Linear regression
lr_y_pred = lr.predict(X_test_scaled)
lr_mse = mean_squared_error(y_test, lr_y_pred)
Ir_mae = mean_absolute_error(y_test, lr_y_pred)
lr_r2 = r2_score(y_test, lr_y_pred)

print('Linear Regression MSE: {}'.format(lr_mse))
print('Linear Regression MAE: {}'.format(Ir_mae))
print('Linear Regression R2: {}'.format(lr_r2))

## b. Pipeline
pipeline_y_pred = pipeline.predict(X_test_scaled)
pipeline_mse = mean_squared_error(y_test, pipeline_y_pred)
pipeline_mae = mean_absolute_error(y_test, pipeline_y_pred)
pipeline_r2 = r2_score(y_test, pipeline_y_pred)

print('Pipeline MSE: {}'.format(pipeline_mse))
print('Pipeline MAE: {}'.format(pipeline_mae))
print('Pipeline R2: {}'.format(pipeline_r2))

## c. Ridge
ridge_y_pred = ridge_best.predict(X_test_scaled)
ridge_mse = mean_squared_error(y_test, ridge_y_pred)
ridge_mae = mean_absolute_error(y_test, ridge_y_pred)
ridge_r2 = r2_score(y_test, ridge_y_pred)

print('Ridge MSE: {}'.format(ridge_mse))
print('Ridge MAE: {}'.format(ridge_mae))
print('Ridge R2: {}'.format(ridge_r2))

## d. Gradient Boosting
gb_y_pred = gb.predict(X_test_scaled)
gb_mse = mean_squared_error(y_test, gb_y_pred)
gb_mae = mean_absolute_error(y_test, gb_y_pred)
gb_r2 = r2_score(y_test, gb_y_pred)

print('Gradient Boosting MSE: {}'.format(gb_mse))
print('Gradient Boosting MAE: {}'.format(gb_mae))
print('Gradient Boosting R2: {}'.format(gb_r2))

"""Gradient Boosting has low MSE & high R2.

completed

Conclusion : Gradient boosing is efficient
"""

# Completed

"""completed"""



"""Completed

"""