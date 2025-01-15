from langchain_integration.vector_database import VectorDatabase

def prepare_database():
    vector_db = VectorDatabase()


    example_texts = [
        """
        Feature: Web Page Title and Accessibility Test
          Scenario: Validate webpage title and accessibility score
            Given I navigate to the test URL
            Then I should see the correct page title
        """,
        """
        Feature: User Login Test
          Scenario: User logs in with valid credentials
            Given the user is on the login page
            When the user enters valid username and password
            And clicks on the login button
            Then the user should be redirected to the homepage
        """,
        """
        Feature: Job List Display Test
          Scenario: Job list is visible on the job page
            Given the user is on the job list page
            When the page loads
            Then a list of available jobs should be displayed
        """
    ]

    vector_db.add_texts(example_texts)

    return vector_db

if __name__ == "__main__":
    db = prepare_database()
    print("Vector database initialized with example texts.")
