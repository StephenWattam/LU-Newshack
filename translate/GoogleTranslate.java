package translate;


import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class GoogleTranslate {

    	private static String toTranslate = "";

    	public static PrintWriter writer;

    public static void main(String args[]) throws InterruptedException, FileNotFoundException{

    	toTranslate = "Hello World";
			    List<WebElement> elements = translateGoogle(toTranslate);
			
    }	 
	
	
	
	public static  List<WebElement> translateGoogle(String query) throws InterruptedException {
		List<WebElement> findElements = null;
		try{
		  // Optional, if not specified, WebDriver will search your path for chromedriver.
		System.setProperty("webdriver.chrome.driver", "/Users/mahmoudel-haj/Downloads/chromedriver");
		
		// Use a browser profile to avoid being detected by google.
		//ProfilesIni allProfiles = new ProfilesIni();
		//WebDriver driver = new ChromeDriver(allProfiles.getProfile("default"));
		WebDriver driver = new ChromeDriver();
	   // WebDriver driver = new FirefoxDriver();
		// WebDriver driver = new ChromeDriver();
		driver.get("https://translate.google.com/");
	       
	    WebElement element = driver.findElement(By.name("text"));
	   JavascriptExecutor executor = (JavascriptExecutor)driver;
	    
	    element.sendKeys(query); // send also a "\n"
	    

		   driver.findElement(By.xpath("//*[@value='ar']")).click();
		    
		    element.submit();

	    String output = driver.findElement(By.id("result_box")).getText();
	    //System.out.println(output);
	    System.out.println(output);
	   // driver.close();
}
catch(Exception e){System.err.println("Error caught " + e);}
	    
		return findElements;
	}
	
}
