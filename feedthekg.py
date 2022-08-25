#!/usr/bin/env python -tt
# coding: utf-8


# Importing the Libraries
import sqlite3
from myapp.models import *
from neomodel import db
import re
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
from twisted.internet import reactor
import os
import pandas as pd
from itertools import chain



class EuroncapSpider(scrapy.Spider):

    def __init__(self, url, **kwargs):

        self.start_urls = [f'{url}']
        super().__init__(**kwargs)

    
    # Spider name
    name = "Euroncap"

    # Extracting from local file
    # start_urls = ["file:///home/ganesh/scrapy_learning/leaf_node_html.html"]

    # Extracting from website
    # start_urls = ["https://www.euroncap.com/en/results/toyota/yaris-cross/43819"]

    # start_urls = ["file:///home/ganesh/myproject/leaf_node_html_test.html"]


    def clean_url(self, url, response):

        # Cleaning the urls as proper links
        clean_image_urls = []
        for img_url in url:
            clean_image_urls.append(response.urljoin(img_url))
  
        return clean_image_urls
    

    # Parse functon to extract the features needed
    def parse(self, response):

        
        # Extracting images from desired location
        # having data and data-src as per the outline of the page

        # Extracting the Test image
        crash_image_urls_data = response.xpath('//*[@class="reward-images"]//img/@data-src').getall()
        crash_image_urls = crash_image_urls_data + response.xpath('//*[@class="reward-images"]//img/@src').getall()

        # # Extracting the adult occupant image
        # adult_occupant_image_urls_data = response.xpath('//*[@class="frame-content"]//img/@data-src').getall()
        # adult_occupant_image_urls = adult_occupant_image_urls_data + response.xpath('//*[@class="frame-content"]//img/@src').getall()

        # # Extracting the pedestrian image
        # pedestrian_image_urls_data = response.xpath('//*[@class="pedestrian-protection"]//img/@data-src').getall()
        # pedestrian_image_urls = pedestrian_image_urls_data + response.xpath('//*[@class="pedestrian-protection"]//img/@src').getall()

        # # Extracting the safety image
        # brakesafety_image_urls_data = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@data-src').getall()
        # brakesafety_image_urls = brakesafety_image_urls_data + response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@src').getall()
        
        # safety_image_urls_data = response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@data-src').getall()
        # safety_image_urls = safety_image_urls_data + response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@src').getall() 


        # Adult occupant tab
        adult_occupant_total = response.xpath('//*[@id="tab2-1"]/div/text()').getall()[0].strip()
        adult_occupant = []

        try:
            adult_occupant_value = response.xpath('//*[@class="frame-points no-frame-info"]/text()').getall()
            adult_occupant_value = [val.strip() for val in adult_occupant_value][:3] + \
                                   [response.xpath('//*[@class="accordion-item-header accordion-item-header-frame"]/ \
                                                               span/text()').getall()[0].strip()]

            adult_occupant_impact = response.xpath('//*[@class="frame-title"]/text()').getall()[:3] + \
                                    [response.xpath('//*[@class="accordion-item-header accordion-item-header-frame"]/ \
                                                                    text()').getall()[0].strip()]

            scrap_container = [['//*[@class="frame w-1-1 frontal-block"]//img/@data-src', 
                                '//*[@class="frame w-1-1 frontal-block"]//span/text()'],
                               ['//*[@class="frame w-1-1"]//img/@data-src',
                                '//*[@class="frame w-1-1"]//span/text()'],
                               ['//*[@class="frame w-1-1 whiplash-block"]//img/@data-src',
                                '//*[@class="frame w-1-1 whiplash-block"]//span/text()'],
                               ['//*[@class="accordion accordion-frame"]//img/@data-src',
                                '//*[@class="accordion accordion-frame"]//img/@data-src']            
                              ]

            
            adult_occupant.append(['Adult Occupant', adult_occupant_total])

            for count in range(len(adult_occupant_value)):

                impact = adult_occupant_impact[count]                                                                                                
                impact_value = adult_occupant_value[count]
                image = response.xpath(scrap_container[count][0]).getall()
                caption = response.xpath(scrap_container[count][1]).getall()

                if len(caption)<len(image):
                    caption=[caption[0]]+caption
                else:
                    caption=caption[:len(image)]

                
                adult_occupant.append([[impact, impact_value],
                               [[cap, img] for cap, img in zip(caption, image)]])

        except:

            adult_occupant.append(['Adult Occupant', adult_occupant_total])
            adult_occupant_value = response.xpath('//*[@class="frame-points no-frame-info"]/text()').getall()
            adult_occupant_value = [val.strip() for val in adult_occupant_value]
            adult_occupant_value = [val for val in adult_occupant_value if val != ''][:5]
            adult_occupant_impact = response.xpath('//*[@class="frame-title"]/text()').getall()[:5]
            
            scrap_container = [['//*[@class="frame w-1-2 frontal-block"]//img/@data-src', 
                        '//*[@class="frame w-1-2 frontal-block"]//span/text()'],
                       ['//*[@class="frame w-1-2 frontal-full-width"]//img/@data-src',
                        '//*[@class="frame w-1-2 frontal-full-width"]//span/text()'],
                       ['//*[@class="frame w-1-2"]//img/@data-src',
                        '//*[@class="frame w-1-2"]//span/text()'],
                       ['//*[@class="frame w-1-2 whiplash-block"]//img/@data-src',
                        '//*[@class="frame w-1-2 whiplash-block"]//span/text()'],
                       ['//*[@class="frame w-1-1 aeb-city"]//img/@src',
                        '//*[@class="frame w-1-1 aeb-city"]/div//text()']            
                      ]

            for count in range(len(adult_occupant_value)):


                impact = adult_occupant_impact[count]                                                                                                
                impact_value = adult_occupant_value[count]
                image = response.xpath(scrap_container[count][0]).getall()
                captions = response.xpath(scrap_container[count][1]).getall()
                captions = [caption.strip() for caption in captions]
                caption = [caption for caption in captions if caption != '']
                if count == 4:
                    caption=caption[2:]

                        
                adult_occupant.append([[impact, impact_value],
                             [[cap, img] for cap, img in zip(caption, image)]])

        adult_occupant.append(['Comments',
                            response.xpath('//*[@id="tab2-1"]/div//text()').getall()[-3].strip()])


        # Child occupant tab
        child_occupant = []

        child_occupant_texts = response.xpath('//*[@id="tab2-2"]/div//text()').getall()
        child_occupant_texts = [text.strip() for text in child_occupant_texts]
        child_occupant_text = [text for text in child_occupant_texts if text != '']

        if child_occupant_text[6] != "Safety Features":

            if child_occupant_text[6] != "Crash Test Performance":

                image = response.xpath('//*[@class="frame w-1-2"]//img/@data-src').getall()

                child_occupant = [['Child Occupant', child_occupant_text[0]],
                                  [child_occupant_text[6], child_occupant_text[7]],
                                  [child_occupant_text[8], child_occupant_text[9], image[0]],
                                  [child_occupant_text[10], child_occupant_text[11], image[1]],
                                  [child_occupant_text[16], child_occupant_text[17]],
                                  [child_occupant_text[30], child_occupant_text[31]],
                                 ]
            else:

                image = response.xpath('//*[@class="frame w-1-2"]//img/@data-src').getall()
                image = [response.urljoin(img_url) for img_url in image]
                
                child_occupant = [['Child Occupant', child_occupant_text[0]],
                                  [child_occupant_text[6], child_occupant_text[7]],
                                  [child_occupant_text[8], child_occupant_text[9], image[-2]],
                                  [child_occupant_text[13], child_occupant_text[14], image[-1]],
                                  [child_occupant_text[18], child_occupant_text[19]],
                                  [child_occupant_text[32], child_occupant_text[33]],
                                 ]


        else:

            child_occupant = [['Child Occupant', child_occupant_text[0]],
                              [child_occupant_text[6], child_occupant_text[7]],
                              [child_occupant_text[16], child_occupant_text[17]],      
                             ]

        child_occupant.append([child_occupant_text[-2], child_occupant_text[-1]])                     



        # Vulnerable road users tab

        pedestrian = []
        road_users = response.xpath('//*[@id="tab2-3"]/div//text()').getall()
        cleaned_road_users = [road_user.strip() for road_user in road_users]
        cleaned_road_users = [road_user for road_user in cleaned_road_users if road_user != '']

        try:


            pedestrian = [[cleaned_road_users[0][:-2], cleaned_road_users[1]],
                          [cleaned_road_users[7], cleaned_road_users[8]],
                          [cleaned_road_users[9], cleaned_road_users[10]],
                          [cleaned_road_users[11], cleaned_road_users[12]],
                          [cleaned_road_users[13], cleaned_road_users[14]],
                          [cleaned_road_users[15], cleaned_road_users[16]],
                         ] 

            pedestrian.append([response.xpath('//*[@class="accordion-item-header sub-item-header"]/text()').getall()[0].strip(),
                           response.xpath('//*[@class="accordion-item-header sub-item-header"]/span/text()').getall()[1].strip()])

            image = response.xpath('//*[@class="yellow-menu-tabs"]//img/@src').getall()
            captions = response.xpath('//*[@class="yellow-menu-tabs"]//div/text()').getall()
            cleaned_captions = [caption.strip() for caption in captions]
            cleaned_captions = [caption for caption in cleaned_captions if caption != '']
            

            pedestrian.append([[cap, img] for cap, img in zip(cleaned_captions, image)])
            pedestrian.append([response.xpath('//*[@class="accordion-item-header sub-item-header"]/text()').getall()[2].strip(),
                           response.xpath('//*[@class="accordion-item-header sub-item-header"]/span/text()').getall()[-1].strip()])

            image = response.xpath('//*[@class="frame aeb-cyclist"]//img/@src').getall()
            captions = response.xpath('//*[@class="frame aeb-cyclist"]//div/text()').getall()
            cleaned_captions = [caption.strip() for caption in captions]
            cleaned_captions = [caption for caption in cleaned_captions if caption != '']

            pedestrian.append([[cap, img] for cap, img in zip(cleaned_captions, image)])
            pedestrian.append([cleaned_road_users[-2], cleaned_road_users[-1]])

        except:

            pedestrian = [['AEB Pedestrian', cleaned_road_users[0]],
                          [cleaned_road_users[6], cleaned_road_users[7]],
                          [cleaned_road_users[8], cleaned_road_users[9]],
                          [cleaned_road_users[10], cleaned_road_users[11]],
                          [cleaned_road_users[12], cleaned_road_users[13]],                       
                         ]


            try:
                pedestrian.append([response.xpath('//*[@data-menu-group="AEB_VRU"]/text()').getall()[0].strip(),
                               response.xpath('//*[@data-menu-group="AEB_VRU"]/span/text()').getall()[0].strip()])
                pedestrian.append([cleaned_road_users[-2], cleaned_road_users[-1]])

            except:
                pedestrian.append([cleaned_road_users[-2], cleaned_road_users[-1]])




        # Safety Assist tab 
        safety_assist = []

        safety_assist_texts = response.xpath('//*[@id="tab2-4"]/div//text()').getall()
        safety_assist_texts = [text.strip() for text in safety_assist_texts]
        safety_assist_text = [text for text in safety_assist_texts if text != '']
        print(safety_assist_text)

        if safety_assist_text[17] == "Seatbelt Reminder":

            image = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@src').getall() + \
                    response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@src').getall()

            caption = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@alt').getall() + \
                      response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@alt').getall()

            safety_assist = [['Safety Assist', safety_assist_text[0]],
                         [safety_assist_text[6], safety_assist_text[7]],
                         [safety_assist_text[14], safety_assist_text[15]],
                         [safety_assist_text[17], safety_assist_text[18]],
                         [safety_assist_text[32], safety_assist_text[33]],
                         [safety_assist_text[40], safety_assist_text[41]],
                         [safety_assist_text[51], safety_assist_text[52]],
                         [[cap, img] for cap, img in zip(caption, image)]
                        ]

        if safety_assist_text[14] == "Seatbelt Reminder":

            image = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@src').getall() + \
                    response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@src').getall()

            caption = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@alt').getall() + \
                      response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@alt').getall()

            if len(safety_assist_text) >= 43:

                safety_assist = [['Safety Assist', safety_assist_text[0]],
                                 [safety_assist_text[6], safety_assist_text[7]],
                                 [safety_assist_text[14], safety_assist_text[15]],
                                 [safety_assist_text[28], safety_assist_text[29]],
                                 [safety_assist_text[43], safety_assist_text[44]],
                                 [[cap, img] for cap, img in zip(caption, image)]
                                ]
            else:

                safety_assist = [['Safety Assist', safety_assist_text[0]],
                                 [safety_assist_text[6], safety_assist_text[7]],
                                 [safety_assist_text[14], safety_assist_text[15]],
                                 [safety_assist_text[28], safety_assist_text[29]],
                                 [safety_assist_text[-6], safety_assist_text[-5]],
                                 [safety_assist_text[-4], safety_assist_text[-3]],
                                ]

        if safety_assist_text[8] == "Seatbelt Reminder":
            if len(safety_assist_text) < 36:
                safety_assist = [['Safety Assist', safety_assist_text[0]],
                         [safety_assist_text[6], safety_assist_text[7]],
                         [safety_assist_text[8], safety_assist_text[9]],
                         [safety_assist_text[-6], safety_assist_text[-5]],
                         [safety_assist_text[-4], safety_assist_text[-3]],
                        ]

            if len(safety_assist_text) >= 36 and safety_assist_text[36] != "AEB Inter-Urban":
                safety_assist_text[36] = safety_assist_text[34] 
                safety_assist_text[37] = safety_assist_text[35]

                safety_assist = [['Safety Assist', safety_assist_text[0]],
                             [safety_assist_text[6], safety_assist_text[7]],
                             [safety_assist_text[8], safety_assist_text[9]],
                             [safety_assist_text[21], safety_assist_text[22]],
                             [safety_assist_text[36], safety_assist_text[37]],
                            ]

        if len(safety_assist_text) >= 30 and safety_assist_text[30] == "Seatbelt Reminder":

            safety_assist = [['Safety Assist', safety_assist_text[0]],
                         [safety_assist_text[6], safety_assist_text[7]],
                         [safety_assist_text[16], safety_assist_text[17]],
                         [safety_assist_text[30], safety_assist_text[31]],
                         [safety_assist_text[43], safety_assist_text[44]],
                         [safety_assist_text[56], safety_assist_text[57]],
                        ]


        if safety_assist_text[13] == "Seatbelt Reminder":

            safety_assist = [['Safety Assist', safety_assist_text[0]],
                         [safety_assist_text[6], safety_assist_text[7]],
                         [safety_assist_text[8], safety_assist_text[9]],
                         [safety_assist_text[13], safety_assist_text[14]],
                         [safety_assist_text[26], safety_assist_text[27]],
                         [safety_assist_text[28], safety_assist_text[29]]
                        ]

        if safety_assist_text[22] == "Seatbelt Reminder":

            safety_assist = [['Safety Assist', safety_assist_text[0]],
                         [safety_assist_text[6], safety_assist_text[7]],
                         [safety_assist_text[8], safety_assist_text[9]],
                         [safety_assist_text[22], safety_assist_text[23]],
                         [safety_assist_text[35], safety_assist_text[36]],
                         [safety_assist_text[37], safety_assist_text[38]],
                        ]

        safety_assist.append([safety_assist_text[-2], safety_assist_text[-1]])


 
        # Extracting all possible images from the links
        # raw_image_urls_data = response.xpath('//img/@data-src').getall()
        # raw_image_urls = response.xpath('//img/@src').getall()       

        
        #Concentrating only table
        specification_table = response.css("div.tab_container")
        
        col1_data = [specs.css("span.tcol1::text").getall() for specs in specification_table]
        col2_data = [specs.css("span.tcol2::text").getall() for specs in specification_table]
        
        
        yield {

               'rating-title' : response.xpath('//div[@class="rating-title"]/p/text()').getall(),
               'value'        : response.css('div.value::text').getall(),
               'col1' : col1_data,
               'col2' : col2_data,
               'crash_image_urls' : self.clean_url(crash_image_urls, response),
               'adult_occupant' : adult_occupant,
               'child_occupant' : child_occupant,
               'pedestrian' : pedestrian,
               'safety_assist' : safety_assist


        }
      


