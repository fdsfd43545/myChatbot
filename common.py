




def get_content_from_llm(client,
                         *,
                         system_prompt='',
                         few_shot_prompt=[],
                         user_prompt='',
                         model_name='deepseek-v4-flash',
                         temperature=0.6,
                         top_p=0.1,
                         frequency_penalty=0,
                         max_tokens=512,):
    """
    大模型有没有记忆

    获取大模型API响应内容
    :param client: OpenAI客户端
    :param system_prompt:系统提示词
    :param few_shot_prompt: 小样本提示
    :param user_prompt:用户提示词
    :param model_name:模型名称
    :param temperature: 温度参数(0~2)
    :param top_p:百分比排名参数(0~1)
    :param frequency_penalty: 频率惩罚力度(-2~2)
    :param max_tokens: 最大token数量
    :return:响应的内容
    """
    messages = []
    if system_prompt.strip():
        messages.append({'role': 'system','content': system_prompt})
    if few_shot_prompt:
        messages += few_shot_prompt
    if user_prompt.strip():
        messages.append({'role': 'user','content': user_prompt})
    response = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        max_tokens=max_tokens,
        messages=messages,
        stream=False        #False给完整的内容，不是一段一段的
    )
    return response.choices[0].message.content