# -*- coding: utf-8 -*-
"""Untitled43.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13a84udDhiScJfWqGXLpgZ6xjptStLHUY

**INSTALLING STREAMLIT AND PYNGROK**
"""

from google.colab import drive
drive.mount('/content/drive')

# Install Streamlit and ngrok
!pip install streamlit -q
!pip install pyngrok

"""**MODEL TRAINING,TESTING AND WRITING IT TO STREAMLIT APP**"""

Commented out IPython magic to ensure Python compatibility.
# Write the Streamlit app to a file
%%writefile app.py
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import streamlit as st

# Load the dataset
file_path = '/content/drive/My Drive/miniproject/ration.csv'  # Update this to the correct path
data = pd.read_csv(file_path)

st.title("Ration Card Type Prediction")

st.write("Columns in the dataset:", data.columns)

data.columns = data.columns.str.strip()

label_encoders = {}
for column in ['Location', 'Electrified', 'Water_Connection', 'Government_Job', 'Ration_Card_Type']:
    if column in data.columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
    else:
        st.write(f"Column '{column}' not found in the dataset")

X = data.drop('Ration_Card_Type', axis=1)
y = data['Ration_Card_Type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
rf_model = RandomForestClassifier(n_estimators=10, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

cv_scores = cross_val_score(rf_model, X, y, cv=5)
st.write(f"Cross-validation scores: {cv_scores}")
st.write(f"Mean cross-validation score: {cv_scores.mean()}")

st.write(f"Accuracy: {accuracy_score(y_test, y_pred)}")
st.write(classification_report(y_test, y_pred))

st.header("Predict Ration Card Type")

user_input = {}
for column in X.columns:
    if column in label_encoders:
        le = label_encoders[column]
        options = list(le.classes_)
        value = st.selectbox(f"Select value for {column}", options)
        user_input[column] = le.transform([value])[0]
    else:
        value = st.text_input(f"Enter the value for {column}")
        user_input[column] = float(value)

if st.button("Predict"):
    user_df = pd.DataFrame([user_input])
    prediction = rf_model.predict(user_df)
    ration_card_type = label_encoders['Ration_Card_Type'].inverse_transform(prediction)
    st.write(f"The predicted Ration Card Type is: {ration_card_type[0]}")

"""**GENERATING LOCAL TUNNEL PASSWORD**"""

!wget -q -O - ipv4.icanhazip.com

!streamlit run app.py & npx localtunnel --port 8501
