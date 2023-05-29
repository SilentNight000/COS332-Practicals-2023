import java.io.*;
import java.net.*;
import java.awt.Desktop;

public class Client {
    public static void main(String[] args) throws Exception {
        String stringurl = "http://127.0.0.1:55555"; // Change this to the server URL
        URL obj = new URL(stringurl);
        HttpURLConnection conn = (HttpURLConnection) obj.openConnection();
        conn.setRequestMethod("GET");

        int response = conn.getResponseCode();
        System.out.println("GET: " + stringurl);
        System.out.println("RESPONSE: " + response);

        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String inputLine;
        StringBuffer result = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            result.append(inputLine);
        }
        in.close();

        // Open the webpage in the default browser
        URL url = new URL(stringurl);
        Desktop.getDesktop().browse(url.toURI());
    }
}