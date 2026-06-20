from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()

x=iris.data
y=iris.target

model = DecisionTreeClassifier()
model.fit(x,y)
prediction = model.predict([[5.1,3.5,1.4,0.2]])
print('prediction:',iris.target_names[prediction[0]])
