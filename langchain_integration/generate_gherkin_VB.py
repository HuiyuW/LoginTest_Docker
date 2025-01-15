import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_integration.vector_database import VectorDatabase
from langchain_integration.prepare_vector_db import prepare_database



def generate_gherkin(task_description):
    # 初始化向量数据库
    vector_db = prepare_database()#导入
    example_results = vector_db.search(task_description, top_k=1)  # 搜索最相似的示例
    # 设置模型路径和设备
    path = "C:/Huiyu_Wang/Work/code/LLM/starcoder2-3b"  # 替换为你的 Starcoder2 模型路径
    
    # path = "C:/Huiyu_Wang/Work/code/LLM/Llama-2-7b-hf"  # 替换为你的 Starcoder2 模型路径
    # 将相似示例添加到 prompt 中
    example_text = example_results[0][0] if example_results else ""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path).to(device)
    # 定义用于生成 Gherkin 脚本的提示
    prompt = f"""
    Gherkin feature file is a semi-formal specification. Please write a detailed Gherkin feature file for the following task:
    {task_description}

    Provide the feature file in the following format with relevant tags:
      - **Feature**: Summarize the goal, purpose, or function being tested.
      - **Scenario**: Describe each test case scenario with clear Given/When/Then steps.
      - **Tags**: Use tags like `@regression` or `@smoke` to categorize scenarios.
    
    Based on the following example:
    {example_text}
    Format:
    Feature: [Brief Feature Description]
      Scenario: [Scenario Description]
        Given [Action or starting state]
        When [Test step or action]
        Then [Expected outcome or verification]
    
    ### Start Output
    Output begins below:
    """

    # 编码输入
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    inputs = torch.cat([inputs, torch.tensor([[tokenizer.eos_token_id]], device=inputs.device)], dim=1)

    # 生成输出
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=1000, do_sample=True, temperature=0.8, top_p=0.95, num_return_sequences=1)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Generated Response:", response)
        feature_path_LLM = "src/test/resources/features/LLM_generated.feature"
        with open(feature_path_LLM, "w",encoding="utf-8") as f:
            f.write(response)
    response = """
    Feature: Web Page Title and Accessibility Test
      Scenario: Validate webpage title and accessibility score
        Given I navigate to the test URL
        Then I should see the correct page title
    """
    # 将生成的 Gherkin 写入文件
    del model
    torch.cuda.empty_cache()
    feature_path = "src/test/resources/features/WebPage2.feature"
    with open(feature_path, "w") as f:
        f.write(response)

    return feature_path

