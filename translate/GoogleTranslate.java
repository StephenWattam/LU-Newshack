

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class GoogleTranslate {


	private static String toTranslate = "";
	public static PrintWriter writer;
	public static void main(String args[]) throws InterruptedException, IOException, URISyntaxException {

		System.setProperty("webdriver.chrome.driver", "/Users/mahmoudel-haj/Downloads/chromedriver");
		WebDriver driver = new ChromeDriver();
		driver.get("https://translate.google.com/");

		   File dir = new File("/Users/mahmoudel-haj/Documents/TranslateFiles");       
		   if(dir.isDirectory()){
		   	  for (File child : dir.listFiles()) {
		   	  System.out.println(child);
		    	 String text = new String(Files.readAllBytes(Paths.get(""+child)), StandardCharsets.UTF_8);
				   System.out.println(text);
				   toTranslate = text;
				   System.out.println(translateGoogle(toTranslate, driver));
		   	  }

		   }
		   
		  
			//List<WebElement> elements = translateGoogle(toTranslate);
			
	}

	public static String translateGoogle(String query, WebDriver driver) throws InterruptedException {
String translation = "";

try {



			WebElement element = driver.findElement(By.name("text"));
			JavascriptExecutor executor = (JavascriptExecutor) driver;

			element.sendKeys(query); // send also a "\n"

			driver.findElement(By.xpath("//*[@value='en']")).click();
			

			element.submit();
			Thread.sleep(200);
			translation = driver.findElement(By.id("result_box")).getText();
			System.out.println("--> " + translation);
			Thread.sleep(200);
		    
		} catch (Exception e) {
			System.err.println("Error caught " + e);
		}

		return translation;
	}

}
