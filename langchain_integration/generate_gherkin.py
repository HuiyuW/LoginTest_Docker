import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

import time



def generate_gherkin(task_description):
    # 设置模型路径和设备
    path = "C:/Huiyu_Wang/Work/code/LLM/starcoder2-3b"  # 替换为你的 Starcoder2 模型路径
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, quantization_config=config).to(device)
    # 定义用于生成 Gherkin 脚本的提示
    prompt = f"""
    Please write a Gherkin example for the following task:
    {task_description}

    Format:
    Feature: [Description]
      Scenario: [Description]
        Given [Step 1]
        When [Step 2]
        Then [Expected outcome]
    """

    # 编码输入
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    inputs = torch.cat([inputs, torch.tensor([[tokenizer.eos_token_id]], device=inputs.device)], dim=1)

    # 生成输出
    with torch.no_grad():
        start_time = time.time()
        outputs = model.generate(inputs, max_length=200, do_sample=True, temperature=0.8, top_p=0.95, num_return_sequences=1)
        end_time = time.time()
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Total Duration: {end_time - start_time:.2f} seconds\n")
        print("Generated Response:", response)
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

