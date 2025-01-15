import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def generate_step_definitions(feature_text):

    path = "C:/Huiyu_Wang/Work/code/LLM/starcoder2-3b"  
    device = "cuda" if torch.cuda.is_available() else "cpu"


    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path).to(device)


    prompt = f"""
    Generate Java step definitions for this Gherkin feature:

    {feature_text}
    Provide the Java `step definitions` class in the following format:
    - Each Gherkin step should have a corresponding Java method with annotations.
    - Implement Selenium code where necessary, and use assertions to validate expected outcomes.
    - Provide comments for each method to clarify purpose and actions.

    Format:
    // Java step definitions
    public class WebPageSteps {{
        // Define step methods here
    }}
    Example:

    // Java step definitions for Web Page Title Verification
    public class WebPageTitleSteps {{
        
        WebDriver driver = new ChromeDriver();

        @Given("I open the test URL in the browser")
        public void openTestURL() {{
            driver.get("https://example.com"); // Replace with actual URL
        }}

        @When("the page loads completely")
        public void pageLoadsCompletely() {{
            // Wait for page to fully load
        }}

        @Then("I should see the expected page title {{string}}")
        public void verifyPageTitle(String expectedTitle) {{
            String actualTitle = driver.getTitle();
            assertEquals(expectedTitle, actualTitle);
        }}
    }}
    ### Start Output
    Output begins below:
    
    """


    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    inputs = torch.cat([inputs, torch.tensor([[tokenizer.eos_token_id]], device=inputs.device)], dim=1)


    with torch.no_grad():
        outputs = model.generate(inputs, max_length=1000, do_sample=True, temperature=0.8, top_p=0.95, num_return_sequences=1)
        steps_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Generated Response:", steps_code)
        step_path_LLM = "src/test/resources/features/LLM_generated.java"
        with open(step_path_LLM, "w",encoding="utf-8") as f:
            f.write(steps_code)
    steps_code = """
    package huiyu.stepdefinitions2;

    import static org.junit.jupiter.api.Assertions.assertEquals;

    import huiyu.BaseTest;
    import huiyu.Config;
    import io.cucumber.java.AfterAll;
    import io.cucumber.java.Before;
    import io.cucumber.java.en.Given;
    import io.cucumber.java.en.Then;

    public class WebPageSteps2 extends BaseTest {
        @Before
        public void init() {
            setUp();
        }

        @Given("I navigate to the test URL")
        public void i_navigate_to_the_test_url() {
            driver.get(Config.TEST_URL);
        }

        @Then("I should see the correct page title")
        public void i_should_see_the_correct_page_title() {
            String expectedTitle = "T-Rex Self-Service";  // Replace with actual expected title
            assertEquals(expectedTitle, driver.getTitle());
        }

        @AfterAll
        public static void afterAllTests() {
            runLighthouse();
        }
    }
    """
    del model
    torch.cuda.empty_cache()

    steps_path = "src/test/java/huiyu/stepdefinitions2/WebPageSteps2.java"
    with open(steps_path, "w") as f:
        f.write(steps_code)

    return steps_path


