import pandas as  pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


# Load the dataset
df = pd.read_csv('../weather/nairobi_weather.csv')

df['rain_flag'] = (df['prcp'] > 0).astype(int)
# Feature engineering
df['date'] = pd.to_datetime(df['time'])

#features
features = ['tavg','tmin','tmax',
            'prcp','snow','wdir','wspd',
            'wpgt','pres','tsun']
df = df.ffill().bfill()
X = df[features]
y = df['rain_flag']
print('Features shape:', X.shape)
print('y shape:', y.value_counts())
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
# Cross-validation
cv_scores = cross_val_score(clf, X, y, cv=5)
print("Cross-validation scores:", cv_scores)

# Save the model
joblib.dump(clf, 'rain_prediction_model.pkl')