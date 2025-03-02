import requests
import json

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-qwdwjtytflqpvxphwoxkyghgjpsgeqwtsfpgqgrsildxwawv"  # 替换为你的 API Key

def chat_with_llm(user_input, max_chars=5000, max_tokens=1024):
    messages = [
        {"role": "system", "content": "你是一个旅游问答助手，专门解答洪崖洞景区的相关问题。"},
        {"role": "user", "content": user_input}
    ]
    payload = {
        "model": "Pro/deepseek-ai/DeepSeek-V3",
        "messages": messages,
        "stream": True,  # 开启流式响应
        "max_tokens": max_tokens,  # 增加 max_tokens 限制
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "stop": None
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # 优化请求：增加超时设置，避免长时间等待
    try:
        response = requests.post(API_URL, json=payload, headers=headers, stream=True, timeout=10)
    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试。"
    except requests.exceptions.RequestException as e:
        return f"请求错误: {e}"
    reply = ""
    try:
        for chunk in response.iter_lines():
            if chunk:
                decoded_data = chunk.decode('utf-8').strip()
                # 解析 JSON 格式的数据流
                if decoded_data.startswith("data: "):
                    json_data = decoded_data[6:]  # 去掉 "data: " 前缀
                    try:
                        parsed_data = json.loads(json_data)
                        if "choices" in parsed_data and parsed_data["choices"]:
                            content = parsed_data["choices"][0]["delta"].get("content", "")
                            # 确保 content 不是 None
                            if content:
                                reply += content
                                print(content, end="", flush=True)  # 实时打印每一部分
                            
                            # 限制最大字符数，防止过长输出
                            if len(reply) >= max_chars:
                                print("\n[回答截断...]")
                                break
                    except json.JSONDecodeError:
                        continue  # 忽略解析错误，继续读取流
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return "对不起，请求失败，请稍后重试。"
    return reply.strip()  # 返回最终拼接的内容

str = input()
# bot_reply = chat_with_llm("洪崖洞晚上好玩吗？")

bot_reply = chat_with_llm(str)
# print("\n助手:", bot_reply)
