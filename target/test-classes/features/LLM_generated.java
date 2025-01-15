
    Generate Java step definitions for this Gherkin feature:

    Feature: Login to the TaaS Serviceportal

  Scenario: Successful login to the TaaS Serviceportal
    Given I open the login page
    When I enter username "vw2xn87" and password "xOqMiHJegL3JvnOCK9rb0vOG1pZ7Oc1C7fAfRR0WEuk4keuwEc0yAUF3QSahP8G3IBKw2FO2zvcr7njD"
    And I click the login button
    Then I should see the terms and conditions popup
    When I accept the terms and conditions
    Then I should be logged in and see my profile avatar and ID

  Scenario: Login with incorrect password
    Given I open the login page
    When I enter username "vw2xn87" and password "1234"
    And I click the login button
    When I accept the terms and conditions
    Then I should be on the login page

  Scenario: Logout after successful login
    Given I open the login page
    When I enter username "vw2xn87" and password "xOqMiHJegL3JvnOCK9rb0vOG1pZ7Oc1C7fAfRR0WEuk4keuwEc0yAUF3QSahP8G3IBKw2FO2zvcr7njD"
    And I click the login button
    Then I should see the terms and conditions popup
    When I accept the terms and conditions
    Then I should be logged in and see my profile avatar and ID
    When I click the profile avatar
    And I click the logout button
    Then I should be on the login page
    Provide the Java `step definitions` class in the following format:
    - Each Gherkin step should have a corresponding Java method with annotations.
    - Implement Selenium code where necessary, and use assertions to validate expected outcomes.
    - Provide comments for each method to clarify purpose and actions.

    Format:
    // Java step definitions
    public class WebPageSteps {
        // Define step methods here
    }
    Example:

    // Java step definitions for Web Page Title Verification
    public class WebPageTitleSteps {
        
        WebDriver driver = new ChromeDriver();

        @Given("I open the test URL in the browser")
        public void openTestURL() {
            driver.get("https://example.com"); // Replace with actual URL
        }

        @When("the page loads completely")
        public void pageLoadsCompletely() {
            // Wait for page to fully load
        }

        @Then("I should see the expected page title {string}")
        public void verifyPageTitle(String expectedTitle) {
            String actualTitle = driver.getTitle();
            assertEquals(expectedTitle, actualTitle);
        }
    }
    ### Start Output
    Output begins below:
    
    yutakatsu2468/mugen-3.0/src/js/game/MugenGame.js
/**
 * This class is a wrapper for the game state.
 *
 * @class
 * @extends Phaser.Game
 * @memberof mugen
 *
 * @param {string} gameID - The ID of the game
 * @param {mugen.MugenConfig} config - The configuration for the game
 */
mugen.MugenGame = class extends Phaser.Game {

    constructor(gameID, config) {

        let gameWidth = config.gameWidth;
        let gameHeight = config.gameHeight;
        let parent = config.parent;

        config.gameWidth = gameWidth * mugen.screenScale;
        config.gameHeight = gameHeight * mugen.screenScale;

        config.parent = parent;

        // Set the stage scale mode
        config.scale.scaleMode = Phaser.ScaleManager.USER_SCALE;
        config.scale.setScreenSize();

        super(config);

        this.gameID = gameID;

        // The config for the game
        this.config = config;

        // The game state
        this.gameState = new mugen.GameState(this);
        this.state.add('GameState', this.gameState);
        this.state.start('GameState');
    }
}
/src/js/game/states/GameState.js
/**
 * The game state class.
 *
 * @class
 * @memberof mugen
 *
 * @param {mugen.MugenGame} game - The game
 */
mugen.GameState = class extends Phaser.State {

    constructor(game) {
        super();

        this.game = game;
        this.gameID = game.gameID