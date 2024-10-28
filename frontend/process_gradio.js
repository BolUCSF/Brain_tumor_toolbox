document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('gradio-container');
    
    try {
        // 获取 Gradio 界面的 URL
        const response = await fetch('http://localhost:5001/gradio');
        const data = await response.json();
        const gradioUrl = data.url;

        // 创建一个 iframe 来加载 Gradio 界面
        const iframe = document.createElement('iframe');
        iframe.src = gradioUrl;
        iframe.style.width = '100%';
        iframe.style.height = '600px';
        iframe.style.border = 'none';

        // 将 iframe 添加到容器中
        container.appendChild(iframe);

    } catch (error) {
        console.error('Error loading Gradio interface:', error);
        container.innerHTML = '<p>Error loading Gradio interface. Please check the console for details.</p>';
    }
});