class PrtclSpider(scrapy.Spider):

    def __init__(self, url, **kwargs):
        self.start_urls = [f'{url}']
        super().__init__(**kwargs)

    def clean_url(self, url, response):


        
            # Cleaning the urls as proper links
            clean_image_urls = []
            print(url)
            for img_url in url:
                clean_image_urls.append(response.urljoin(img_url))
  
            return clean_image_urls

    # Spider name
    name = "Prtcl"

    # Extracting from local file
    # start_urls = ["file:///home/ganesh/scrapy_learning/leaf_node_html.html"]
    
    # start_urls = [filename]
    # Extracting from website
    # start_urls = ["https://www.euroncap.com/en/results/toyota/yaris-cross/43819"]

    

    # Parse functon to extract the features needed
    def parse(self, response):

        
        pdf_links = []
        # Url done
        tables = response.xpath('//*[@class="box white styledLinks"]//table//tbody//td')[0]
        url = tables.xpath('//p').getall()
        for node in url:
            try:
                pdf_links.append(re.findall('(https.*?.pdf)', node))
            except:
                pass

        pdf_link = [link for link in pdf_links if link != []]

    
        # tables = response.xpath('//*[@class="box white styledLinks"]//table//tbody//td')[0]
        # url = tables.css('a[href$=".pdf"]::attr(href)').getall()
        # title = tables.css('a::attr(title)').getall()

        
        prtcl_text = response.xpath('//*[@class="col2"]/div//text()').getall()
        cleaned_prtcl_text = [text.strip() for text in prtcl_text]
        cleaned_prtcl_text = [text for text in cleaned_prtcl_text if text != '']


        year = [word for text in cleaned_prtcl_text for word in text.split() if word.isdigit()]



        

        yield {

         
         'pdf_link' : pdf_link,
         'year' : year,       


        }




        
