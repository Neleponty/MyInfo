from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
MB = MultinomialNB(alpha=0.01)

X = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[1,1,1,1]])
print(X.ndim)
Y = np.array([1,2,3,4,5])
MB.fit(X,Y)
print(MB.predict([0,0,1,0]))

# ТФИДФ РАБОТАЕТ
tf = TfidfVectorizer()
A = tf.fit_transform(['a','b'])
def group(A_m,tf):

    print(sorted([max([(item,tf.get_feature_names()[i]) for item in A_m[:,i].toarray()], key=lambda a: a[0]) for i in range(A_m.shape[1])]))
group(A,tf)
print(tf.get_feature_names())