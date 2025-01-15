package huiyu;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.json.JSONObject;

public class LighthouseUtil2 {

    // 执行 Lighthouse 测试并生成报告
    public static void lighthouseReport(String URL, String reportName, String customPort) throws IOException {
        ProcessBuilder builder = new ProcessBuilder("cmd.exe", "/c", "lighthouse", URL,
                "--port=" + customPort, "--preset=desktop", "--output=json",
                "--output-path=target/" + reportName + ".json");
        builder.redirectErrorStream(true);
        Process process = builder.start();
        
        // 读取 Lighthouse 执行过程中的输出
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        }
    }

    // 从生成的 Lighthouse JSON 报告中解析可访问性得分
    public static double getAccessibilityScore(String reportName) throws IOException {
        String path = "target/" + reportName + ".json";
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            StringBuilder jsonContent = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                jsonContent.append(line);
            }
            JSONObject jsonObject = new JSONObject(jsonContent.toString());
            return jsonObject.getJSONObject("categories").getJSONObject("accessibility").getDouble("score") * 100;
        }
    }
}
