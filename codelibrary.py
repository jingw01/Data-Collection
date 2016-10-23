#python collection


#library 
%matplotlib inline
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.plot as plt
import pandas as pd
import seaborn as sns


###############################Pandas#############################
#read file
df_raw = pd.read_csv(filename)

# quick exploratory 
df_raw.head()
df_raw.describe()
df_raw.notnull().summary
#pivot table
data.pivot_table(values=['x'],index=['a','b','c'],aggfunc=np.mean)

#cross summary for categorical data
def percConvert(ser):
  return ser/float(ser[-1])
pd.crosstab(data[Y],data[X],margins=True).apply(percConvert, axis=1)


#change data type
colType = pd.DataFrame({'type':{'a':'continuous','b':'categorical'}}).
reset_index().rename(columns={'index':'features'})
for i, row in colTypes.iterrows():  #i: dataframe index; row: each row in series format
    if row['type']=="categorical":
        data[row['feature']]=data[row['feature']].astype(np.object)
    elif row['type']=="continuous":
        data[row['feature']]=data[row['feature']].astype(np.float)
print data.dtypes

#filter
data.loc[(data[a]=='a' &data[b]=='b'),[c,d]]

#add new variables, e.g. mode

df['new varibale'] = data[d],fillna(sp.stats.mode(data[d]).mode[0],inplace=False)

#rename column
flatframe = flatframe.rename(columns={'minor':'year'})

#convert string to datatime

df['date'] = pd.to_datetime(df['date'])
df['day'] = (df['date'] - df['pre_date']).dt.days

# create dataframe
yeardict[y]=pd.DataFrame(yearlist2)#one for each year
yearspanel=pd.Panel.from_dict(yeardict, orient="minor")#stack dataframes into a panel
hierframe=yearspanel.to_frame() #flattening leads to a hierarchical index

#nested dict
pd.DataFrame(nestdict).T

#change data type
flatframe.year = flatframe.year.astype(int)

#count unique value of a series
prolific=flatframe.url.value_counts()

#group by 
dfgrp = df.groupby([grp1]).sum()
dfgrp.div(dfgrp[colsum],0)

#merge
largedf=flatframe.merge(tempdf, on="url")
left.join(right, on=key_or_keys)
pd.merge(left, right, left_on=key_or_keys, right_index=True, how='left', sort=False)


##sorting 
df.sort(['A', 'B'], ascending=[1, 0])

#reshape

pd.melt(df, id_vars=['A'], value_vars=['B', 'C'],var_name='',value_name='')


#dummy 
df_dummy = pd.get_dummies(df['factor'])

#binning
bins = df['binvar'].quantile([.25, .50, .75, 1]).values
group_names =['a','b','c','d']
df['categories'] = pd.cut(df['binvar'],bins,labels=group_names)
pd.value_counts(df['categories'])


###############################Plots#############################

#distributution by factors 
g = sns.FacetGrid(df, row= "factor1",col="factor2", margin_titles=True,size=5)
bins = np.linspace(0, 60, 13)
g.map(sns.distplot, "x", color="steelblue", bins=bins)

#group b plots

def fraction_plot(grpvar,ax):
    grp=df[[grpvar,'colsum','x']].groupby(grpvar).sum()
    return grp.div(grp['colsum'],0)['x'].plot(kind='bar',ax=ax)
fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(30, 15))

#plot iwth confidence interval 
plt.gca().invert_xaxis()
plt.plot(nbrs, fmeanstr, color=c0, label="training");
plt.fill_between(nbrs, fmeanstr - fstdsstr, fmeanstr+fstdsstr, color=c0, alpha=0.3)
plt.plot(nbrs, fmeanste, color=c1, label="testing");
plt.fill_between(nbrs, fmeanste - fstdsste, fmeanste+fstdsste, color=c1, alpha=0.5)

plt.legend();


############################### Numpy/Sparse #############################


#add indicator variables based on a categorical column
#determine the unique genres
genres = set()
for genre in largedf.genres:
    genres.update(genre)
