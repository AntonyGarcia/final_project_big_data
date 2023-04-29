import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
import numpy as np

# Step 1: Define a custom dataset class
class LoadDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def preprocess_data(df):
    # One-hot encode categorical variables
    categorical_features = ['hour_of_day', 'day_of_week', 'month_of_year', 'year', 'is_holiday']
    df = pd.get_dummies(df, columns=categorical_features)

    # Scale continuous variables
    scaler = StandardScaler()
    continuous_features = ['epoch','temperature', 'humidity', 'dew_point', 'temperature_feeling', 'wind_speed', 'rain_1h']
    df[continuous_features] = scaler.fit_transform(df[continuous_features])

    return df

class DeepGRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_gru_layers, num_fc_layers):
        super(DeepGRUModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_gru_layers = num_gru_layers

        self.gru = nn.GRU(input_size, hidden_size, num_layers=num_gru_layers, batch_first=True, dropout=0.2)
        self.dropout = nn.Dropout(0.5)
        self.fc_layers = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_fc_layers)])
        self.output = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_gru_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.gru(x, h0)

        out = self.dropout(out[:, -1, :])
        for fc in self.fc_layers:
            out = torch.relu(fc(out))
            out = self.dropout(out)

        out = self.output(out)
        return out

def train_and_evaluate(X_train, X_test, y_train, y_test, epochs=50, batch_size=64, learning_rate=0.001):
    train_dataset = LoadDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

    input_size = X_train.shape[2]
    hidden_size = 256
    output_size = 1

    best_test_loss = float('inf')
    best_model_state = None

    model = DeepGRUModel(input_size, hidden_size, output_size, num_gru_layers=2, num_fc_layers=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device, dtype=torch.float32), batch_y.to(device, dtype=torch.float32)

            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs.squeeze(), batch_y)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            X_test_tensor = torch.tensor(X_test, device=device, dtype=torch.float32)
            y_test_tensor = torch.tensor(y_test, device=device, dtype=torch.float32)
            test_outputs = model(X_test_tensor)
            test_loss = criterion(test_outputs.squeeze(), y_test_tensor)

            if test_loss.item() < best_test_loss:
                best_test_loss = test_loss.item()
                best_model_state = model.state_dict()
                print(f'Best model updated at epoch [{epoch + 1}/{epochs}], Best Test Loss: {best_test_loss:.4f}')

        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')

    # Load the best model state
    model.load_state_dict(best_model_state)

    return model


def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i : i + seq_length])
    return np.array(sequences)

def prepare_data(filename, seq_length=24):
    original_df = pd.read_csv(filename)
    original_df = original_df.sort_values(by='epoch')
    df = preprocess_data(original_df.copy())

    X = df.drop(['load'], axis=1).values
    y = df['load'].values

    X = create_sequences(X, seq_length)
    y = y[seq_length:]

    split_index = int(0.9 * len(X))

    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Split the original DataFrame into training and testing DataFrames
    original_df_test = original_df.iloc[split_index + seq_length :, :]

    return X_train, X_test, y_train, y_test, original_df_test


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # Load and preprocess data
    seq_length = 24
    X_train, X_test, y_train, y_test, original_df_test = prepare_data('raw_data/final_dataset.csv', seq_length=seq_length)

    # Train and evaluate the GRU model
    trained_model = train_and_evaluate(X_train, X_test, y_train, y_test, epochs=200)

    # Predict test dataset
    with torch.no_grad():
        X_test_tensor = torch.tensor(X_test, device=device, dtype=torch.float32)
        test_outputs = trained_model(X_test_tensor)
        predictions = test_outputs.cpu().numpy().squeeze()

    # Add predictions to the original test DataFrame and export to CSV
    original_df_test['predicted_load'] = predictions
    original_df_test.to_csv('original_test_dataset_with_predictions.csv', index=False)

if __name__ == "__main__":
    main()