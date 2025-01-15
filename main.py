# main.py
from langchain_integration.generate_gherkin import generate_gherkin
# from langchain_integration.generate_gherkin_VB import generate_gherkin
# from langchain_integration.generate_gherkin_langchain import generate_gherkin
from langchain_integration.generate_steps import generate_step_definitions
from langchain_integration.run_tests import run_java_tests



task_description = "Open a webpage and verify the page title"


feature_path = generate_gherkin(task_description)
print(f"Gherkin scripts saved at {feature_path}")


with open(feature_path, "r") as f:
    feature_text = f.read()
steps_path = generate_step_definitions(feature_text)
print(f"Step definition is generated at {steps_path}")


run_java_tests()
