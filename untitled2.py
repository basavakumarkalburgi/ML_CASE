# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jZv3CUeiDwqfDV48_q523p8Otp4Sg4YR
"""

from google.colab import drive
drive.mount('/content/drive')

!ls /content/drive/MyDrive/MLDataSets/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

!pip install xgboost

from xgboost import XGBRegressor #ML Model
from sklearn.model_selection import train_test_split # Split data into Training and Testing 
from sklearn.model_selection import GridSearchCV # For Hyper Parameter Tuning
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

diamond_df = pd.read_csv('/content/drive/MyDrive/MLDataSets/diamonds.csv')
diamond_df.head(20)

diamond_df.drop(['Unnamed: 0'],axis =1,  inplace=True)
diamond_df.head()

diamond_df.info()

diamond_df.shape

diamond_df.dtypes

diamond_df.isna().sum()

diamond_df.describe()

!pip install ydata-profiling

from ydata_profiling import ProfileReport
profile = ProfileReport(diamond_df,title="profiling Report")

profile.to_notebook_iframe()

sns.countplot(data=diamond_df, x='color')
plt.show()

sns.countplot(data=diamond_df, x='clarity')
plt.show()

ab=list(diamond_df['cut'].unique())
ab

from scipy.sparse import dia
cut_mapping = {'Fair':0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
diamond_df.cut = diamond_df.cut.map(cut_mapping)
diamond_df.head()

color_mapping = {'J':0,'I': 1,'H':2,'G':3,'F':4,'E':5,'D':6}
diamond_df.color = diamond_df.color.map(color_mapping)

clarity_mapping = {'I1':0,'SI2': 1,'SI1':2,'vs2':3,'vs1':4,'ws2':5,'ws1':6}
diamond_df.clarity = diamond_df.clarity.map(clarity_mapping)

diamond_df.head()

diamond_df[diamond_df["x"]==0].index

diamond_df = diamond_df.drop(diamond_df[diamond_df["x"]==0].index)
diamond_df = diamond_df.drop(diamond_df[diamond_df["y"]==0].index)
diamond_df = diamond_df.drop(diamond_df[diamond_df["z"]==0].index)

diamond_df = diamond_df[diamond_df['depth'] < diamond_df['depth'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['table'] < diamond_df['table'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['x'] < diamond_df['x'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['y'] < diamond_df['y'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['z'] < diamond_df['z'].quantile(0.99)]

diamond_df.info()

model_df = diamond_df.copy()

x = model_df.drop(['price'], axis=1)
y= model_df['price']

x.columns

y.head()

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)

x_train.shape,x_test.shape,y_train.shape,y_test

'''
xgb1 = XGBRegressor()
parameters = {
              'objective':['reg:squarederror'],
              'learning_rate': [.0001, 0.001, .01],
              'max_depth': [3, 5, 7],
              'min_child_weight': [3,5,7],
              'subsample': [0.1,0.5,1.0],
              'colsample_bytree': [0.1, 0.5, 1.0],
              'n_estimators': [500]}

xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        cv = 3,
                        n_jobs = -1,
                        verbose=0)
                        '''

# xgb_grid.fit(x_train, y_train)

#print("MAE:", mean_absolute_error(y_test, xgb_grid.predict(X_test)))
#print("MSE:", mean_squared_error(y_test, xgb_grid.predict(X_test)))
#print("R2:", r2_score(y_test, xgb_grid.predict(X_test)))

xgb1 = XGBRegressor()

history = xgb1.fit(x_train,y_train,verbose=True)

print("MAE:", mean_absolute_error(y_test, xgb1.predict(x_test)))
print("MSE:", mean_squared_error(y_test, xgb1.predict(x_test)))

xgb1.save_model('xgb_model.json')

!pip install joblib

import joblib
# save the model to a file
joblib.dump(xgb1, 'xgb_grid.joblib')

from google.colab import files
files.download('xgb_grid.joblib') 
files.download('xgb_model.json')

'''xgb_cv = (xgb_grid.best_estimator_)

eval_set = [(X_train, y_train),
            (X_test, y_test)]

fit_model = xgb_cv.fit(
    X_train,
    y_train,
    eval_set=eval_set,
    eval_metric='mae',
    early_stopping_rounds=50,
    verbose=True)'''

xgb_grid.save_model('xgb_model.json')

!pip install joblib
import joblib
# save the model to a file
joblib.dump(xgb1, 'xgb_grid.joblib')
from google.colab import files
files.download('xgb_grid.joblib') 
files.download('xgb_model.json')