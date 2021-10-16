
import pandas as pd

df = pd.read_csv ('dummy_df.csv')
df.columns
df = df.drop('Unnamed: 0', 1)
df.dtypes

X = df.drop('price',axis=1)
y = df['price']

#training model
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 42)
regressor.fit(X, y)

#predicting
X.columns

#getting first row
X_test=X.iloc[[12]]

X_test.iloc[0, 5:] = 0

X_copy=X_test

for i in range(12):
    X_test=X_test.append(X_copy)
    X_test=X_test.reset_index(drop=True)
    X_test.iloc[[i],[i+5]] = 1

X_test.drop(X_test.tail(1).index,inplace=True) # drop last n rows



y_pred = regressor.predict(X_test)
X_test['prediction prices'] = y_pred.tolist()

###################### adding another feature (ausstattung)


import pandas as pd

df=pd.read_csv ('ausstattung_data.csv')

df.columns
df = df.drop('Unnamed: 0', 1)
df.dtypes

X = df.drop('price',axis=1)
y = df['price']

#training model
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 42)
regressor.fit(X, y)

#predicting
X.columns

#getting first row
X_test=X.iloc[[11]]

X_test.iloc[0, 5:] = 0

X_copy=X_test

for i in range(4):
    X_test=X_test.append(X_copy)
    X_test=X_test.reset_index(drop=True)
    X_test.iloc[[i],[i+5]] = 1

X_test.drop(X_test.tail(1).index,inplace=True) # drop last n rows



y_pred = regressor.predict(X_test)
X_test['prediction prices'] = y_pred.tolist()








