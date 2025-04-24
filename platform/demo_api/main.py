import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 读取 API 信息
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_API_URL")
model = os.getenv("DEEPSEEK_MODEL_NAME")

# 初始化 DeepSeek API 客户端
client = OpenAI(api_key=api_key, base_url=base_url, model=model)

# 与 DeepSeek 聊天的函数
def chat_with_deepseek(user_input):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"出错了: {e}"

# 创建 Gradio 界面
iface = gr.Interface(
    fn=chat_with_deepseek,
    inputs=gr.Textbox(label="请输入问题"),
    outputs=gr.Textbox(label="DeepSeek 的回复"),
    title="DeepSeek 聊天助手",
    description="输入问题，与 DeepSeek 模型互动。"
)

# 启动网页应用
if __name__ == "__main__":
    iface.launch()