# coding=utf-8
# Author: Dustyn Gibson <miigotu@gmail.com>
#
# URL: https://sickrage.github.io
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import datetime
import time

import sickbeard
from sickbeard import logger, tvcache
from sickbeard.common import cpu_presets
from sickbeard.indexers.indexer_config import INDEXER_TVDB
from sickbeard.bs4_parser import BS4Parser
from bs4 import BeautifulSoup
import re

from sickrage.helper.common import convert_size, try_int
from sickrage.providers.torrent.TorrentProvider import TorrentProvider

import StringIO
import pprint


class EZTVProvider(TorrentProvider):  # pylint: disable=too-many-instance-attributes

    def __init__(self):

        TorrentProvider.__init__(self, "EzTV")

        self.public = True
        self.minseed = None
        self.ranked = None
        self.sorting = None
        self.minleech = None
        self.token = None
        self.token_expires = None

        self.url = "https://eztv.ag/search/"
        self.urls = {"RSS": "https://eztv.ag/ezrss.xml"}

        # self.cache = tvcache.TVCache(self, min_time=20)  # only poll EZTV every 20 minutes max

    def yb_debug(self, obj, msg = ""):
        output = StringIO.StringIO()
        pprint.pprint(obj, stream=output)
        logger.log(msg + output.getvalue(), logger.INFO)
    
    def login(self):
        return True

    def get_rss(self):
        url = self.urls['RSS']
        data = self.get_url(url, returns='text')
        data = BeautifulSoup(data, 'html5lib')
        items = []
        for item in data('item'):
            
            title = item.title.text
            download_url = item.enclosure['url']
            if not (title and download_url):
                continue

            seeders = try_int(item.find('torrent:seeds').text)
            i_size = item.find('torrent:contentlength')
            torrent_size = i_size.text if i_size else -1
            size = convert_size(torrent_size) or -1
            
            i_hash = item.find('torrent:infohash')
            info_hash = i_hash.text if i_hash else item.infoHash
               
            i = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,  'hash': info_hash}
            #self.yb_debug(i, "rss item ")
            items.append(i)
        
        return items
        
     
    def search(self, search_strings, age=0, ep_obj=None):  # pylint: disable=too-many-branches, too-many-locals, too-many-statements
        results = []
        #self.yb_debug(search_strings)

        for mode in search_strings:
            #self.yb_debug(mode)
            items = []            
            if mode == 'RSS':
                items = self.get_rss()
            else: 
                #self.yb_debug(search_strings[mode][0], "0 ")
                
                url = self.url + search_strings[mode][0].replace(' ' , '-')
                #self.yb_debug(url, "url ")
                data = self.get_url(url)
                with BS4Parser(data, 'html5lib') as html:
                    torrent_lines = html.find_all('tr', attrs={"name" : 'hover'})
                    for tr in torrent_lines:
                        tds = tr.find_all('td')
                        
                        title = tds[1].find('a').string
                        all_as = tds[2].find_all('a')
                        # prefer using torrent than magnet links
                        if len(all_as) == 2:
                            t_link = all_as[1]['href']
                        else:
                            t_link = all_as[0]['href']
                            
                        size = tds[3].string
                        seeders = tds[5].string
                        item = {'title': title, 'link': t_link, 'size': size, 'seeders': seeders}
                        #self.yb_debug(item, "regular item ")
                        items.append(item)
                    
            
            results += items            
            
        return results;
	
provider = EZTVProvider()
