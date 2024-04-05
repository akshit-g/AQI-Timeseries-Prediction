import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt
import pickle

class AQIPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AQI Predictor")

        self.seq_length_label = ttk.Label(root, text="Sequence Length:")
        self.seq_length_label.grid(row=0, column=0, padx=10, pady=5)

        self.seq_length_entry = ttk.Entry(root)
        self.seq_length_entry.grid(row=0, column=1, padx=10, pady=5)

        self.predict_button = ttk.Button(root, text="Predict", command=self.predict_aqi)
        self.predict_button.grid(row=0, column=2, padx=10, pady=5)

        self.plot_button = ttk.Button(root, text="Plot", command=self.plot_results)
        self.plot_button.grid(row=0, column=3, padx=10, pady=5)

        self.status_label = ttk.Label(root, text="")
        self.status_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        self.load_model()

    def load_model(self):
        # Load the trained LSTM model
        try:
            with open('aqi_modelseq3.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Model file not found!")
            self.root.destroy()

    def predict_aqi(self):
        try:
            seq_length = int(self.seq_length_entry.get())
            if seq_length < 1:
                raise ValueError("Sequence length must be at least 1.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Load data
        df = pd.read_csv('hour.csv', parse_dates=['Datetime'])

        # Drop rows with NaN values
        df_cleaned = df.dropna()

        # Scaling data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df_cleaned['AQI'].values.reshape(-1, 1))

        X, y = self.create_sequences(scaled_data, seq_length)

        # Predict AQI values
        predictions_lstm = self.model.predict(X)
        predictions_lstm = scaler.inverse_transform(predictions_lstm).flatten()
        y = scaler.inverse_transform(y).flatten()

        # Calculate evaluation metrics
        rmse_lstm = sqrt(mean_squared_error(y, predictions_lstm))
        mse_lstm = mean_squared_error(y, predictions_lstm)
        mae_lstm = mean_absolute_error(y, predictions_lstm)
        r2_lstm = r2_score(y, predictions_lstm)

        self.status_label.config(text=f'LSTM RMSE: {rmse_lstm:.2f}, MSE: {mse_lstm:.2f}, MAE: {mae_lstm:.2f}, R2 Score: {r2_lstm:.2f}')

        self.predictions_lstm = predictions_lstm
        self.actual_values = y

    def create_sequences(self, data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    def plot_results(self):
        try:
            self.predictions_lstm
        except AttributeError:
            messagebox.showerror("Error", "Please predict AQI values first.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.actual_values, label='Actual AQI')
        plt.plot(self.predictions_lstm, label='Predicted AQI')
        plt.xlabel('Time')
        plt.ylabel('AQI')
        plt.title('Actual vs Predicted AQI')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AQIPredictorApp(root)
    root.mainloop()
