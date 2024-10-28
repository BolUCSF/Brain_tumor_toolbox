from flask import Flask, request, jsonify, Response
import time
from brats_image import brats_image_set

app = Flask(__name__)

global_image_set = None

@app.route('/api/upload_paths', methods=['POST'])
def upload_paths():
    data = request.get_json()  # 获取 JSON 数据
    paths = data.get('paths', {})  # 从数据中提取路径
    print('Received paths:', paths)  # 打印接收到的路径（可选）

    global global_image_set
    global_image_set = brats_image_set(data['paths'])

    # 在这里可以添加处理路径的逻辑

    return jsonify({'status': 'success', 'message': 'Paths received successfully.'})

@app.route('/api/start_registration', methods=['POST'])
def start_registration():
    data = request.get_json()  # 获取 JSON 数据
    print(data)
    brainmask_needed = data.get('brainmask', False)  # 从数据中提取开关状态
    paths = data.get('paths', {})
    global global_image_set
    global_image_set = brats_image_set(data['paths'])
    print('Brainmask needed:', brainmask_needed)  # 打印开关状态（可选）

    # log = global_image_set.registration_image(brainmask_needed)
    log = (line + '\n' for line in global_image_set.registration_image(brainmask_needed))
    # log = "test"

    return Response(log, mimetype='text/plain')  # 返回流式响应

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 启动 Flask 应用
