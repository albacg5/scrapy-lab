import scrapy
import unidecode
import re
import logging

cleanString = lambda x: '' if x is None else unidecode.unidecode(re.sub(r'\s+',' ',x))


class ElpaisSpider(scrapy.Spider):
    name = 'elpais'
    allowed_domains = ['www.elpais.com']
    start_urls = ['https://elpais.com/']

    def parse(self, response):

        # We get all of the sections of El Pais newspaper
        sect = response.css("section")


        for s in sect:
            section_name = 'No section name'

            # Checking at the html, we found that the name of the section is stored
            # in the data-dtm-region attribute, but since this could be empty, we 
            # previously store 'No section name' as its name.
            if 'data-dtm-region' in s.attrib:
                section_name = s.attrib['data-dtm-region']
            
            # We get information for every article inside the section
            for article in s.css("article"):
                    title = article.css("a::text").extract_first()
                    url = response.url[:-1] + article.css("a::attr(href)").extract_first()
                    summary =  article.css("p::text").extract_first()
                    
                    # There's a chance that the url stored previously is from a different domain
                    # that is not El Pais, and the previous call wouldn't be as useful as it is 
                    # supposing that the article is in the same domain. If it is in another domain,
                    # article.css("a::attr(href)").extract_first() will contain another https url,
                    # so we do the next check:
                    if url.count('https') >= 2:
                        url = article.css("a::attr(href)").extract_first()
                    
                    if summary == None: summary = "No summary"
                
                    yield {
                    'section': section_name,
                    'appears_ulr': response.url,
                    'title': cleanString(title),
                    'article_url': url,
                    'summary': cleanString(summary),
                    }        
