import scrapy 
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.linkextractors import LinkExtractor
from scrape_pdf.items import ScrapePdfItem
import re 

class PdfUrl_Spider(CrawlSpider):

    name = 'scrape_pdf'
    allowed_domains = ['uvic.ca']

    start_urls = ['https://www.uvic.ca']

    rules = [Rule(LinkExtractor(allow=''), callback='scraping_pdf', follow=True)]

    def scraping_pdf(self, response):

        if response.status != 200:
            return None 
        

        item = ScrapePdfItem()
        
        #Checking if the Content-Type exists in the responseheader
        if b'Content-Type' in response.headers.keys():
            link_to_pdf = 'text/html' in str(response.headers['Content-Type'])
        else:
            return None 

        Content_Disposition = b'Content-Disposition' in response.headers.keys()

        #Checking if the url sends us to a pdf link
        if link_to_pdf:
            #print(re.search('filename="(.+)"', str(response.headers['Content-Disposition'])).group(1))
            print(response.url, "\n")

            if Content_Disposition:
                #File name is available at Content-Disposition: attachment; filename="cool.html"
                item['pdf_name'] = re.search('filename="(.+)"', str(response.headers['Content-Disposition'])).group(1)
                item['pdf_url'] = response.url
            else:
                #The pdf name is the last field of the url after ( / ) 
                item['pdf_name'] = response.url.split('/')[-1]
                item['pdf_url'] = response.url   
        else:
            return None 

        return item 
