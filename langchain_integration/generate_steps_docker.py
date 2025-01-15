import os
import time
from transformers import AutoTokenizer, LlamaForCausalLM, pipeline, AutoModelForCausalLM
from langchain import LLMChain, HuggingFacePipeline, PromptTemplate
import torch
from datetime import datetime
import gc

def generate_step_definitions(task_gherkin):
    model_paths = [
        # "C:/Huiyu_Wang/Work/code/LLM/Llama-3.1-8B-Instruct",
        "C:/Huiyu_Wang/Work/code/LLM/starcoder2-3b"
    ]


    device = torch.device("cuda:0")


    template = '''
    I am using Java + Selenium + Cucumber for automated testing, with the following setup:

    Java Version: 11
    Testing Framework: JUnit 4
    Selenium Version: 4.11.0
    Cucumber-Java Version: 7+
    All Step Definitions classes go in a steps package.
    There is a Hooks class where @Before and @After manage WebDriver initialization and teardown, accessed via Hooks.driver.
    Desired Output Format
    No repetition of the entire prompt in your final output.
    For each Gherkin step, provide a @Given, @When, or @Then-annotated Java method in the Step Definitions file.
    Use Selenium to locate elements and perform actions/validations.
    Use placeholders (By.id("TODO"), // TODO comments) if any locator/assertion is not determined.
    The final code should start with:
    package steps;

    and include necessary imports like:

    import io.cucumber.java.en.*;
    import org.openqa.selenium.*;
    import static org.junit.Assert.*;

    Example of Gherkin + Step Definitions
    Sample Gherkin
    Feature: Login Feature
    Scenario: Login with valid credentials
        Given I open the login page
        When I fill in username "validUser" and password "secretPass"
        And I click on the login button
        Then I should see the dashboard

    Sample Step Definitions
    package steps;

    import io.cucumber.java.en.Given;
    import io.cucumber.java.en.When;
    import io.cucumber.java.en.Then;
    import org.openqa.selenium.By;
    import org.openqa.selenium.WebDriver;
    import static org.junit.Assert.assertTrue;

    public class LoginStepDefs {{

        private WebDriver driver;

        public LoginStepDefs() {{
            this.driver = Hooks.driver;
        }}

        @Given("I open the login page")
        public void iOpenTheLoginPage() {{
            driver.get("https://example.com/login");
        }}

        @When("I fill in username {{string}} and password {{string}}")
        public void iFillInUsernameAndPassword(String username, String password) {{
            driver.findElement(By.id("username_field")).sendKeys(username);
            driver.findElement(By.id("password_field")).sendKeys(password);
        }}

        @When("I click on the login button")
        public void iClickOnTheLoginButton() {{
            driver.findElement(By.id("login_button")).click();
        }}

        @Then("I should see the dashboard")
        public void iShouldSeeTheDashboard() {{
            boolean dashboardVisible = driver.findElement(By.id("dashboard_page")).isDisplayed();
            assertTrue("Dashboard should be visible after login", dashboardVisible);
        }}
    }}

    New Gherkin Feature to Process
    Please generate Step Definitions directly (without repeating this prompt) for:
    {task}

    Instructions
    Provide a Java class, package steps;, necessary imports, and a WebDriver instance.
    Write separate annotated methods for each step.
    Use placeholders if locators or assertions are unknown.
    ##Do not repeat the entire prompt text in your output. Just output the Java code and optionally a brief explanation after.
    ### Start Output
    Output begins below:
    '''

    # task_gherkin = '''
    # Scenario: View job list and job detail
    #     Given I am on the T-Rex dashboard after logging in
    #     When I click on "Jobs" in the main menu
    #     Then I should see the job list
    #     When I select one job from the list
    #     Then I should see the job detail page
    # '''
    prompt = PromptTemplate(
        input_variables=["task"],
        template=template
    )


    for model_path in model_paths:

        model_name = os.path.basename(model_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"step_definition_withexample_{timestamp}_{model_name}.txt"
        with open(log_file, "w", encoding="utf-8") as log:

            log.write(f"Model Path: {model_path}\n")
            log.write(f"Device: {device}\n")
            log.write("Parameters: max_length=2048, top_p=1, repetition_penalty=1.15\n\n")


            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map=device)
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=2048,
                top_p=1,
                repetition_penalty=1.15
            )
            llama_model = HuggingFacePipeline(pipeline=pipe)
            chain = LLMChain(llm=llama_model, prompt=prompt)

    
            start_time = time.time()
            log.write(f"Experiment Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n\n")

            total_tokens = 0

            for i in range(1, 2):
                log.write(f"--- Test Run {i} ---\n")
                print(f"--- Test Run {i} ---\n")
                test_start = time.time()

    
                result = chain.run(task=task_gherkin)
                test_end = time.time()

                num_tokens = len(tokenizer.encode(result))
                total_tokens += num_tokens
                tokens_per_second = num_tokens / (test_end - test_start)

    
                log.write(f"Output:\n{result}\n")
                print(f"Output:\n{result}\n")
                log.write(f"Test Run {i} Duration: {test_end - test_start:.2f} seconds\n")
                log.write(f"Generated Tokens: {num_tokens}\n")
                log.write(f"Generation Speed: {tokens_per_second:.2f} tokens/sec\n\n")
                print(f"Test Run {i} Duration: {test_end - test_start:.2f} seconds\n")
                print(f"Generated Tokens: {num_tokens}")
                print(f"Generation Speed: {tokens_per_second:.2f} tokens/sec\n")


            end_time = time.time()
            log.write(f"Experiment End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
            log.write(f"Total Duration: {end_time - start_time:.2f} seconds\n")
            log.write(f"Total Generated Tokens: {total_tokens}\n")
            print(f"Total Generated Tokens: {total_tokens}\n")
        del chain
        del llama_model
        del pipe
        del model
        del tokenizer


        gc.collect()

        torch.cuda.empty_cache()

    print("All experiments completed.")
    steps_code = """
package huiyu.stepdefinitions_login_test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import huiyu.BaseTest;
import huiyu.Config;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class LoginTest_test extends BaseTest {

    private WebDriverWait wait;

    @Before
    public void init() {
        setUp();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Given("I open the login page")
    public void i_open_the_login_page() {
        driver.get(Config.TEST_URL); // 访问测试页面
    }


    @When("I enter username {string} and password {string}")
    public void i_enter_username_and_password(String username, String password) {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    
        // 等待 Username 输入框可见
        WebElement usernameInput = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.cssSelector("groupui-input[id='welcome-user-name']")
        ));
        usernameInput.sendKeys(username);
    
        // 等待 Password 输入框可见
        WebElement passwordInput = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.cssSelector("groupui-input[id='welcome-api-key']")
        ));
        passwordInput.sendKeys(password);
    }



    @When("I click the login button")
    public void i_click_the_login_button() {
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("welcome-login")));
        loginButton.click();
    }

    @Then("I should see the terms and conditions popup")
    public void i_should_see_the_terms_and_conditions_popup() {
        WebElement popup = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.xpath("//groupui-headline[contains(text(),'Terms & Conditions')]")
        ));
        assertTrue(popup.isDisplayed(), "Terms and conditions popup should be displayed.");
    }

    @When("I accept the terms and conditions")
    public void i_accept_the_terms_and_conditions() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        
        // 定位 Terms & Conditions 弹窗
        WebElement modal = driver.findElement(By.xpath("//groupui-modal[@ng-reflect-displayed='true']"));
    
        // 滚动到 Terms & Conditions 弹窗底部
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollTop = arguments[0].scrollHeight;", modal);
    
        // 等待 "I Agree" 按钮可点击
        WebElement acceptButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("welcome-agree-agb")));
    
        // 强制点击 "I Agree" 按钮
        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", acceptButton);
    }
    

@Then("I should be logged in and see my profile avatar and ID")
public void i_should_be_logged_in_and_see_my_profile_avatar_and_id() {
    // 等待 profile 头像和 ID 显示
    WebElement profileContainer = wait.until(
        ExpectedConditions.visibilityOfElementLocated(By.id("app-profile-header"))
    );

    // 查找 profile 头像
    WebElement profileAvatar = profileContainer.findElement(By.tagName("groupui-avatar"));
    assertNotNull(profileAvatar, "Profile avatar is not visible, login might have failed.");

    // 查找 profile ID（文本内容）
    String profileId = profileContainer.getText().trim();
    assertFalse(profileId.isEmpty(), "Profile ID is missing, login might have failed.");

    // 记录日志（可选）
    System.out.println("Login successful. Profile ID: " + profileId);
}

@When("I click the profile avatar")
public void i_click_the_profile_avatar() {
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

    // 先检查是否有 Toast 通知，等待它消失
    try {
        WebElement toastMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".toast-title")));
        wait.until(ExpectedConditions.invisibilityOf(toastMessage));
        System.out.println("Toast message disappeared.");
    } catch (TimeoutException e) {
        System.out.println("No blocking toast message found.");
    }

    // 等待头像可见
    WebElement profileContainer = wait.until(
        ExpectedConditions.visibilityOfElementLocated(By.id("app-profile-header"))
    );

    // 查找并点击头像
    WebElement profileAvatar = profileContainer.findElement(By.tagName("groupui-avatar"));
    if (profileAvatar == null) {
        throw new RuntimeException("Profile avatar not found. Cannot proceed to logout.");
    }
    profileAvatar.click();
}




@When("I click the logout button")
public void i_click_the_logout_button() {
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

    // 等待 Logout 按钮可见并点击
    WebElement logoutButton = wait.until(
        ExpectedConditions.elementToBeClickable(By.id("app-logout"))
    );

    if (logoutButton == null) {
        throw new RuntimeException("Logout button not found.");
    }

    logoutButton.click();
}


@Then("I should be on the login page")
public void i_should_be_on_the_login_page() {
    try {
        // 等待并检查用户名输入框是否仍然可见
        WebElement usernameInput = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.cssSelector("groupui-input[id='welcome-user-name']")
        ));
        assertTrue(usernameInput.isDisplayed(), "Username input field should be visible if login failed.");

        // 等待并检查密码输入框是否仍然可见
        WebElement passwordInput = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.cssSelector("groupui-input[id='welcome-api-key']")
        ));
        assertTrue(passwordInput.isDisplayed(), "Password input field should be visible if login failed.");

        // 等待并检查登录按钮是否仍然可见
        WebElement loginButton = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.id("welcome-login")
        ));
        assertTrue(loginButton.isDisplayed(), "Login button should be visible if login failed.");

        System.out.println("✅ Login failed as expected: Login page elements are still visible.");
    } catch (TimeoutException e) {
        fail("❌ Login page elements not found, login might have succeeded unexpectedly.");
    }
}




}
    """
    steps_path = "src/test/java/huiyu/stepdefinitions_login_test/LoginTest_test.java"
    with open(steps_path, "w", encoding="utf-8") as f:
        f.write(steps_code)
    return steps_path
