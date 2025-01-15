package huiyu.stepdefinitions;

import static org.junit.jupiter.api.Assertions.assertEquals;

import huiyu.BaseTest;
import huiyu.Config;
import io.cucumber.java.AfterAll;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;

public class WebPageSteps extends BaseTest {
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

