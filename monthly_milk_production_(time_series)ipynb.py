# -*- coding: utf-8 -*-
"""monthly milk production (Time Series)ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1noF8-UkYeoS7gQnNRvKq3LcsXnBKYFfw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/content/monthly_milk_production.csv',index_col='Date',parse_dates=True)
df.index.freq='MS'

df.head()

df.plot(figsize=(12,6))

from statsmodels.tsa.seasonal import seasonal_decompose

results = seasonal_decompose(df['Production'])
results.plot();

len(df)

train = df.iloc[:156]
test = df.iloc[156:]

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

df.head(),df.tail()

scaler.fit(train)
scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)

scaled_train[:10]

#define generator
from keras.preprocessing.sequence import TimeseriesGenerator
n_input = 3
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)

X,y = generator[0]
print(f'Given the Array: \n{X.flatten()}')
print(f'Predict this y: \n {y}')

X.shape

#we do the same thing ,but here we are using 12 months
n_input=12
generator=TimeseriesGenerator(scaled_train,scaled_train,length=n_input,batch_size=1)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

#define model
model=Sequential()
model.add(LSTM(100,activation='relu',input_shape=(n_input,n_features)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')

model.summary()

#fit model
model.fit(generator,epochs=50)

loss_per_epoch = model.history.history['loss']
plt.plot(range(len(loss_per_epoch)),loss_per_epoch)

last_train_batch=scaled_train[-12:]

last_train_batch=last_train_batch.reshape((1,n_input,n_features))

model.predict(last_train_batch)

scaled_test[0]

test_predictions = []

first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))

for i in range(len(test)):

    # get the prediction value for the first batch
    current_pred = model.predict(current_batch)[0]

    # append the prediction into the array
    test_predictions.append(current_pred)

    # use the prediction to update the batch and remove the first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

test_predictions

test.head()

true_predictions = scaler.inverse_transform(test_predictions)

test['Prediction']=true_predictions

test.plot(figsize=(14,5))

from sklearn.metrics import mean_squared_error
from math import sqrt
rmse=sqrt(mean_squared_error(test['Production'],test['Prediction']))
print(rmse)

