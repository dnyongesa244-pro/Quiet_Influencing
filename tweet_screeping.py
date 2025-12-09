from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime
    
def scrape_twitter_hashtag(hashtag, max_tweets=50):
    """
    Scrape Twitter hashtag page (requires login)
    Note: Twitter may block automated access
    """
    driver = webdriver.Chrome()  # Or use webdriver.Firefox()
    
    try:
        # Login to Twitter (you need to handle this)
        driver.get("https://twitter.com/login")
        time.sleep(10)  # Manual login time
        
        # Navigate to hashtag
        driver.get(f"https://twitter.com/hashtag/{hashtag}")
        time.sleep(3)
        
        tweets_data = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while len(tweets_data) < max_tweets:
            # Find tweet elements
            tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            
            for tweet in tweet_elements:
                try:
                    text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                    username = tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span').text
                    
                    tweets_data.append({
                        'platform': 'Twitter',
                        'username': username,
                        'text': text,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    if len(tweets_data) >= max_tweets:
                        break
                        
                except:
                    continue
            
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Check if we're at the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    finally:
        driver.quit()
    
    return pd.DataFrame(tweets_data)