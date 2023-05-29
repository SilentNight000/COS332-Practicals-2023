import java.util.*;
import java.io.*;
import java.net.*;
import java.text.*;
import com.sun.net.httpserver.*;

public class Server {
    private static final int PORT = 55555;
    private static final String LOCAL_TIMEZONE = "Africa/Johannesburg";

    // Define a map of city names and their timezones
    private static final Map<String, String> CITIES = new HashMap<>();
    static {
        CITIES.put("New York", "America/New_York");
        CITIES.put("London", "Europe/London");
        CITIES.put("Paris", "Europe/Paris");
        CITIES.put("Tokyo", "Asia/Tokyo");
    }

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        server.createContext("/", new WorldClockHandler());
        server.setExecutor(null);
        server.start();
        System.out.println("Server running on port " + PORT);
    }

    static class WorldClockHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // Extract the request path from the exchange
            String requestPath = exchange.getRequestURI().getPath();
            String response = "";

            // If the request is for the root path, show the main clock page
            if ("/".equals(requestPath)) {
                response = getClockPage(LOCAL_TIMEZONE);
            }
            // If the request is for a city path, show the corresponding clock page
            else if (CITIES.containsKey(requestPath.substring(1))) {
                String city = requestPath.substring(1);
                String timezone = CITIES.get(city);
                response = getClockPage(timezone);
            }

            // Set the response headers
            exchange.getResponseHeaders().set("Content-Type", "text/html");
            exchange.getResponseHeaders().set("Cache-Control", "no-cache");

            // Send the response content
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }

        // Returns an HTML page showing the clock for a given timezone
        private String getClockPage(String timezone) {
            String localTime = new Date().toString();
            String cityTime = getCityTime(timezone);
            StringBuilder sb = new StringBuilder();
            sb.append("<html><head><meta http-equiv=\"refresh\" content=\"1\"></head>");
            sb.append("<body>");
            sb.append("<h1>World Clock</h1>");
            sb.append("<p>Local Time: ").append(localTime).append("</p>");
            sb.append("<p>").append(timezone).append(" Time: ").append(cityTime).append("</p>");
            sb.append("<ul>");
            for (String city : CITIES.keySet()) {
                sb.append("<li><a href=\"").append(city).append("\">").append(city).append("</a></li>");
            }
            sb.append("</ul>");
            sb.append("</body></html>");
            return sb.toString();
        }

        // Returns the current time in a given timezone
        /*private Date getCityTime(String timezone) {
            Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone(timezone));
            return calendar.getTime();
        }*/
        // Returns the current time in a given timezone as a string
    private String getCityTime(String timezone) {
    Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone(timezone));
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    formatter.setTimeZone(calendar.getTimeZone());
    return formatter.format(calendar.getTime());
}

    }
}