genres = sorted(genres)

#make a column for each genre
for genre in genres:
    largedf[genre] = [genre in g for g in largedf.genres] #############################?
     
largedf.head()

# read txt file 
with open(filename) as f:
    content = f.readlines()
    data=[]
    for l in content:
        data.append(l)

from scipy.sparse import csr_matrix
array = np.hstack((a,b,c))
csr_array = csr_matrix(array)

#binning

import numpy
data = numpy.random.random(100)
bins = numpy.linspace(0, 1, 10)
digitized = numpy.digitize(data, bins)
bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]


#statistics model

import statsmodels.api as sm

# add constant for the intercept to work 

Xt = np.vstack([age, weight, height]).T
X = sm.add_constant(Xt)
ols = sm.OLS(  blood, X)
# fit three models
ols_result = ols.fit()
print(olsh_result.summary())
print(ols_result.rsquared)

#prediction
from statsmodels.sandbox.regression.predstd import wls_prediction_std

Xs = np.array( [1, 45, 180, 70])
Q=ols_result.predict(Xs)

sdev, lower, upper = wls_prediction_std(ols_result, exog=Xs, alpha=0.05)
print(lower, upper, Q)

nfldata['Intercept'] = 1.0
logit_sm = sm.Logit(nfldata['IsTouchdown'], nfldata[["Intercept","YardLine","IsPass","Interaction"]])
fit_sm = logit_sm.fit()
print(fit_sm.summary())


#sklearn
#split a test data
from sklearn.cross_validation import train_test_split
itrain, itest = train_test_split(xrange(df.shape[0]), train_size=0.7)

mask=np.ones(df.shape[0], dtype='int')
mask[itrain]=1
mask[itest]=0
mask = (mask==1)

train = df[mask]
test = df[~mask]

print "###################check for balance######################"
print "The faction of the driver singup took a first trip - train: %.3f" \
%(train.first_completed_date.notnull().sum()/np.float(train.shape[0]))
print "The faction of the driver singup took a first trip - test: %.3f" \
%(test.first_completed_date.notnull().sum()/np.float(test.shape[0]))

#feature engineering

# feature engineering
from sklearn.feature_extraction import DictVectorizer

cols_to_drop = [ ]

X_train_tmp =  train.drop(cols_to_drop, axis = 1).T.to_dict().values()
X_test_tmp =  test.drop(cols_to_drop, axis = 1).T.to_dict().values()

vectorizer = DictVectorizer( sparse = False )

X_train = np.hstack((vectorizer.fit_transform(X_train_tmp)\
                    ,train[['days_signup_veh','days_signup_veh']].values))
X_test = np.hstack((vectorizer.transform(X_test_tmp)\
                    ,test[['days_signup_veh','days_signup_veh']].values))

Y_train = train.y
Y_test = test.y


from sklearn.decomposition import PCA
pca = PCA(n_components=6)
pca.fit(X)
print(pca.explained_variance_ratio_)
print(pca.components_)


#model training
from sklearn.linear_model import LogisticRegression 
from sklearn.grid_search import GridSearchCV

Cs=[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
parameters = {"C":Cs}

clflog = LogisticRegression(penalty="l1")
fitmodel = GridSearchCV(clflog, param_grid=parameters, cv=5, scoring="accuracy")
fitmodel.fit(X_train, Y_train)

#store the best classifer
best=fitmodel.best_estimator_
print "Best parameters:",fitmodel.best_params_
print "Best score",fitmodel.best_score_
print 'Grid score',fitmodel.grid_scores_


from sklearn.metrics import confusion_matrix

training_accuracy = fitmodel.score(X_train, Y_train)
test_accuracy = fitmodel.score(X_test, Y_test)
print "############# based on standard predict ################"
print "Accuracy on training data: %0.2f" % (training_accuracy)
print "Accuracy on test data:     %0.2f" % (test_accuracy)
print confusion_matrix(Y_test, fitmodel.predict(X_test))
print "########################################################"


########Other

#memory
def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper
    
@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print(fib(40))




