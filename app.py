import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    # 获取参数：https://your-url.onrender.com/?url=直播源地址
    target_url = request.args.get('url')
    
    if not target_url:
        return "<h1>IPTV Proxy is Running</h1><p>用法: ?url=直播源地址</p>", 200

    # 伪装请求头，防止部分源站屏蔽
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': target_url
    }

    try:
        # 使用 stream=True 实现流式转发，不占用 Render 珍贵的 512MB 内存
        r = requests.get(target_url, headers=headers, stream=True, timeout=20)
        
        def generate():
            for chunk in r.iter_content(chunk_size=262144): # 256KB 缓冲区
                if chunk:
                    yield chunk

        return Response(
            generate(),
            content_type=r.headers.get('Content-Type', 'video/mp2t'),
            status=r.status_code
        )
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == "__main__":
    # Render 必须监听 0.0.0.0，端口由环境变量 $PORT 指定（默认10000）
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
