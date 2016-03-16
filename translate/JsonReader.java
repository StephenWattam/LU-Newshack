
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class JsonReader {

	private static final String filePath = "/Users/mahmoudel-haj/Downloads/out.short.json";

	//
	public static void main(String[] args) {

		try {
			// read the json file
			FileReader reader = new FileReader(filePath);

			String text = new String(Files.readAllBytes(Paths.get(filePath)), StandardCharsets.UTF_8);
			jsonToMap(text.trim());
			System.exit(0);
		} catch (Exception e) {
			System.err.println(e);
		}
	}

	public static void jsonToMap(String t) throws JSONException, IOException {

		System.setProperty("webdriver.chrome.driver", "/Users/mahmoudel-haj/Downloads/chromedriver");
		WebDriver driver = new ChromeDriver();
		driver.get("https://translate.google.com/");

		HashMap<Object, Object> map = new HashMap<Object, Object>();
		JSONObject jObject = new JSONObject(t);
		Iterator<?> keys = jObject.keys();

		while (keys.hasNext()) {
			Object key = keys.next();
			if(!key.toString().contains("en")){
				
			try {
				JSONObject value = jObject.getJSONObject((String) key);
				System.out.println("Language: " + key);

				Iterator<String> categories = value.keys();
				while (keys.hasNext()) {
					Object category = categories.next();
					JSONObject value2 = value.getJSONObject((String) category);

					// System.out.println("Category: " + category);

					Iterator<String> stubs = value2.keys();
					while (stubs.hasNext()) {
						String stub = stubs.next();
						JSONObject article = value2.getJSONObject(stub);

						// System.out.println("Article ID: " + article);
						article.put("tagged", "yes");
						String title = "";
						String summary = "";

						org.json.JSONArray groups = new org.json.JSONArray();

						try {
							title = (String) article.get("title");
							String title_translate_text = GoogleTranslate.translateGoogle(title, driver);
							article.put("title", title_translate_text);
							title = (String) article.get("title");
							System.out.println("=======> " + title);

							
						} catch (Exception e) {
						}
						try {
							summary = (String) article.getString("summary");
							
							String summary_translate_text = GoogleTranslate.translateGoogle(summary, driver);
							article.put("summary", summary_translate_text);
							summary = (String) article.get("summary");
							System.out.println("=======> " + summary);
							
						} catch (Exception e) {
						}

						try {
							JSONObject media = article.getJSONObject("media");
							JSONObject images = media.getJSONObject("images");

							Iterator<String> key2 = images.keys();
							while (key2.hasNext()) {
								String imgLabel = key2.next();

								JSONObject imageList = null;
								try {
									imageList = images.getJSONObject(imgLabel);
								} catch (Exception e) {
								}

								Iterator<String> key3 = imageList.keys();

								while (key3.hasNext()) {
									String imageID = key3.next();
									JSONObject image = imageList.getJSONObject(imageID);

									String altText = "";
									try {
										altText = (String) image.get("altText");
										System.out.println("_______> " + altText);
										String alt_translate_text = GoogleTranslate.translateGoogle(altText, driver);

										image.put("altText", alt_translate_text);
										altText = (String) image.get("altText");
										System.out.println("=======> " + altText);

										

										System.out.println(altText);
									} catch (Exception e) {
									}

								}
							}
						} catch (Exception e) {
						}

						FileWriter file = new FileWriter("/Users/mahmoudel-haj/Downloads/steve.json");
						jObject.write(file);
						file.flush();
						file.close();
						
					}

				}

				System.out.println(key.toString());

			} catch (Exception e) {
			}
			

			
		}
		}//language loop

	}

}
