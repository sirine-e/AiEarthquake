import tensorflow as tf
import numpy as np
import joblib

classifier = None
input_length = 512  
classes = ['No Earthquake', 'Earthquake']  

model_handle_map = {
    "earthquake-cnn": "./graphs/model-cnn.keras",  
    "earthquake-rnn": "./graphs/model-rnn.keras",
    "earthquake-mlp": "./graphs/model-mlp.keras",
}

def config(model_name="earthquake-cnn"):
    global classifier
    
    def load_model(model_name):
        global classifier
        try:
            model_path = model_handle_map[model_name]
            classifier = tf.keras.models.load_model(model_path)
            print(f"Successfully loaded model from {model_path}")
        except Exception as e:
            print(f"Model loading failed: {type(e)}: {e.args}")
            raise

    def dry_run():
        test_input = np.random.rand(1, input_length, 1)
        _ = classifier.predict(test_input)
        print("Dry run successful")

    load_model(model_name)
    dry_run()

def preprocess_timeseries(data):
    scaler = joblib.load('scaler.save')

    if data.ndim == 1:
        data = data.reshape(1, -1)
    elif data.ndim == 3:
        data = data.squeeze(axis=2)

    if data.shape[1] != input_length:
        raise ValueError(f"Input must have 512 features. Got {data.shape[1]}")

    data = scaler.transform(data)
    return data.reshape(data.shape[0], data.shape[1], 1)


def classify(timeseries_data):
    global classifier

    processed_data = preprocess_timeseries(timeseries_data)
    probabilities = classifier.predict(processed_data)

    results = []
    for prob in probabilities:
        pred_class = int(prob > 0.5)
        results.append({
            "class": classes[pred_class],
            "probability": float(prob),
            "is_earthquake": bool(pred_class)
        })
    return results

if __name__ == "__main__":
    config("earthquake-cnn")

    test_data = np.random.rand(input_length) 

    predictions = classify(test_data)
    
    for i, pred in enumerate(predictions):
        print(f"Sample {i+1}:")
        print(f"  Prediction: {pred['class']}")
        print(f"  Probability: {pred['probability']:.4f}")
        print(f"  Is earthquake: {pred['is_earthquake']}\n")