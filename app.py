from flask import Flask,request,jsonify
from PIL import Image
from io import BytesIO
from ultralytics import YOLO

app =Flask(__name__)
model = YOLO('Tickle_S01_70.pt')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


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

def start_processing(image):
    img=Image.open(BytesIO(image.read()))
    cordinates_array=run_model(img)
    if cordinates_array:
        return cordinates_array
    else:
        return 'No segmentation detected',404

def starts_with_5(number):
    number_str = str(number)
    number_str = number_str.lstrip()
    return number_str.startswith('5')

def run_model(image):
    cls_array = []
    cord_array = []
    results = model.predict(source=image, save_crop=False, conf=0.5, project="img.jpg", save_txt=False)
    if results:
        for result in results:
            if result:
                # print(result.boxes.cls)
                cls_array.append(result.boxes.cls)
                # print(result.boxes.xyxy)
                cord_array.append(result.boxes.xyxy)
            else:
                print('No Detection')
                return 0

        cls_array = cls_array[0]
        cls_ind_array = []
        cls_5_cord_array = []

        for index, val in enumerate(cls_array, start=0):
            if (starts_with_5(val.item())):
                cls_ind_array.append(index)

        for index, val in enumerate(cls_ind_array, start=0):
            cord_list = cord_array[0][val].tolist()
            round_cords = [round(coord) for coord in cord_list]
            cls_5_cord_array.append(round_cords)
        # print(cls_5_cord_array)
        return array_brake(cls_5_cord_array)
    else:
        return
def array_brake(array):
    braked_array=[]
    for val in array:
        # print(cord_array[val])
        point_1 = (val[0], val[1])
        point_2 = (val[2], val[1])
        point_3 = (val[0], val[3])
        point_4 = (val[2], val[3])
        # print(f'LineOne: {point_1} LineOne: {point_2} LineTwo: {point_3} LineTwo: {point_4}')
        braked_array.append([point_1, point_2, point_3, point_4])
    # print(braked_array)
    return braked_array

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)