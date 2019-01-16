from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    listings = {}#Dictionary to store all the reqired informations. 
    
    
    #Automating browser to collect the latest News Title and Paragraph Text.
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["latest_title"]= soup.find('div',class_='content_title').get_text()
    listings["description"]= soup.find('div',class_="article_teaser_body").text
    browser.quit()
    
    
    #Automating browser to find the image url for the current Featured Mars Image.
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["featured_image_url"]="https://www.jpl.nasa.gov"+soup.find('div', class_="carousel_items").a['data-fancybox-href']
    browser.quit()
    
    
    #Automating browser to collect the latest Mars weather.
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["mars_weather"]=soup.find('div',class_="ProfileTimeline").p.text
    browser.quit()
    
    #Using Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    import pandas as pd
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description','Value']
    df.set_index('Description' ,inplace=True)
    listings["html_table"] = df.to_html()
    browser.quit()
    
    
    
    #Automating browser to obtain high resolution images for each of Mar's hemispheres.
    browser = init_browser()
    url="http://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results=soup.find_all('div',class_='img-caption-box')
    title=[] # List to collect the names of the Mar's hemispheres
    img_url=[] #List to collect the img urls of each of the Mar's hemispheres
    for i in results:
        title.append(i.h5.text)
    

    hemisphere_image_urls=[]
    for i in range(4):
        soup = BeautifulSoup(html, 'lxml')
        url=soup.find_all('img',class_='img840')[i]
        img_url.append(""+url['src'])
        hemisphere_image_urls.append({
        'img_url':img_url[i],
        'title':title[i],
            })
        
        
    listings["hemisphere_image_urls"]= hemisphere_image_urls
    browser.quit()
    return listings

scrape()