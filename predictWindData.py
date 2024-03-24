import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

from readGovData import query

def print_predictions(Year, Month, Day):
    df = query(Year, Month, Day)
    model_path = 'PATH TO H5 MODEL'
    model = tf.keras.models.load_model(model_path)

    df_subset = df.iloc[:, 4:]
    scaler = joblib.load('PATH TO SCALER.pkl')
    df_scaled = scaler.transform(df_subset)

    predictions = model.predict(df_scaled)
    predictions_df = pd.DataFrame(predictions, columns=['Lull', 'Average', 'Gust'])
    plt.plot(df['Hour'], predictions_df['Lull'], label='Predicted Lull', color='red')
    plt.plot(df['Hour'], predictions_df['Average'], label='Predicted Average', color='red', linestyle='dashed')
    plt.plot(df['Hour'], predictions_df['Gust'], label='Predicted Gust', color='red', linestyle='dotted')

    plt.xticks(np.arange(df['Hour'].min(), df['Hour'].max()+1, 1))
    plt.ylim(0, 25)
    plt.xlim(8, 20)

    # Add title
    plt.title(f"Squamish Prediction for {Year}-{Month}-{Day}")
    # Show the plot
    plt.show()

if __name__ == "__main__":
    print_predictions(Year=2024, Month=3, Day=1)
