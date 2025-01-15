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
    private static Process xvfbProcess; // 用于管理 Xvfb 进程

    @BeforeEach
    public void setUp() {
        try {
            // 启动 Xvfb
            if (xvfbProcess == null) {
                System.out.println("Starting Xvfb...");
                xvfbProcess = Runtime.getRuntime().exec("Xvfb :99 -screen 0 1920x1080x24");
                Thread.sleep(2000); // 等待 Xvfb 启动
            }

            System.setProperty("DISPLAY", ":99");

            // 初始化 ChromeDriver
            WebDriverManager.chromedriver().setup();
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--remote-allow-origins=*");
            options.addArguments("--no-sandbox"); // 适用于 Docker
            options.addArguments("--disable-dev-shm-usage"); // 解决某些环境下共享内存不足的问题
            options.addArguments("--headless"); // 以无界面模式运行

            driver = new ChromeDriver(options);
            System.out.println("ChromeDriver initialized and Chrome launched.");
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to start Xvfb or ChromeDriver", e);
        }
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
    public static void cleanup() {
        if (xvfbProcess != null) {
            System.out.println("Stopping Xvfb...");
            xvfbProcess.destroy();
            xvfbProcess = null;
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
