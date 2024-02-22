from flask import Flask,request,jsonify

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app =Flask(__name__)
@app.route('/upload', methods=['POST'])

def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}),400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}),400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid File type'}), 400
    if file:
        array = start_processing(file)
        if array:
            return jsonify({'result': array}),201
        else:
            return jsonify({'error': 'Array Receiving Failed'}),404

    return jsonify({'error': 'Invalid file format'}),400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_processing(file):

    name = file.filename

    return name

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)