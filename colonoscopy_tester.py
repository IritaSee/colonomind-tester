"""
Selenium-based automation script for testing ColonoMind webapp.
"""
import time
import logging
from pathlib import Path
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class ColonoMindTester:
    """Automated tester for ColonoMind webapp using Selenium."""
    
    def __init__(self, webapp_url: str, headless: bool = False):
        """
        Initialize the tester.
        
        Args:
            webapp_url: URL of the ColonoMind webapp
            headless: Run browser in headless mode
        """
        self.webapp_url = webapp_url
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Set up Selenium WebDriver."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Automatically download and use the correct ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        
        logger.info("WebDriver initialized successfully")
        
    def navigate_to_webapp(self):
        """Navigate to the ColonoMind webapp."""
        logger.info(f"Navigating to {self.webapp_url}")
        self.driver.get(self.webapp_url)
        
        # Wait for Streamlit to load
        time.sleep(3)
        
    def upload_image(self, image_path: str, upload_timeout: int = 15) -> bool:
        """
        Upload an image to the webapp and start analysis.
        
        Args:
            image_path: Absolute path to the image file
            upload_timeout: Timeout for upload in seconds
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            logger.info(f"Uploading image: {Path(image_path).name}")
            
            # Find the file input element (Streamlit uses standard file input)
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            
            if not file_inputs:
                logger.error("No file input found on page")
                return False
            
            # Use the first file input
            file_input = file_inputs[0]
            
            # Send the file path to the input
            file_input.send_keys(image_path)
            
            logger.info("Image file sent to upload input")
            
            # Wait for the "Start Analysis" button to appear and be clickable
            # Based on screenshot, it's a purple button with "Start Analysis" text
            try:
                start_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start Analysis')]"))
                )
                logger.info("Found 'Start Analysis' button, clicking...")
                start_button.click()
                return True
            except TimeoutException:
                logger.warning("Could not find 'Start Analysis' button - maybe auto-started or upload failed?")
                # Check if maybe it auto-started or if we are already seeing results
                return True
            
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return False
    
    def wait_for_processing(self, timeout: int = 60) -> bool:
        """
        Wait for the classification to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if processing completed, False if timeout
        """
        try:
            logger.info("Waiting for classification to complete...")
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    # Check for the result card header "ColonoScan MES Score"
                    result_header = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'ColonoScan MES Score')]")
                    if result_header:
                        logger.info("Processing completed (Result card found)")
                        return True
                        
                    # Check for "Analysis Results" header
                    analysis_header = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Analysis Results')]")
                    if analysis_header:
                        logger.info("Processing completed (Analysis Results header found)")
                        return True

                    # Check sidebar prediction "Prediction: MES"
                    sidebar_pred = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Prediction: MES')]")
                    if sidebar_pred:
                        logger.info("Processing completed (Sidebar prediction found)")
                        return True
                        
                except Exception:
                    pass
                
                time.sleep(1)  # Check every 1 second
            
            logger.warning(f"Processing timeout after {timeout} seconds")
            return False
            
        except Exception as e:
            logger.error(f"Error waiting for processing: {e}")
            return False
    
    def extract_mes_classification(self) -> Optional[int]:
        """
        Extract the MES classification result from the page.
        
        Returns:
            MES classification (1-4) or None if not found
        """
        try:
            logger.info("Extracting MES classification...")
            
            # Strategy 1: Look for the main result card "ColonoScan MES Score: X"
            # The screenshot shows "ColonoScan MES Score: 3" in a red card
            try:
                # Find element containing the text
                score_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'ColonoScan MES Score:')]")
                for element in score_elements:
                    text = element.text.strip()
                    # Extract the number
                    import re
                    match = re.search(r'Score:\s*([0-3])', text)
                    if match:
                        score = int(match.group(1))
                        logger.info(f"Found MES score in result card: {score}")
                        return score
            except Exception as e:
                logger.debug(f"Strategy 1 failed: {e}")

            # Strategy 2: Look for Sidebar "Prediction: MES X"
            try:
                sidebar_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Prediction: MES')]")
                for element in sidebar_elements:
                    text = element.text.strip()
                    # Text likely "Prediction: MES 3"
                    match = re.search(r'MES\s*([0-3])', text)
                    if match:
                        score = int(match.group(1))
                        logger.info(f"Found MES score in sidebar: {score}")
                        return score
            except NoSuchElementException:
            # Strategy 2: Get all text content and search for MES pattern
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            mes_patterns = [
                r'ColonoScan MES Score:\s*([0-3])',
                r'Prediction: MES\s*([0-3])',
                r'MES Score:\s*([0-3])',
                r'MES[:\s]*([0-3])',
                r'Score[:\s]*([0-3])',
            ]
            
            for pattern in mes_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    mes_value = int(match.group(1))
                    logger.info(f"Extracted MES classification via regex: {mes_value}")
                    return mes_value
            
            logger.warning("Could not extract MES classification from page")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting MES classification: {e}")
            return None
    
    def reset_for_next_image(self):
        """Reset the webapp state for the next image."""
        try:
            logger.info("Resetting webapp for next image...")
            
            # Try to click "Analyze New Image" button in sidebar if it exists
            try:
                new_image_btn = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze New Image')]")
                if new_image_btn and new_image_btn[0].is_displayed():
                    logger.info("Clicking 'Analyze New Image' button")
                    new_image_btn[0].click()
                    time.sleep(2)
                    return
            except Exception:
                pass
            
            # Fallback: Reload the page
            self.driver.get(self.webapp_url)
            time.sleep(3)  # Wait for page to load
            
        except Exception as e:
            logger.error(f"Error resetting webapp: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
