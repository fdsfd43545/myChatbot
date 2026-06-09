# 导入 streamlit 库，用于快速构建 Web 应用界面
import streamlit as st

# 从 openai 库导入 OpenAI 客户端类，用于与大模型 API 进行通信
from openai import OpenAI

# 从本地文件 common.py 中导入自定义函数 get_content_from_llm，用于封装获取模型回复的逻辑
from common import get_content_from_llm


# 定义一个函数，用于获取 AI 对用户问题的回复
def get_ai_response(question):
    # 从会话状态中取出最后两条消息：history 是上一轮 AI 的回复，question 是当前用户的新输入
    # 注意：这里的逻辑假设消息列表至少有两条数据，否则会出错
    history, question = st.session_state['messages'][-2:]

    # 调用封装好的函数获取大模型回复
    # 参数包括：客户端对象、模型名称、以及将历史回复和当前问题拼接后的提示词
    return get_content_from_llm(client,
                                model_name=model_name,
                                user_prompt=f'{history[1]},{question[1]}'
                                )


# 侧边栏配置区域
with st.sidebar:
    # 在侧边栏创建一个单选按钮，让用户选择 API 服务提供商（OpenAI 或 Deepseek）
    api_vendor = st.radio(
        "选择你的服务器厂商",
        ('openai', 'Deepseek')
    )

    # 根据用户选择的厂商，设置不同的模型选项列表和 API 基础 URL
    if api_vendor == 'openai':
        # OpenAI 厂商可用的模型列表（注意：此处示例中的 gpt-4o-mini 和 gpt-3o-mini 可能是演示名称，实际请以官方为准）
        options = ['gpt-4o-mini', 'gpt-3o-mini']
        # 使用了一个特定的 OpenAI 香港中转 API 地址
        base_url = 'https://twapi.openai-hk.com/v1'
    elif api_vendor == 'Deepseek':
        # Deepseek 厂商可用的模型列表（注意：deepseek-v4-flash 可能是演示名称，实际请以官方为准）
        options = ['deepseek-v4-flash']
        # Deepseek 官方 API 地址
        base_url = 'https://api.deepseek.com'

    # 在侧边栏创建一个下拉选择框，让用户选择具体的模型
    model_name = st.selectbox('选择你的模型：', options)

    # 在侧边栏创建一个密码输入框，用于用户输入 API Key（输入内容会被隐藏）
    api_key = st.text_input(label='提供你的api key', type='password')

# 初始化会话状态中的消息列表
# 如果 session_state 中没有 'messages' 键，则创建一个包含初始 AI 消息的列表
# 只要网页没关闭，这个列表就会一直保留（实现简单的上下文记忆）
if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai', '你好主人，我是你的助手，贝利亚')]

# 在主界面写入一个标题
st.write('# 空空的deepseek')

# 检查用户是否输入了 API Key
if not api_key:
    # 如果没有输入 API Key，在主界面显示错误信息
    st.error('请输入你的APIKEY')
    # 停止脚本执行，防止后续代码运行出错
    st.stop()

# 创建 OpenAI 客户端实例
# 指定 base_url（API 地址）和 api_key（认证密钥）
client = OpenAI(base_url=base_url, api_key=api_key)

# 遍历会话状态中的所有消息，并在界面上显示
for role, content in st.session_state['messages']:
    # 根据角色（ai 或 human）创建不同的聊天消息气泡
    st.chat_message(role).write(content)

# 在主界面底部创建一个聊天输入框
user_input = st.chat_input()

# 如果用户输入了内容（按下回车）
if user_input:
    # 在界面上显示用户输入的消息
    st.chat_message('human').write(user_input)

    # 将用户输入的消息追加到会话状态的消息列表中，格式为 ('角色', '内容')
    st.session_state['messages'].append(('human', user_input))

    # 显示一个加载中的旋转图标，提示用户等待 AI 回复
    with st.spinner('贝利亚正在思考，请等待'):
        # 调用函数获取 AI 的回复
        resp_from_ai = get_ai_response(user_input)

        # 在界面上显示 AI 的回复
        st.chat_message('assistant').write(resp_from_ai)

        # 将 AI 的回复追加到会话状态的消息列表中
        st.session_state['messages'].append(('ai', resp_from_ai))
