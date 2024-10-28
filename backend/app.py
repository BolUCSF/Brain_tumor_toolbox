# app.py
from flask import Flask, jsonify, request
import gradio as gr
from brats_image import brats_image_set

app = Flask(__name__)

# 定义全局变量
global_image_set = None

# 上传路径并初始化 brats_image_set
@app.route('/api/upload_paths', methods=['POST'])
def upload_paths():
    global global_image_set  # 声明使用全局变量
    data = request.json
    print("Received file paths:", data['paths'])  # 打印接收到的路径
    
    # 初始化 brats_image_set
    global_image_set = brats_image_set(data['paths'])  # 根据接收到的路径初始化

    return jsonify({"status": "success", "received_paths": data['paths']})

# 定义 Gradio 应用
def update_textboxes():
    return (global_image_set.T1,global_image_set.T1C,global_image_set.T2,global_image_set.FLAIR)

# 初始化 Gradio 界面
with gr.Blocks() as gradio_interface:
    with gr.Row():
        with gr.Column(scale=1):  # 左侧 4 个文本框
            text1 = gr.Textbox(label="")
            text2 = gr.Textbox(label="")
            text3 = gr.Textbox(label="")
            text4 = gr.Textbox(label="")
        with gr.Column(scale=1):  # 右侧 4 个按钮
            button1 = gr.Button("Button 1")

            button1.click(
                fn=update_textboxes,
                inputs=None,
                outputs=[text1, text2, text3, text4]
            )



# 用于启动 Gradio 并获取 URL
@app.route("/gradio")
def launch_gradio():
    # 启动 Gradio 应用并获取端口
    app_gradio, local_url, share_url = gradio_interface.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        share=False,
        inbrowser=False, 
        prevent_thread_lock=True
    )
    return {"url": local_url}

# 启动 Flask 服务器
if __name__ == "__main__":
    app.run(port=5000)
