package huiyu.stepdefinitions_login;

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

public class LoginTest extends BaseTest {

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
