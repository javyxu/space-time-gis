# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 16:02:14
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: download_agora.py
'''

from urllib import request as urllib2
import re
import os
from bs4 import BeautifulSoup

from spacetimegis.utils.logging_mixin import logger
from spacetimegis.constants import LogLevel
from spacetimegis.settings import get_celery_app
from spacetimegis import app

config = app.config
celery_app = get_celery_app(config)

def get_ty_links():
    logger.writelog(LogLevel.info, '======== start get typhoon links ========')
    years = []
    year_links = []
    for i in range(1979, 2018):
        years.append(str(i))
        year_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/year/wnp/' + str(i) + '.html.en')

    tys = []
    ty_links = []
    for i, year in enumerate(years):
        logger.writelog(LogLevel.info, 'search {0} years'.format(str(i)))
        try:
            html = urllib2.urlopen(year_links[i]).read()
        except Exception as e:
            logger.writelog(LogLevel.info, e)
            logger.writelog(LogLevel.error, e)
            continue
        
        soup = BeautifulSoup(html, "html.parser")
        row1 = soup.find_all(attrs={"class":"ROW1"})
        row0 = soup.find_all(attrs={"class":"ROW0"})
        number = len(row1) + len(row0)
        for j in range(1, 10):
            tys.append(year + '0' + str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/'+\
                            years[i] + '0' + str(j) + '.html.en')
        
        for j in range(10, number+1):
            tys.append(year + str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/'+\
                            years[i] + str(j) + '.html.en')
        logger.writelog(LogLevel.info, '{0} years search success.'.format(str(i)))
    
    return tys, ty_links

def download_imgs(path_, tys, ty_links):
    logger.writelog(LogLevel.info, '======= start download data =======')
    # path_ = os.path.abspath('.')
    root = path_ + '/tys_raw/'
    if not os.path.exists(root):
        os.mkdir(root)

    for i, ty_link in enumerate(ty_links):
    # for i in range(0, len(ty_links)):
        try:
            html = urllib2.urlopen(ty_link).read()
        except Exception as e:
            logger.writelog(LogLevel.error, e)
            continue
        
        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find_all('a')
        
        # all satellite images for every 6 hour
        for a in a_list:
            if (str(a.string)).strip() != 'Image':
                continue
            try:
                image_link = 'http://agora.ex.nii.ac.jp/'+ a['href']
                html_new = urllib2.urlopen(image_link).read()
                soup_new = BeautifulSoup(html_new,"html.parser")
                tr_list = soup_new.find_all('tr')
            except Exception as e:
                logger.writelog(LogLevel.error, e)
                continue

            boo = False
            wind = '0'
            for tr in tr_list:
                if (str(tr.string)).strip() == 'Maximum Wind':
                    tr_next = tr.next_sibling.next_sibling
                    if tr_next.string[0] == '0': # 0kt should be excluded
                        boo = True
                        break
                    wind = str(re.findall(r'\d+',tr_next.string))

            if boo: # 0kt should be excluded
                continue

            pressure = '1000'
            for tr in tr_list:
                if (str(tr.string)).strip() == 'Central Pressure':
                    tr_next = tr.next_sibling.next_sibling
                    pressure = str(re.findall(r'\d+',tr_next.string))

            lat = None
            for tr in tr_list:
                if (str(tr.string)).strip() == 'Latitude':
                    tr_next = tr.next_sibling.next_sibling
                    lat = str(re.findall(r'\d+',tr_next.string))
            
            lon = None
            for tr in tr_list:
                if (str(tr.string)).strip() == 'Longitude':
                    tr_next = tr.next_sibling.next_sibling
                    lon = str(re.findall(r'\d+',tr_next.string))
            
            pict_list = []
            anew_list = soup_new.find_all('a')
            for anew in anew_list: # find ir images
                if (str(anew.string)).strip() == 'Magnify this':
                    st = anew['href'].replace('/0/','/1/') # replace vis to ir
                    pict_list.append('http://agora.ex.nii.ac.jp'+ st)
            
            try: # save images
                s = pict_list[0].replace('/g/', '/1/')
                # filename : typhoon-number_time(YYMMDDHH)_wind_pressure.jpg
                filename = tys[i] + '_' + s[len(s)-19:len(s)-11] + '_' + lat + '_' + lon + '_' + wind + '_' + pressure
                filename = rename(filename)

                if os.path.exists(filename):
                    logger.writelog(LogLevel.info, filename + ' has been existed!')
                    continue

                with open(root + filename + '.jpg', 'wb') as f:
                    req = urllib2.urlopen(s)
                    buf = req.read()
                    f.write(buf)

            except Exception as e:
                logger.writelog(LogLevel.error, e)

        logger.writelog(LogLevel.info, tys[i] + ' has been downloaded.')

def rename(fname): # there maybe some unexcepted char in fname, drop them

    new_fname = fname.replace('[','')
    new_fname = new_fname.replace(']','')
    new_fname = new_fname.replace('u','')
    new_fname = new_fname.replace('\'','')
    new_fname = new_fname.replace(', ', '.')
    return new_fname

@celery_app.task(bind=True)
def download(self, path):
    ts, links = get_ty_links()
    task_id = download_imgs(path, ts, links)