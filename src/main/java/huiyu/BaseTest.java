package huiyu;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class BaseTest {
    protected WebDriver driver;
    protected static final List<Double> accessibilityScores = new ArrayList<>();

    @BeforeEach
    public void setUp() {
        // 初始化 WebDriver
        // System.setProperty("webdriver.chrome.driver", Config.DRIVER_PATH);
        WebDriverManager.chromedriver().setup();
        
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--remote-allow-origins=*");
        // options.addArguments("--remote-debugging-port=" + Config.LIGHTHOUSE_PORT); // 确保以调试端口打开.注释掉这一行就可以正常开启新的web page
        driver = new ChromeDriver(options);
        System.out.println("ChromeDriver initialized and Chrome launched."); // 添加调试信息
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            System.out.println("Closing WebDriver...");
            driver.quit();
            driver = null;
            System.out.println("WebDriver closed successfully.");
        }
    }

    @AfterAll
    public static void runLighthouse() {
        try {
            // 执行 Lighthouse 分析并记录可访问性得分
            LighthouseUtil2.lighthouseReport(Config.TEST_URL, Config.LIGHTHOUSE_REPORT_NAME, Config.LIGHTHOUSE_PORT);
            accessibilityScores.add(LighthouseUtil2.getAccessibilityScore(Config.LIGHTHOUSE_REPORT_NAME));

            // 计算并输出平均可访问性得分
            double averageScore = accessibilityScores.stream().mapToDouble(Double::doubleValue).average().orElse(0);
            System.out.println("Average Accessibility Score: " + averageScore);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
}

