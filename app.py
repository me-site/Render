from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "请在 URL 后方加入 ?url=直播源地址", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': target_url
    }

    try:
        # 增加 timeout 到 20 秒，容忍跨境网络波动
        r = requests.get(target_url, headers=headers, stream=True, timeout=20)
        
        # 这里的 chunk_size 设置为 256KB，平衡延迟和稳定性
        def stream_gen():
            for chunk in r.iter_content(chunk_size=262144):
                if chunk:
                    yield chunk

        return Response(
            stream_gen(),
            content_type=r.headers.get('Content-Type', 'video/mp2t'),
            status=r.status_code
        )
    except Exception as e:
        return f"Singapore Proxy Error: {str(e)}", 500

if __name__ == "__main__":
    # Render 默认使用 10000 端口
    app.run(host='0.0.0.0', port=10000)
