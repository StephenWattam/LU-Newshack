

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
//import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.internal.ProfilesIni;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class test {
    	private static String docName = "", par = "", lang = "", toTranslate = "";
    	private static int sentID = 0, counter = 0, counter2 = 0;
    	public static PrintWriter writer;

    	
    public static void main(String args[]) throws InterruptedException, FileNotFoundException{

   		 System.setProperty("webdriver.chrome.driver", "/Users/mahmoudel-haj/Downloads/chromedriver");

    		writer = new PrintWriter("/Users/mahmoudel-haj/Documents/workspace/GoogleTranslate");

		while(1==1){
			
		counter++;
			sentID= 1;
			lang = "ar";
			par = new String("Hello World");
			//System.out.println(par);
			toTranslate += "[[[[" + sentID + "####" + lang + "%%%%" + par + "]]]] ";  
    	
			if(counter==40){
				System.out.println((++counter2) + "batch= " + counter);
			    List<WebElement> elements = translateGoogle(toTranslate);
				System.out.println(toTranslate);
			    toTranslate = "";
			    counter = 0;
			}
		}
	    
	
    }	 
	
	
	
	public static  List<WebElement> translateGoogle(String query) throws InterruptedException {
		List<WebElement> findElements = null;
		try{
		  // Optional, if not specified, WebDriver will search your path for chromedriver.
		
		// Use a browser profile to avoid being detected by google.
		//ProfilesIni allProfiles = new ProfilesIni();
		//WebDriver driver = new ChromeDriver(allProfiles.getProfile("default"));
		WebDriver driver = new ChromeDriver();
	    //WebDriver driver = new FirefoxDriver();
		// WebDriver driver = new ChromeDriver();
		driver.get("https://translate.google.com/");
	       
	    WebElement element = driver.findElement(By.name("text"));
	   // driver.findElement(By.id("ar"));
	   JavascriptExecutor executor = (JavascriptExecutor)driver;
	   // driver.findElement(By.xpath("//*[@value='ar']")).click();
	    
	   // driver.findElement(By.cssSelector("input[type='button'][value='Open device access']")).click();

	   // executor.executeScript("arguments[1].click();", element);

	    
	    element.sendKeys(query); // send also a "\n"
	    
	    element.submit();

	    String output = driver.findElement(By.id("result_box")).getText();
	    System.out.println(output);
	    writer.println(output);
	    writer.flush();
	    Thread.sleep(200);
	    driver.close();
}
catch(Exception e){System.err.println("Error caught - Continue...");}
	    
		return findElements;
	}
	
}
