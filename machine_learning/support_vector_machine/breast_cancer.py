import numpy as np
import pandas as pd
from sklearn import preprocessing, model_selection, svm

df = pd.read_csv('../data/breast_cancer_wisconsin.data')
# -99999 is recognized as an outlier (we don't wan't to drop it, but care of it)
df.replace('?', -99999, inplace=True)
df = df.drop('id', 1)

X = np.array(df.drop('class', 1))
y = np.array(df['class'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = svm.SVC()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print(accuracy)

# [4] expected
example_measures = np.array([[7, 8, 8, 2, 4, 8, 4, 8, 2]])
example_measures = example_measures.reshape(len(example_measures), -1)
prediction = clf.predict(example_measures)
print(prediction)