import pandas as pd
import quandl
import math
import datetime
import numpy as np
import pickle
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

## df = DataFrame (pandas)
df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

## just get the column that we care about
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
## replace NA/NaN with a value (cause we can't work with NA/Nan in machine learning)
df.fillna(-99999, inplace=True)

## try to predict 10% of the dataframe
forecast_out = int(math.ceil(0.01*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)

## features : everything except label column
X = np.array(df.drop(['label'], 1))

## normalization
X = preprocessing.scale(X)

X_lately = X[-forecast_out:]
X = X[:-forecast_out]

## drop rows where there is no labels
df.dropna(inplace=True)

## labels : the label column of course
y = np.array(df['label'])

## fit classifier with 20% of our data
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

## save the classifier (we don't want to train it each time)
#clf = LinearRegression()
#clf.fit(X_train, y_train)
#with open('linear_regression.pickle', 'wb') as f:
    #pickle.dump(clf, f)

## open the saved classifier
pickle_in = open('linear_regression.pickle', 'rb')
clf = pickle.load(pickle_in)

## test classifier (accuracy)
accuracy = clf.score(X_test, y_test)

print('accuracy : ' + str(accuracy))

## predict
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.savefig('file.svg') ## or plt.show()