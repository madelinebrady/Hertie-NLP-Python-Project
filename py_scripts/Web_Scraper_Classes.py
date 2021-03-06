# coding: utf-8

# # Web Scraper Tool for US Media Outlets

import requests
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


class WebScraper:
    """
    A class used to scrape articles from eight different U.S. media outlets.
    """
    @staticmethod
    def scrape_breitbart():
        """
        Scrapes new articles from breitbart.com/politics
        return: pd.DataFrame
        """
        # load the HTML content using requests and save into a variable
        breitbart_request = requests.get('https://www.breitbart.com/politics/')
        breitbart_homepage = breitbart_request.content

        # create soup 
        breitbart_soup = BeautifulSoup(breitbart_homepage, 'html.parser')

        # locate article URLs
        breitbart_tags = breitbart_soup.find_all('h2')

        # get article titles, content, dates, and links
        breitbart_links = []
        breitbart_titles = []
        breitbart_dates = []
        breitbart_contents = []

        for n in np.arange(0, min(len(breitbart_tags), 30)):

            # get article link
            link = breitbart_tags[n].find('a')['href']
            link = "https://www.breitbart.com" + link
            breitbart_links.append(link)

            # get article title
            title = breitbart_tags[n].find('a').get_text()
            breitbart_titles.append(title)

            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get publication datetime
            date = soup_article.time.attrs['datetime']
            date = date[:-10]
            breitbart_dates.append(date)

            # get article content
            body = soup_article.find_all('div', class_='entry-content')
            x = body[0].find_all('p')

            # combine paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)

            breitbart_contents.append(final_article)

        # assembling data
        breitbart_data = pd.DataFrame.from_dict({
            'publisher': 'Breitbart',
            'date': breitbart_dates,
            'link': breitbart_links,
            'article_title': breitbart_titles,
            'article_text': breitbart_contents 
        })

        return breitbart_data

    @staticmethod
    def scrape_fox():
        """
        Scrapes new articles from foxnews.com/politics
        return: pd.DataFrame
        """
        # load the HTML content using requests and save into a variable
        fox_requests = requests.get('https://www.foxnews.com/politics')
        fox_homepage = fox_requests.content

        # create a soup to allow BeautifulSoup to work
        fox_soup = BeautifulSoup(fox_homepage, 'html.parser')

        # locate article links
        fox_tags = fox_soup.find_all('article')

        # get homepage article links
        fox_links = []
        fox_text = []
        fox_titles = []
        fox_dates = []

        for n in np.arange(0, len(fox_tags)):
            link = fox_tags[n].find('a')
            link = link.get('href')
            link = "https://foxnews.com" + link
            fox_links.append(link)
            fox_links = [x for x in fox_links if "/v/" not in x]
            fox_links = [x for x in fox_links if "https://foxnews.comhttps://www.foxnews.com" not in x]

        # prep for article content
        for link in fox_links:
            fox_article_request = requests.get(link)
            fox_article = fox_article_request.content
            fox_article_soup = BeautifulSoup(fox_article, 'html.parser')

            # get article metadata
            fox_metadata = fox_article_soup.find_all('script')[2].get_text()
            fox_metadata = fox_metadata.split(",")

            for item in fox_metadata:

                # get article title
                if 'headline' in item:
                    item = item.replace('\n',"")
                    item = item.replace('headline', "")
                    item = item.replace(':', "")
                    item = item.replace('"', '')
                    fox_titles.append(item)

                # get article date
                elif 'datePublished' in item:
                    item = item.replace('\n',"")
                    item = item.replace('datePublished', "")
                    item = item.replace(':', "")
                    item = item.replace('"', '')
                    fox_dates.append(item)

            # get article text
            body = fox_article_soup.find_all('div')
            x = body[0].find_all('p')

            # combine paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                paragraph = paragraph.replace('\n',"")
                list_paragraphs.append(paragraph)

                # removing copyright info and newsletter junk from the article
                final_article = " ".join(list_paragraphs)
                final_article = final_article.replace("This material may not be published, broadcast, rewritten, or redistributed. ©2020 FOX News Network, LLC. All rights reserved. All market data delayed 20 minutes.", " ")
                final_article = final_article.replace("This material may not be published, broadcast, rewritten,", " ")
                final_article = final_article.replace("or redistributed. ©2020 FOX News Network, LLC. All rights reserved.", " ")
                final_article = final_article.replace("All market data delayed 20 minutes.", " ")
                final_article = final_article.replace("Get all the stories you need-to-know from the most powerful name in news delivered first thing every morning to your inbox Subscribed You've successfully subscribed to this newsletter!", " ")
            fox_text.append(final_article)

        # join fox data
        fox_data = pd.DataFrame.from_dict({
            'publisher': 'Fox',
            'date': fox_dates,
            'link': fox_links,
            'article_title': fox_titles,
            'article_text': fox_text 
        })
        
        return fox_data

    @staticmethod
    def scrape_wt():
        """
        Scrapes new articles from washingtontimes.com/news/politics
        return: pd.DataFrame
        """
        # load the HTML content using requests and save into a variable
        wt_request = requests.get('https://www.washingtontimes.com/news/politics/')
        wt_homepage = wt_request.content

        # create soup 
        wt_soup = BeautifulSoup(wt_homepage, 'html.parser')

        # locate article URLs
        wt_tags = wt_soup.find_all('h2', class_='article-headline')

        # get article titles, content, dates, and links
        wt_links = []
        wt_titles = []
        wt_dates = []
        wt_contents = []

        for n in np.arange(0, len(wt_tags)):

            # get article link
            link = wt_tags[n].find('a')['href']
            link = 'https://www.washingtontimes.com' + link
            wt_links.append(link)

            # get article title
            title = wt_tags[n].find('a').get_text()
            wt_titles.append(title)
    
            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get publication datetime
            meta = soup_article.find('div', class_='meta').find('span', class_='source').text
            strip = meta.replace(' -\n\t\t\t\n\t\t\t\tAssociated Press\n -\n                      \n                        \n                        ', '')
            strip = strip.replace(' -\n\t\t\t\n\t\t\t\tThe Washington Times\n -\n                      \n                        \n                        ', '')
            date = strip.replace('\n                      \n                    ', '')
            wt_dates.append(date)

            # get article content
            for div in soup_article.find_all('div', {'class':'article-toplinks'}):
                div.decompose()

            body = soup_article.find_all('div', class_= 'bigtext')  
            x = body[0].find_all('p')

            # combine paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs).split("\n")[0]

            wt_contents.append(final_article)

        # assembling data
        wt_data = pd.DataFrame.from_dict({
            'publisher': 'washington_times',
            'date': wt_dates,
            'link': wt_links,
            'article_title': wt_titles,
            'article_text': wt_contents 
        })

        return wt_data

    @staticmethod
    def scrape_ap():
        """
        Scrapes new articles from apnews.com/apf-politics 
        return: pd.DataFrame
        """ 
        # load the HTML content using requests and save into a variable
        ap_requests = requests.get('https://apnews.com/apf-politics')
        ap_homepage = ap_requests.content

        # create a soup to allow BeautifulSoup to work
        ap_soup = BeautifulSoup(ap_homepage, 'html.parser')

        # locate articles
        ap_tags = ap_soup.find_all('a', class_='Component-headline-0-2-106')

        # get homepage article links
        ap_links = []

        for link in ap_tags:
            link = link.get('href')
            link = 'https://apnews.com' + link
            ap_links.append(link)

        # get article title, date, and content
        ap_text = []
        ap_titles = []
        ap_dates = []

        for link in ap_links:
            ap_article_request = requests.get(link)
            ap_article = ap_article_request.content
            ap_article_soup = BeautifulSoup(ap_article, 'html.parser')

            # article titles
            title = ap_article_soup.find_all('meta')[14]
            title = title['content']
            ap_titles.append(title)

            # article date
            date = ap_article_soup.find_all('meta')[24]
            date = date['content']
            ap_dates.append(date)

            # article content: <div class="Article" data-key=Article.
            body = ap_article_soup.find_all('div')
            x = body[0].find_all('p')

            # combine paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                paragraph = paragraph.replace('\n',"")
                paragraph = paragraph.replace('CHICAGO (AP) -',"")
                paragraph = paragraph.replace('DETROIT (AP) -',"")
                paragraph = paragraph.replace('WASHINGTON (AP) -',"")
                paragraph = paragraph.replace('___ Catch up on the 2020 election campaign with AP experts on our weekly politics podcast, “Ground Game.',"")
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
            ap_text.append(final_article)

        # join ap data
        ap_data = pd.DataFrame.from_dict({
            'publisher': 'AP',
            'date': ap_dates,
            'link': ap_links,
            'article_title': ap_titles,
            'article_text': ap_text 
        })
        
        return ap_data 

    @staticmethod
    def scrape_nbc():
        """
        Scrapes new articles from nbcnews.com/politics 
        return: pd.DataFrame
        """ 
        # load the HTML content using requests and save into a variable
        nbc_request = requests.get('https://www.nbcnews.com/politics')
        nbc_homepage = nbc_request.content

        # create soup 
        nbc_soup = BeautifulSoup(nbc_homepage, 'html.parser')

        # locate article URLs
        nbc_tags = nbc_soup.find_all('h2', class_='teaseCard__headline') + nbc_soup.find_all('h2', class_='title___2T5qK')

        # get article titles, content, dates, and links
        nbc_links = []
        nbc_titles = []
        nbc_dates = []
        nbc_contents = []

        for n in np.arange(0, len(nbc_tags)):

            # get article link
            link = nbc_tags[n].find('a')['href']
            nbc_links.append(link)

            # get article title
            title = nbc_tags[n].find('a').get_text()
            nbc_titles.append(title)

            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get publication datetime
            if soup_article.time != None:
                date = soup_article.time.attrs['datetime']
                date = date[4:-24] 
            else:
                date = None
            nbc_dates.append(date)

            # get article content
            body = soup_article.find_all('div', class_= 'article-body__content')    
            final_article = " ".join([item.text for item in body])

            nbc_contents.append(final_article)

        # assembling data
        nbc_data = pd.DataFrame.from_dict({
            'publisher': 'nbc',
            'date': nbc_dates,
            'link': nbc_links,
            'article_title': nbc_titles,
            'article_text': nbc_contents 
        })

        # dropping rows that are not text articles (these will have NA in date)
        nbc_data = nbc_data.dropna()
        
        return nbc_data

    @staticmethod
    def scrape_nyt():
        """
        Scrapes new articles from nytimes.com/section/politics 
        return: pd.DataFrame
        """ 
        # load the HTML content using requests and save into a variable
        nyt_request = requests.get('https://www.nytimes.com/section/politics')
        nyt_homepage = nyt_request.content

        # create soup 
        nyt_soup = BeautifulSoup(nyt_homepage, 'html.parser')

        # homepage URLs
        nyt_tags_home = nyt_soup.find_all('h2', class_='css-l2vidh e4e4i5l1')

        # setup 
        nyt_links = []
        nyt_titles = []
        nyt_dates = []
        nyt_contents = []

        # articles, links, titles, and content
        for n in np.arange(0, len(nyt_tags_home)):

            # get article link
            link = nyt_tags_home[n].find('a')['href']
            link = "https://www.nytimes.com" + link
            nyt_links.append(link)

            # get article title
            title = nyt_tags_home[n].find('a').get_text()
            nyt_titles.append(title)

            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get publication datetime
            date = soup_article.time.attrs['datetime']
            date = date[:-15]
            nyt_dates.append(date)

            # get article content
            for div in soup_article.find_all("div", {'class': 'css-9tf9ac'}):
                div.decompose()

            body = soup_article.find_all('div', {'class':['css-53u6y8', 'css-1fanzo5']})
            final_article = " ".join([item.text for item in body])

            nyt_contents.append(final_article)
            
        # assembling data
        nyt_data = pd.DataFrame.from_dict({
            'publisher': 'new_york_times',
            'date': nyt_dates,
            'link': nyt_links,
            'article_title': nyt_titles,
            'article_text': nyt_contents 
        })
        
        return nyt_data

    @staticmethod
    def scrape_politico():
        """
        Scrapes new articles from politico.com/politics
        return: pd.DataFrame
        """ 
        # load the HTML content using requests and save into a variable
        politico_request = requests.get('https://www.politico.com/politics')
        politico_homepage = politico_request.content

        # create soup 
        politico_soup = BeautifulSoup(politico_homepage, 'html.parser')

        # locate article URLs
        politico_tags = politico_soup.find_all('h3')

        # get article titles, content, dates, and links
        politico_links = []

        for n in np.arange(0, len(politico_tags)):
            # get article link
            link = politico_tags[n].find('a')['href']
            if "/news/" in link:
                politico_links.append(link)

        politico_titles = []
        politico_dates = []
        politico_contents = []

        for link in politico_links:

            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get article title
            title = soup_article.find('h2', attrs={'class':'headline'}).get_text()
            politico_titles.append(title)

            # get publication datetime
            date = soup_article.time.attrs['datetime']
            date = date[:-9]
            politico_dates.append(date)

            # get article content
            body = soup_article.find_all('p', attrs={'class':'story-text__paragraph'})
            final_article = " ".join([item.text for item in body])

            politico_contents.append(final_article)

        # assembling data
        politico_data = pd.DataFrame.from_dict({
            'publisher': 'politico',
            'date': politico_dates,
            'link': politico_links,
            'article_title': politico_titles,
            'article_text': politico_contents 
        })
        
        return politico_data

    @staticmethod
    def scrape_buzzfeed():
        """
        Scrapes new articles from buzzfeednews.com/section/politics
        return: pd.DataFrame
        """ 
        # load the HTML content using requests and save into a variable
        buzz_request = requests.get('https://www.buzzfeednews.com/section/politics')
        buzz_homepage = buzz_request.content

        # create soup
        buzz_soup = BeautifulSoup(buzz_homepage, 'html.parser')

        # locate article URLs
        buzz_tags = buzz_soup.find_all('h2')

        # get article titles, content, dates, and links
        buzz_links = []
        buzz_titles = []
        buzz_dates = []
        buzz_contents = []

        for n in np.arange(0, min(len(buzz_tags), 30)):

            # get article link
            link = buzz_tags[n].find('a')['href']
            buzz_links.append(link)

            # get article title
            title = buzz_tags[n].find('a').get_text()
            buzz_titles.append(title)

            # prep article content
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')

            # get publication datetime
            date = soup_article.find_all('div', class_='news-article-header__timestamps')
            date = " ".join([item.text for item in date]).replace('\n', '')
            buzz_dates.append(date)

            # get article content
            body = soup_article.find_all('div', attrs={'data-module':'subbuzz-text'})
            article = " ".join([item.text for item in body]).replace('\n', '')
            final_article = re.sub(r' {[^}]*}', '', article)

            buzz_contents.append(final_article)

        # assembling data
        buzz_data = pd.DataFrame.from_dict({
            'publisher': 'buzzfeed',
            'date': buzz_dates,
            'link': buzz_links,
            'article_title': buzz_titles,
            'article_text': buzz_contents 
        })

    @staticmethod
    def save_data(outlet, scraped_df):
        """
        Concatenates scraped data to old df and saves new data set
        return: pd.DataFrame
        """
        # read in old data
        old_data = pd.read_csv('data/' + outlet + '_data.csv')
        num_old = len(old_data)

        # append new data
        new_data = old_data.append(scraped_df).drop_duplicates()

        # save new .csv
        new_data.to_csv('data/' + outlet + '_data.csv', index = False)
        num_now = len(new_data)

        print("number of entries in old {} data: {}".format(outlet, num_old))
        print("total number of entries in new {} data: {}".format(outlet, num_now))
        print("difference: {}".format(num_now - num_old))


# use example
# nyt_data = WebScraper.scrape_nyt()
# WebScraper.save_data("nyt", nyt_data)

