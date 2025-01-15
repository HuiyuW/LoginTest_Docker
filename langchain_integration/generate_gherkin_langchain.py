from langchain import LLMChain, PromptTemplate
from langchain.llms.base import LLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class CustomStarCoderLLM(LLM):
    def __init__(self, model_path, device='cuda'):
        super().__init__()  # 调用父类的初始化方法
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
        self.device = device

    def _call(self, prompt, stop=None):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(inputs, max_length=200, do_sample=True, temperature=0.8, top_p=0.95)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @property
    def _llm_type(self):
        return "custom_starcoder"
    

def generate_gherkin(task_description):
    # 设置模型路径和设备
    model_path = "C:/Huiyu_Wang/Work/code/LLM/starcoder2-3b"  # 替换为你的 Starcoder2 模型路径
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 设置模型路径


    # 初始化自定义 LLM
    llm = CustomStarCoderLLM(model_path=model_path)

    # 创建 Gherkin 提示模板
    gherkin_template = """
    Please write a Gherkin example for the following task:
    Description: {task_description}

    Format:
    Feature: [Description]
      Scenario: [Description]
        Given [Step 1]
        When [Step 2]
        Then [Expected outcome]
    """

    prompt = PromptTemplate(template=gherkin_template, input_variables=["task_description"])
    chain = LLMChain(llm=llm, prompt=prompt)

    # 运行生成 Gherkin 脚本

    gherkin_script = chain.run(task_description)
    print("Generated gherkin_script:", gherkin_script)

    gherkin_script = """
    Feature: Web Page Title and Accessibility Test
      Scenario: Validate webpage title and accessibility score
        Given I navigate to the test URL
        Then I should see the correct page title
    """
    # 将生成的 Gherkin 写入文件
    del llm
    torch.cuda.empty_cache()
    feature_path = "src/test/resources/features/WebPage2.feature"
    with open(feature_path, "w") as f:
        f.write(gherkin_script)

