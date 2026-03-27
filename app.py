from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    # 获取播放地址，例如：域名/?url=http://xxx.m3u8
    target_url = request.args.get('url')
    
    if not target_url:
        return "请在 URL 后方加入 ?url=直播源地址", 400

    # 模拟请求头，避开部分源站的防盗链
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': target_url
    }

    try:
        # stream=True 是关键，边下载边发送，不占用服务器内存
        r = requests.get(target_url, headers=headers, stream=True, timeout=15)
        
        # 将源站的响应头透传给播放器（主要是 Content-Type）
        return Response(
            r.iter_content(chunk_size=1024 * 512), # 每次转发 512KB
            content_type=r.headers.get('Content-Type', 'video/mp2t'),
            status=r.status_code
        )
    except Exception as e:
        return f"代理出错: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
