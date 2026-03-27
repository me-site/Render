<?php
// 获取播放链接，例如 index.php?url=http://target.com/live.m3u8
$target_url = $_GET['url'];

if (filter_var($target_url, FILTER_VALIDATE_URL)) {
    // 设置 Header 模拟浏览器或特定播放设备
    $options = [
        "http" => [
            "header" => "User-Agent: Mozilla/5.0\r\n",
            "timeout" => 10
        ]
    ];
    $context = stream_context_create($options);
    
    // 设置正确的 Content-Type（根据实际流格式调整）
    header("Content-Type: video/mp2t");
    
    // 读取并直接输出流数据
    readfile($target_url, false, $context);
} else {
    echo "Invalid URL";
}
?>
