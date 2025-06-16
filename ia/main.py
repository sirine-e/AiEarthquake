import classify
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)

validation_samples = {
    "1": pd.read_csv('test_samples/sample_42_label_1.csv', header=None).values,
    "2": pd.read_csv('test_samples/sample_2_label_0.csv', header=None).values
}

@app.route('/config', methods=['POST'])
def doConfiguration():
    print("Configuring earthquake detector")
    model_name = "earthquake-cnn"
    if 'model' in request.args:
        model_name = request.args['model']
    classify.config(model_name)
    print("Configuration done")
    return {"status": "ok", "data": f"Configured {model_name}"}

@app.route('/classify', methods=['POST'])
def doClassification():
    if 'data' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
        
    file = request.files['data']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "Empty file"}), 400
        
    try:
        if file.filename.endswith('.npy'):
            data = np.load(file)
        elif file.filename.endswith('.csv'):
            content = file.stream.read().decode('utf-8')
            data = np.array([float(x) for x in content.split(',') if x.strip()])
        else:
            return jsonify({"status": "error", "message": "Only .csv or .npy files accepted"}), 400
        
        data = np.array(data).flatten()
        if data.shape != (512,):
            return jsonify({
                "status": "error",
                "message": f"Need exactly 512 values. Got {len(data)}",
                "expected": 512,
                "received": len(data)
            }), 400
            
        result = classify.classify(data.reshape(1, 512, 1))
        return jsonify({"status": "success", "data": result})
        
    except ValueError as e:
        return jsonify({"status": "error", "message": f"Data format error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({
            "error": "Classification failed",
            "details": str(e)
        }), 500

@app.route('/validate', methods=['POST'])
def doValidation():
    sample_id = request.args.get('id', '0')
    
    try:
        if sample_id not in validation_samples:
            return jsonify({
                "status": "error",
                "message": f"Invalid sample id {sample_id}"
            }), 400
            
        data = validation_samples[sample_id]
        result = classify.classify(data.reshape(1, 512, 1))
        
        return jsonify({
            "status": "success",
            "sample_id": sample_id,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Validation failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting earthquake detection service")
    classify.config("earthquake-cnn")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)