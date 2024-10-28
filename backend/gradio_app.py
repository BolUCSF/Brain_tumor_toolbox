from flask import Flask, jsonify, request
import gradio as gr
from brats_image import brats_image_set
from tkinter import Tk, filedialog

app = Flask(__name__)


@app.route('/api/upload_paths', methods=['POST'])
def upload_paths():
    data = request.json
    print("Received file paths:", data['paths'])  # 打印接收到的路径
    return jsonify({"status": "success", "received_paths": data['paths']})

# 定义 Gradio 应用
def greet(name):
    return f"Hello, {name}!"

def button_clicked():
    # 隐藏主Tk窗口
    root = Tk()
    root.withdraw()
    # 打开文件选择器
    file_path = filedialog.askopenfilename()
    return file_path if file_path else "No file selected"

with gr.Blocks() as gradio_interface:
    with gr.Row():
        with gr.Column(scale=1):  # 左侧 4 个文本框
            text1 = gr.Textbox(label="Textbox 1")
            text2 = gr.Textbox(label="Textbox 2")
            text3 = gr.Textbox(label="Textbox 3")
            text4 = gr.Textbox(label="Textbox 4")
        with gr.Column(scale=1):  # 右侧 4 个按钮
            button1 = gr.Button("Button 1")
            button2 = gr.Button("Button 2")
            button3 = gr.Button("Button 3")
            button4 = gr.Button("Button 4")
            
            # 为每个按钮设置点击事件
            button1.click(fn=lambda: button_clicked(), outputs=text1)
            button2.click(fn=lambda: button_clicked(), outputs=text2)
            button3.click(fn=lambda: button_clicked(), outputs=text3)
            button4.click(fn=lambda: button_clicked(), outputs=text4)

# 用于启动 Gradio 并获取 URL
@app.route("/gradio")
def launch_gradio():
    # 启动 Gradio 应用并获取端口
    app_gradio, local_url, share_url = gradio_interface.launch(
        server_name="0.0.0.0", 
        server_port=7861, 
        share=False,
        inbrowser=False, 
        prevent_thread_lock=True
    )
    return {"url": local_url}

# 启动 Flask 服务器
if __name__ == "__main__":
    app.run(port=5001)