# the wrapper to make it run more times
def run_spider(spider, url):
    def f(q):
        try:
            # Haivng setting to save and extract image
            settings = get_project_settings()
            settings['ITEM_PIPELINES'] = {'scrapy.pipelines.images.ImagesPipeline': 1}
            settings['IMAGES_STORE'] = '.'
            settings['FEED_FORMAT'] = 'json'
            settings['FEED_URI'] = 'output_file.json'

            # Crawling process
            runner = CrawlerProcess(settings)
            deferred = runner.crawl(spider, url)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)

        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


# Function to webscrappe the EuroNcap webpage
def web_scrapping():

    conn = sqlite3.connect('index_EN.sqlite')
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS Car ''')
    cur.execute('''DROP TABLE IF EXISTS Brand ''')
    cur.execute('''DROP TABLE IF EXISTS Year ''')
    cur.execute('''DROP TABLE IF EXISTS Star ''')

    cur.execute('''DROP TABLE IF EXISTS ResultAll ''')
    cur.execute('''DROP TABLE IF EXISTS Pedestrian ''')
    cur.execute('''DROP TABLE IF EXISTS SafetyAssist ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Car
        (id INTEGER PRIMARY KEY, model TEXT UNIQUE, year_id INTEGER, 
        brand_id INTEGER, star_id INTEGER, url TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Brand
        (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Year
        (id INTEGER PRIMARY KEY, year TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Star
        (id INTEGER PRIMARY KEY, Star TEXT UNIQUE)''')


    conn_1 = sqlite3.connect('file:spiderEN.sqlite?mode=ro', uri=True)
    cur_1 = conn_1.cursor()

    allsenders = list()
    cur_1.execute('''SELECT url,html FROM Pages''')
    
    return cur_1


# Function to remove the unwanted url
def link_screening(link_end, links, prefix):

    """
        Function to clean the urls from the list

        Inputs:
            link_end: gives the end of the main link
                      to match the start of the next
                      link
            links   : list of urls
            prefix  : main url with http

        Return:
            Collection: List of cleaned links


    """

    collection = []

    for link in links:

        # Example "en/about euroncap/"
        look_for_end = str(link).find("/"+link_end, 0, 3)
        look_for_https =  str(link).find("https", 0, 5)
        
        if look_for_end==0:
            # Example "http://www.euroncap.com/en/about euroncap/"
            collection.append(prefix[0:-4]+link)
        
        if look_for_https==0:
            collection.append(link)

    # Set is used to remove duplicates
    return set(collection)


# Function to establish connection between pages
# in Neo4j as nodes
def graph(data):

    """
        This function used to create knowledge graph
        as same as the EuroNcap webpages

        Input:
            Data: Webpage url along with the data
                  of the page in html format

        Return: 
            Nothing creates the graph in Neo4j
            database


    """

    # Variable Declaration
    URLS = []
    HTMLS = []    
    created_URLS = []

    # Main loop
    for URL,HTML in data:

        # Add "/" at the end of the url
        # as the url in html ends with "/"
        URLS.append(URL+"/")
        HTMLS.append(HTML)
    
    # Created range for debugging  
    # (At 90 we have 5 disjoints)  
    urls = URLS[0:-1]
    htmls = HTMLS[0:-1]  

    # Loop for debugging
    for url, html in zip(urls,htmls):
        
        # Query the databse to find if the node already exists
        query = db.cypher_query("MATCH (a:Page) WHERE a.page_url = \""+ str(url)+"\" RETURN True") 

        # Node doesn't exists already
        if url not in created_URLS and query[0] == []:
            
            created_URLS.append(url)
            end_url = url.split("/")[-2 if url.split("/")[-1]== '' else -1 ]
            current_page = Page(page_name= end_url, page_url=url).save()

            # Get all the nodes in database at present
            all_nodes = Page.nodes.all()

            # Get the previous page from current page
            url_split = url.split("/")
            url_split.remove('')
            url_split[0] = url_split[0]+"/"
            number_of_splits = len(url_split)*(-1)
           

            for i in range(-2, number_of_splits, -1):
                
                prev_url = '/'.join([str(elem) for elem in url_split[0:i]])

                # query if the previous url is valid and exists
                query = db.cypher_query("MATCH (a:Page) WHERE a.page_url = \""+ str(prev_url)+"/\" RETURN True")

                # If the previous page exists connect to the current page
                if query[0] !=[]:

                    previous_page = Page.nodes.get(page_url=prev_url+"/")
                    current_page.relation.connect(previous_page) 
                    break            


            # Extract links/url from the html of the current page
            raw_links = re.findall(r'href=[\'"]?([^#\'" >]+)', str(html))
            cleaned_links = link_screening(end_url, raw_links, url)
            

            # Connect the extracted links to current page
            for link in cleaned_links:            
                if link in URLS and link.find(url)==0 and len(link.split("/"))==len(url.split("/"))+1 and link not in created_URLS:

                    created_URLS.append(link)
                    next_page = Page(page_name=link.split("/")[-2 if link.split("/")[-1]== '' else -1 ], page_url=link).save()
                    next_page.relation.connect(current_page)
                    
            

        # Node exists already        
        else:  
            
            # Query and get the node/page
            node = (db.cypher_query("MATCH (a:Page) WHERE a.page_url = \""+ str(url)+"\" RETURN a.page_name, a.page_url"))[0][0]
            all_nodes = Page.nodes.all()
            existing_page = Page.nodes.get(page_name=node[0])
            
            raw_links = re.findall(r'href=[\'"]?([^#\'" >]+)', str(html))
            cleaned_links = link_screening(end_url, raw_links, url)
            

            for link in cleaned_links:            
                if link in URLS and link.find(url)==0 and len(link.split("/"))==len(url.split("/"))+1 and link not in created_URLS:

                    created_URLS.append(link)
                    next_page = Page(page_name=link.split("/")[-2 if link.split("/")[-1]== '' else -1 ], page_url=link).save()
                    next_page.relation.connect(existing_page)

    # Delete the hanging node since there is no page
    db.cypher_query("MATCH (n) WHERE not( (n)-[]-() ) DELETE n") 
                    
    return URLS, HTMLS


# This function is used to organize the leaf node
def leaf_nodes(URLS, HTMLS):

    empty_nodes = []

    # Get all the nodes in database at present
    all_nodes = Page.nodes.all()

    # Query to get the leaf node of the root node storing URL because node names repeat in the results
    # But URLS are different
    query = (db.cypher_query("MATCH (a:Page {page_name: \"en\"})-[r]-(b) Where not (b)<--() Return b.page_url"))[0]

    # Making list of leaf nodes from list of list 
    pagenames = set(['/'.join([str(pagename) for pagename in elem]) for elem in query])

    # Removing this URL since the URL is to be used separately
    # pagenames.remove("https://www.euroncap.com/en/results/")
    
    # Getting the root node
    root = Page.nodes.get(page_name="en")
    
    #Creating a result node
    result_node = Page(page_name="result", page_url="https://www.euroncap.com/en/results/").save()
    result_node.relation.connect(root)

    # Removeing the old json file if it exists
    if "output_file.json" in os.listdir('.'):
        os.remove('output_file.json')


    # Test list    
    # pagenames = ["https://www.euroncap.com/en/results/suzuki/baleno/24497/", "https://www.euroncap.com/en/results/toyota/aygo/29355/",
    #              "https://www.euroncap.com/en/results/opel/vauxhall/karl/28538/", "https://www.euroncap.com/en/results/ford/ka+/26314/"]
    # Making the leaf nodes to connect with results node
    for node in pagenames:
        
        # Run scrapy to scrape the html content from url
        # into a json file
        run_spider(EuroncapSpider, str(node))
        print(str(node))

        # Add try and except
        # sometimes the file is empty due to page unavailable
        # it throws error
        try:
            df = pd.DataFrame.from_dict(pd.read_json('output_file.json'))
            os.remove('output_file.json')

            leaf = Page.nodes.get(page_url=str(node))
            leaf.relation.disconnect(root)

            value = list(chain.from_iterable(df['value']))
            col1 = list(chain.from_iterable(df['col1'][0]))
            specs = list(chain.from_iterable(df['col2'][0]))
            # model_idx = col1.index('Tested Model')
            # class_idx = col1.index('Class')

            
            year_idx = col1.index('Year Of Publication')
            # print("column1 values", col1)
            # weight_idx = col1.index('Kerb Weight')
            # body_idx = col1.index('Body Type')
            # vin_idx = col1.index('')

            # Creating a new node with data from HTML
            current_page = Resultpage(resultpage_name =  leaf.page_name,
                                      resultpage_url = leaf.page_url,                                          
                                      resultpage_tested_model = specs if specs ==[] else specs[0],   
                                      resultpage_body_type = specs if specs ==[] else specs[-5],    
                                      resultpage_year_of_publication = specs if specs ==[] else specs[year_idx], #specs[-4],    
                                      resultpage_kerb_weight = specs if specs ==[] else specs[-3],    
                                      resultpage_vin = specs if specs ==[] else specs[-2],    
                                      resultpage_class = specs if specs ==[] else specs[-1],
                                      resultpage_test_image_url = df['crash_image_urls'][0],
                                      resultpage_adultoccupant = df['adult_occupant'][0],
                                      resultpage_childoccupant = df['child_occupant'][0],
                                      resultpage_pedestrain = df['pedestrian'][0],
                                      resultpage_safety_assist = df['safety_assist'][0]).save()

            # Deleting the exisiting node
            leaf.delete()
            current_page.relationf.connect(result_node)    


        except ValueError as v:

            leaf = Page.nodes.get(page_url=str(node))
            leaf.relation.disconnect(root)
            empty_nodes.append(str(node))


            # Deleting the exisiting node
            leaf.delete()      
       
    print("Number of empty pages are", len(empty_nodes), "\n", empty_nodes)
    return



# Function for having the node based on proper class
def class_categorization():

    # Get all the nodes in database at present
    all_nodes = Page.nodes.all()

    # Query to get the leaf node of the root node storing URL because node names repeat in the results
    # But URLS are different
    query = (db.cypher_query("MATCH (a:Resultpage) return a.resultpage_class"))[0]

    # Flatten the list
    flattened_query = list(chain.from_iterable(query))

    # Check for empty list and remove
    car_class = [item for item in flattened_query if item != "[]"]

    # Get the previous result node
    result_node = Page.nodes.get(page_name="result")

    # Add the class nodes for car
    for classname in list(set(car_class)):
        current_node = Class(class_name =  classname).save()
        current_node.relation.connect(result_node)

    # Get all the car nodes linked to "result"
    car_node =  (db.cypher_query("MATCH (a:Resultpage) return a.resultpage_url"))[0]  

    car_nodes = [car for car in list(chain.from_iterable(car_node)) if car not in car_class]


    # Create new nodes for protocols and safety ratings
    new_node_adult = Aop(aop_name = "Adult occupant").save()
    new_node_child = Cop(cop_name = "Child occupant").save()
    new_node_pedestrain = Sas(sas_name = "Safety Assist").save()
    new_node_safetyassist = Vru(vru_name = "Pedestrian").save()

    # Create year nodes
    query_yr = (db.cypher_query("MATCH (a:Resultpage) return a.resultpage_year_of_publication"))[0]

    # Flatten the list
    flattened_query_yr = list(chain.from_iterable(query_yr))

    # Check for empty list and remove
    pub_year = [item for item in flattened_query_yr if item != "[]"]
    # print(pub_year)

    # Add the class nodes for car
    for year in list(set(pub_year)):
        year_node = Year(year_name = year).save()



    # Make a connection of the car node to respective class from result node
    for node in car_nodes:
        # try:
        current_node = Resultpage.nodes.get(resultpage_url=node)
        previous_node = Class.nodes.get(class_name=current_node.resultpage_class)
        current_node.relationf.disconnect(result_node)
        new_node = Vehicle(vehicle_name=current_node.resultpage_tested_model,
                           vehicle_url=current_node.resultpage_url,            
                           vehicle_body_type = current_node.resultpage_body_type,
                           vehicle_year_of_publication = current_node.resultpage_year_of_publication,    
                           vehicle_kerb_weight = current_node.resultpage_kerb_weight,    
                           vehicle_vin = current_node.resultpage_vin,
                           vehicle_test_image_url = current_node.resultpage_test_image_url).save()
        new_node.relation.connect(previous_node)

        new_year_node = Year.nodes.get(year_name = new_node.vehicle_year_of_publication)
        new_year_node.relation.connect(new_node)     

        new_node_adult = Aop.nodes.get(aop_name = "Adult occupant")
        new_node_adult.relation.connect(new_node, {'aop_ratings': current_node.resultpage_adultoccupant})        

        new_node_child = Cop.nodes.get(cop_name = "Child occupant")
        new_node_child.relation.connect(new_node, {'cop_ratings': current_node.resultpage_childoccupant})        

        new_node_safetyassist = Sas.nodes.get(sas_name = "Safety Assist")
        new_node_safetyassist.relation.connect(new_node, {'sas_ratings': current_node.resultpage_safety_assist})

        new_node_pedestrain = Vru.nodes.get(vru_name = "Pedestrian")
        new_node_pedestrain.relation.connect(new_node, {'vru_ratings': current_node.resultpage_pedestrain})

        
        (db.cypher_query("MATCH (n {vehicle_url: \"" + str(current_node.resultpage_url) + "\"}) SET n:Resultpage"))
        current_node.relationclass.connect(previous_node)        

    
    # Delete the class property since we grouped
    (db.cypher_query("MATCH (a:Resultpage) remove a.resultpage_body_type,\
                                                  a.resultpage_year_of_publication,\
                                                  a.resultpage_kerb_weight,\
                                                  a.resultpage_vin,\
                                                  a.resultpage_class,\
                                                  a.resultpage_test_image_url,\
                                                  a.resultpage_adultoccupant,\
                                                  a.resultpage_childoccupant,\
                                                  a.resultpage_pedestrain,\
                                                  a.resultpage_safety_assist"))

       
    

    return


# Function to establish protocol connections
def protocol_connection():

    # Get all the nodes in database at present
    all_nodes = Page.nodes.all()

    # Removeing the old json file if it exists
    if "output_file.json" in os.listdir('.'):
        os.remove('output_file.json')

    prtcl_links = ["https://www.euroncap.com/en/for-engineers/protocols/adult-occupant-protection/",
                   "https://www.euroncap.com/en/for-engineers/protocols/child-occupant-protection/",
                   "https://www.euroncap.com/en/for-engineers/protocols/vulnerable-road-user-vru-protection/",
                   "https://www.euroncap.com/en/for-engineers/protocols/safety-assist/",]

    rating = ["Adult occupant", "Child occupant", "Pedestrian", "Safety Assist"]
    # page_nodes = [link.split("/")[-2] for link in prtcl_links]

    yearset = []

    for count, link in enumerate(prtcl_links):
        
        # Run scrapy to scrape the html content from url
        # into a json file
        run_spider(PrtclSpider, str(link))
        print(str(link))

        df = pd.DataFrame.from_dict(pd.read_json('output_file.json'))
        os.remove('output_file.json')

        query_yr = (db.cypher_query("MATCH (a:Year) return a.year_name"))[0]

        # Flatten the list
        pub_year = list(chain.from_iterable(query_yr))

        # Loop in different protocols
        for pdf in df['pdf_link']:
            for idx, link in enumerate(pdf):
                # Conection with respective rating node and page node
                end_url = str(link).split("/")[-2 if str(link).split("/")[-1]== '' else -1][:-6]
                current_prtcl = Prtcl(prtcl_name= end_url, prtcl_url=str(link)).save()
                
                if count == 0:
                    new_node_adult = Aop.nodes.get(aop_name = rating[count])
                    current_prtcl.relation2.connect(new_node_adult)
                    page = Page.nodes.get(page_url = prtcl_links[count])
                    current_prtcl.relation6.connect(page)

                if count == 1:
                    new_node_adult = Cop.nodes.get(cop_name = rating[count])
                    current_prtcl.relation1.connect(new_node_adult)
                    page = Page.nodes.get(page_url = prtcl_links[count])
                    current_prtcl.relation6.connect(page)

                if count == 2:
                    new_node_adult = Vru.nodes.get(vru_name = rating[count])
                    current_prtcl.relation4.connect(new_node_adult)
                    page = Page.nodes.get(page_url = prtcl_links[count])
                    current_prtcl.relation6.connect(page)

                if count == 3:
                    new_node_adult = Sas.nodes.get(sas_name = rating[count])
                    current_prtcl.relation3.connect(new_node_adult)
                    page = Page.nodes.get(page_url = prtcl_links[count])
                    current_prtcl.relation6.connect(page)                           

                # Coonection with years
                if df['year'][0][idx] not in yearset and df['year'][0][idx] not in pub_year:
                    new_year_node = Year(year_name = df['year'][0][idx]).save()
                    current_prtcl.relation5.connect(new_year_node)
                    yearset.append(df['year'][0][idx])

                else:
                    new_year_node = Year.nodes.get(year_name = df['year'][0][idx])
                    current_prtcl.relation5.connect(new_year_node)       

        

    return


def external_connection():

    # # Get all the nodes in database at present
    all_nodes = Page.nodes.all()

    query_imp = (db.cypher_query("MATCH (n:Imp) RETURN n.imp_impact"))[0]

    imp_node = list(chain.from_iterable(query_imp))

    for imp in set(imp_node):
        if imp == 'pedestrian':
            # Connecting imp node to vru
            # using cypher because we can get imp node since
            # its external one, there is no defenition here
            (db.cypher_query("MATCH (n:Imp), (a:Vru)-[:DEFINE_AS]-(b) CREATE (n)-[:BELONGS_TO]->(b)"))
            
        else:
            print("No Impact node, so connection to impact node is skipped")

    
    # connecting veh node to year

    query_veh = (db.cypher_query("MATCH (n:Veh) RETURN n.veh_year"))[0]
    veh_year = list(chain.from_iterable(query_veh))

    # veh_tuple = [(veh_node[count], veh_node[count+1]) for count in range(int(len(veh_node)/2))]

    for year in set(veh_year):
        
        if year == None:
            year =2022
            db.cypher_query("MATCH (n:Veh) SET n.veh_year = \"" + str(year) + "\"")
        
        else:
            pass
        
        db.cypher_query("MATCH (n:Veh {veh_year:\"" + str(year) + "\"}), (y:Year {year_name:\""+str(year)+"\"}) CREATE (n)-[:PUBL_IN]->(y)")

    


    return




if __name__ == '__main__':

    # Webscrape the EuroNcap webpage
    data = web_scrapping()

    # Establish the connection with Neo4j
    db.set_connection('bolt://neo4j:euroncap@localhost:7687')
    # db.set_connection('bolt://neo4j:euroncap@localhost:4687')
    
    # Delete all the existing nodes
    db.cypher_query("MATCH (n) DETACH DELETE n")
    
    # Main Function to connect the nodes
    URLS, HTMLS = graph(data)
   
    # Building base graph with links 
    # and respective html page of it
    leaf_nodes(URLS, HTMLS)

    # Categorizing based on vehicle
    # Class and year
    class_categorization()

    # Adding protocol to the 
    # Existing year and class
    protocol_connection()

    # Buliding connection with the
    # main graph
    # external_connection()
    

    
    
