import os
import random
import time

# Paths to the text files (one password per line).
ROCKYOU_FILE = os.path.join("datasets", "rockyou_dataset.txt")
HIBP_FILE = os.path.join("datasets", "hibp_dataset.txt")
# CRACKSTATION_FILE = os.path.join("datasets", "crackstation_dataset.txt")


def load_dataset(file_path):
    """
    Reads passwords from a text file (one per line) and returns them as a list.
    """
    data_list = []
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                pwd = line.strip()
                if pwd:
                    data_list.append(pwd)
    return data_list


def build_qnn_model():
    """
    Placeholder for building a quantum neural network model structure.
    Returns a dictionary to represent QNN components.
    """
    # structure to QNN parameters or layers
    model = {
        "num_qubits": 8,
        "layers": [
            {"type": "Hadamard", "params": None},
            {"type": "Entangling", "params": None},
            {"type": "Rotation", "params": {"theta": 0.5}},
        ],
        "optimizer": {"type": "SimulatedQuantumGradient", "learning_rate": 0.01}
    }
    print("[INFO] QNN model initialized with 8 qubits and 3 layers.")
    return model


def train_qnn_model(model, dataset, epochs=3):
    """
    Simulates training steps on the QNN model using the dataset.
    """
    data_size = len(dataset)
    if data_size == 0:
        print("[WARNING] Dataset is empty. No training performed.")
        return

    print(f"[INFO] Starting QNN training on {data_size} samples for {epochs} epochs.")
    for epoch in range(1, epochs + 1):
        random.shuffle(dataset)  
        total_loss = 0.0
        for pwd in dataset:
            loss = random.uniform(0.0, 1.0) * 0.01
            total_loss += loss

            time.sleep(0.0001)

        avg_loss = total_loss / data_size
        print(f"[EPOCH {epoch}] Average Loss: {avg_loss:.5f}")

    print("[INFO] Training complete. Model parameters updated (simulation).")


def main():
    # 1) Load each dataset
    rockyou_data = load_dataset(ROCKYOU_FILE)
    hibp_data = load_dataset(HIBP_FILE)
    # crackstation_data = load_dataset(CRACKSTATION_FILE)

    # 2) Combine into one big list
    combined_data = rockyou_data + hibp_data #+ crackstation_data
    print(f"[INFO] Total combined dataset size: {len(combined_data)}")

    # 3) Build QNN model
    qnn_model = build_qnn_model()

    # 4) Train the QNN model
    train_qnn_model(qnn_model, combined_data, epochs=3)

    # 5) Done
    print("[INFO] QNN training simulation finished.")


if __name__ == "__main__":
    main()
