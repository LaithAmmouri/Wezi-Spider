# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from urllib.parse import unquote
from scrapy.selector import HtmlXPathSelector


class WeziSpider(scrapy.Spider):
    name = 'wezi'
    allowed_domains = ['weziwezi.com']
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=أمراض_وعلاجات' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=تغذية' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=أدب' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=مطبخ_وأكلات' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=ديني' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=تدبير_منزلي' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=صحة_ورشاقة' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=جمال_وأزياء' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=حيوانات_ونباتات' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=دول' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=أمومة_وطفولة' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=آدم_وحواء' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=مسلسلات' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=أفلام' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=مال_وأعمال' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=قانون' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=تعليم' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=عالم_السيارات' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=علوم' % page for page in range(1, 100)]
    # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=فنون' % page for page in range(1, 100)]
    start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=معلومات_عامة' % page for page in range(1, 100)]


    def parse(self, response):

        articles = json.loads(response.text)['Articles']

        for article in articles:
            # Prepare article url:
            article_url = unquote(response.urljoin(article['url']))

            # Get article html response:
            html_response = HtmlXPathSelector(requests.get(article_url))

            # Select the article links, get the response, and save them in MongoDB:
            article_body = html_response.xpath('//*[@itemprop="articleBody"]')
            links = article_body.xpath('.//a')

            for link in links:
                link_href = link.xpath('.//@href')[0].extract()
                child_link_name = link.xpath('.//text()')[0].extract()
                if not link_href.startswith('#'):
                    if ("http" not in link_href) and ("https" not in link_href):
                        child_link = response.urljoin(link_href)
                        status = requests.get(child_link).status_code

                        if status != 200:
                            yield {'parent_article_url': article_url,
                                   'child_link': child_link,
                                   'child_link_name': child_link_name,
                                   'link_type': 'internal',
                                   'status': status}
                    else:
                        child_link = link.xpath('.//@href')[0].extract()
                        status = requests.get(child_link).status_code

                        if status != 200:
                            yield {'parent_article_url': article_url,
                                   'child_link': child_link,
                                   'child_link_name': child_link_name,
                                   'link_type': 'external',
                                   'status': status}














































# # -*- coding: utf-8 -*-
# import scrapy
# import requests
# from pprint import pprint
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy import signals
# import json
# from urllib.parse import unquote
# from scrapy.selector import HtmlXPathSelector
#
#
# class WeziSpider(scrapy.Spider):
#     name = 'wezi'
#     allowed_domains = ['weziwezi.com']
#     start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]=%s&rsargs[]=أمراض_وعلاجات' % page for page in range(1, 2)]
#                  # ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]={0}&rsargs[]={1}' % page for page in range(1, 100)]
#
#     # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]={0}&rsargs[]={1}'.format(page, category) for category in ['أمراض_وعلاجات', 'تغذية'] for page in range(1, 100)]
#     # start_urls = ['https://weziwezi.com/index.php?action=ajax&rs=JsonCategories&rsargs[]={0}&rsargs[]={1}'.format(page, category) for category in ['أمراض_وعلاجات'] for page in range(1, 100)]
#
#     # start_urls = ['https://weziwezi.com/%D8%A7%D8%B9%D8%B1%D8%A7%D8%B6-%D9%86%D9%82%D8%B5-%D9%81%D9%8A%D8%AA%D8%A7%D9%85%D9%8A%D9%86-%D9%83/']
#
#     # Set the HTTP error codes that should be handled
#     def parse(self, response):
#         articles = json.loads(response.text)['Articles']
#
#         for article in articles:
#             # Prepare article url:
#             article_url = unquote(response.urljoin(article['url']))
#
#             # Get article html response:
#             html_response = HtmlXPathSelector(requests.get(article_url))
#
#             # Select the article links, get the response, and save them in MongoDB:
#             article_body = html_response.xpath('//*[@itemprop="articleBody"]')
#             links = article_body.xpath('.//a/@href').extract()
#             filtered_links = filter(self.filter_links, links)
#             processed_links = self.process_links(filtered_links)
#
#             for processed_link in processed_links:
#                 if ("http" not in processed_link) and ("https" not in processed_link):
#                     processed_link = response.urljoin(processed_link)
#                     status = requests.get(processed_link).status_code
#
#                     if status != 200:
#                         yield {'parent_article_url': article_url,
#                                'child_link': processed_link,
#                                'link_type': 'internal',
#                                'status': requests.get(processed_link).status_code}
#                 else:
#                     status = requests.get(processed_link).status_code
#
#                     if status != 200:
#                         yield {'parent_article_url': article_url,
#                                'child_link': processed_link,
#                                'link_type': 'external',
#                                'status': requests.get(processed_link).status_code}
#
#     def filter_links(self, link):
#         if link.startswith('#'):
#             return False
#         else:
#             return True
#
#     def process_links(self, filtered_links):
#         processed_links = []
#
#         for filtered_link in filtered_links:
#             processed_links.append(filtered_link)
#
#         return processed_links
#
#
