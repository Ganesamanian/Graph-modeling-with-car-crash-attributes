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

        try:

            # Extracting images from desired location
            # having data and data-src as per the outline of the page

            # Extracting the Test image
            crash_image_urls_data = response.xpath('//*[@class="reward-images"]//img/@data-src').getall()
            crash_image_urls = crash_image_urls_data + response.xpath('//*[@class="reward-images"]//img/@src').getall()

            # Extracting the adult occupant image
            adult_occupant_image_urls_data = response.xpath('//*[@class="frame-content"]//img/@data-src').getall()
            adult_occupant_image_urls = adult_occupant_image_urls_data + response.xpath('//*[@class="frame-content"]//img/@src').getall()

            # Extracting the pedestrian image
            pedestrian_image_urls_data = response.xpath('//*[@class="pedestrian-protection"]//img/@data-src').getall()
            pedestrian_image_urls = pedestrian_image_urls_data + response.xpath('//*[@class="pedestrian-protection"]//img/@src').getall()

            # Extracting the safety image
            brakesafety_image_urls_data = response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@data-src').getall()
            brakesafety_image_urls = brakesafety_image_urls_data + response.xpath('//*[@id="tabAutoBrakeFunctionOnly"]//img/@src').getall()
            
            safety_image_urls_data = brakesafety_image_urls + response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@data-src').getall()
            safety_image_urls = safety_image_urls_data + response.xpath('//*[@id="tabDriverReactsToWarning"]//img/@src').getall()      

            

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
                   'adult_occupant_image_urls' : self.clean_url(adult_occupant_image_urls, response),
                   'pedestrian_image_urls' : self.clean_url(pedestrian_image_urls, response),
                   'safety_image_urls' : self.clean_url(safety_image_urls, response)


            }
        except:
            yield {

                   'rating-title' : ' ',
                   'value'        : ' ',
                   'col1' : ' ',
                   'col2' : ' ',
                   'crash_image_urls' : ' ',
                   'adult_occupant_image_urls' : ' ',
                   'pedestrian_image_urls' : ' ',
                   'safety_image_urls' : ' ',


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
                    
    return URLS, HTMLS


# This function is used to organize the leaf node
def leaf_nodes(URLS, HTMLS):

    # Get all the nodes in database at present
    all_nodes = Page.nodes.all()

    # Query to get the leaf node of the root node storing URL because node names repeat in the results
    # But URLS are different
    query = (db.cypher_query("MATCH (a:Page {page_name: \"en\"})-[r]-(b) Where not (b)<--() Return b.page_url"))[0]

    # Making list of leaf nodes
    pagenames = set(['/'.join([str(pagename) for pagename in elem]) for elem in query])

    # Removing this URL since the URL is to be used separately
    # pagenames.remove("https://www.euroncap.com/en/results/")
    
    # Getting the root node
    root = Page.nodes.get(page_name="en")


    
    # Creating a result node
    result_node = Page(page_name="result", page_url="https://www.euroncap.com/en/results/").save()
    result_node.relation.connect(root)

    if "output_file.json" in os.listdir('.'):
        os.remove('output_file.json')


    # Making the leaf nodes to connect with results node
    for counter, node in enumerate(pagenames):
        
        # # Saving HTML data to a file
        # idx = URLS.index(str(node))

        # f = open("leaf_node_html_test.html", "w")
        # f.write(str(HTMLS[idx]))
        # f.close()       
        
        # Scraping the saved file into Json 
        # time.sleep(2)
        run_spider(EuroncapSpider, str(node))
        print(str(node))
        # Add try and except
        try:
            df = pd.DataFrame.from_dict(pd.read_json('output_file.json'))
            os.remove('output_file.json')

            leaf = Page.nodes.get(page_url=str(node))
            leaf.relation.disconnect(root)

            value = list(chain.from_iterable(df['value']))
            specs = list(chain.from_iterable(df['col2'][0]))
            # Creating a new node with data from HTML
            current_page = Resultpage(resultpage_name =  leaf.page_name,
                                      resultpage_url = leaf.page_url,
                                      resultpage_adult_occupant = value if value ==[] else value[0],
                                      resultpage_child_occupant = value if value ==[] else value[1],   
                                      resultpage_vulnerable_roadusers = value if value ==[] else value[2],    
                                      resultpage_safety_assist = value if value ==[] else value[3],    
                                      resultpage_tested_model = specs if specs ==[] else specs[0],   
                                      resultpage_body_type = specs if specs ==[] else specs[-5],    
                                      resultpage_year_of_publication = specs if specs ==[] else specs[-4],    
                                      resultpage_kerb_weight = specs if specs ==[] else specs[-3],    
                                      resultpage_vin = specs if specs ==[] else specs[-2],    
                                      resultpage_class = specs if specs ==[] else specs[-1],
                                      resultpage_test_image_url = df['crash_image_urls'][0],
                                      resultpage_adultoccupant_image_url = df['adult_occupant_image_urls'][0],
                                      resultpage_pedestrain_image_url = df['pedestrian_image_urls'][0],
                                      resultpage_safety_image_url = df['safety_image_urls'][0]).save()

            # Deleting the exisiting node
            leaf.delete()
            current_page.relationf.connect(result_node)

        except:

            leaf = Page.nodes.get(page_url=str(node))
            leaf.relation.disconnect(root)

            # Deleting the exisiting node
            leaf.delete()  
        

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
        current_node = Resultpage(resultpage_name =  classname).save()
        current_node.relationf.connect(result_node)

    # Get all the car nodes linked to "result"
    car_node =  (db.cypher_query("MATCH (a:Resultpage) return a.resultpage_url"))[0]  

    # Make a connection of the car node to respective class from result node
    for node in list(chain.from_iterable(car_node)):
        try:
            current_node = Resultpage.nodes.get(resultpage_url=node)
            previous_node = Resultpage.nodes.get(resultpage_name=current_node.resultpage_class)
            current_node.relationf.disconnect(result_node)
            current_node.relation.connect(previous_node)
            # Delete the class property since we grouped
            db.cypher_query("MATCH (n:Resultpage {resultpage_url:\"" + str(node) + "\"}) REMOVE n.resultpage_class")

        except:
            pass
    
    # Delete the free nodes that don't belong to the class
    leaf_node = (db.cypher_query("MATCH (a:Page {page_name: \"result\"})-[r]-(b) Where not (b)<--() Return b.resultpage_name"))[0]
    for node in list(chain.from_iterable(leaf_node)):
        if node not in car_class:
            free_node = Resultpage.nodes.get(resultpage_name=node)
            free_node.delete()


    # Delete the hanging node since there is no page
    db.cypher_query("MATCH (n) WHERE not( (n)-[]-() ) DELETE n")
    

    return



if __name__ == '__main__':

    # Webscrape the EuroNcap webpage
    data = web_scrapping()

    # Establish the connection with Neo4j
    db.set_connection('bolt://neo4j:Minion1$@localhost:7687')
    
    # Delete all the existing nodes
    db.cypher_query("MATCH (n) DETACH DELETE n")
    
    # Main Function to connect the nodes
    URLS, HTMLS = graph(data)
   
    leaf_nodes(URLS, HTMLS)

   
    class_categorization()
    
    
    

  



