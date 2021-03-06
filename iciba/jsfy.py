#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 金山翻译
# author by star
import sys
from workflow import Workflow,web
import urllib

api_url = "http://dict-co.iciba.com/api/dictionary.php"
app_key = "DB77106E3D56416869155B591C53C9C5"
ICON_DEFAULT = 'icon.png'
word = sys.argv[1]
en_word_flag = u"word"
zh_word_flag = u"chinese"
delimiter = "="

def getTransResult():
    url = api_url+"?w="+urllib.quote(word)+"&type=json&key="+app_key
    res = web.get(url)
    return res.json()

def genAlfred(data):
    if data.get('word_name') != None:
        if(data['symbols'][0]['parts'][0].get("part_name") != None):
            mp3 = ""
            #mean zh
            if data['symbols'][0]['symbol_mp3'] != "":
                mp3 = data['symbols'][0]['symbol_mp3']
            wf.add_item(
                title=u"拼音:[" + data['symbols'][0]['word_symbol'] + "]",
                subtitle=u"phonic for " + word.decode('utf-8') + "[by star]",
                arg=u""+zh_word_flag+delimiter+word.decode('utf-8')+delimiter+"拼音:[".decode('utf-8') + data['symbols'][0]['word_symbol'] + "]"+delimiter+mp3,
                valid=True,
                icon=ICON_DEFAULT)
            for part in data['symbols'][0]['parts'][0]['means']:
                cur_title = u""+part['word_mean']
                sub_title = u"zh for "  + word.decode('utf-8') + "[by star]"
                wf.add_item(
                    title=cur_title,
                    subtitle=sub_title,
                    arg=u""+zh_word_flag+delimiter+word.decode('utf-8')+delimiter+cur_title+delimiter+data['symbols'][0]['symbol_mp3'],
                    valid=True,
                    icon=ICON_DEFAULT)
        else:
            # mean en
            if data['symbols'][0]['ph_am'] != "":
                wf.add_item(
                    title=u"am:[" + data['symbols'][0]['ph_am'] + "] ,en:[" + data['symbols'][0]['ph_en'] + "]",
                    subtitle=u"phonic for " + word + "[by star]",
                    arg=u""+ en_word_flag +delimiter+data['word_name']+delimiter+"am:[" + data['symbols'][0]['ph_am'] + "] ,en:[" + data['symbols'][0]['ph_en'] + "]"+ delimiter + data['symbols'][0]['ph_am_mp3'],
                    valid=True,
                    icon=ICON_DEFAULT)
            for part in data['symbols'][0]['parts']:
                cur_title = u"" + part['part']
                cur_title = cur_title + ','.join(part['means'])
                sub_title = u"" + part['part'] + " for " + word + "[by star]"
                wf.add_item(
                    title=cur_title,
                    subtitle=sub_title,
                    arg=u""+en_word_flag+delimiter+data['word_name']+delimiter+cur_title + delimiter + data['symbols'][0]['ph_am_mp3'],
                    valid=True,
                    icon=ICON_DEFAULT)
    else:
        wf.add_item(title=u'error...',
                    subtitle=u"something has wrong...",
                    arg=word,
                    valid=True,
                    icon=ICON_DEFAULT)
    wf.send_feedback()

def main(wf):
    data = getTransResult()
    genAlfred(data)
    exit()

if __name__ == u"__main__":
    update_settings = {'version': '1.0.0','github_slug':'star1989/alfred_workflow'}
    wf = Workflow(update_settings=update_settings)
    sys.exit(wf.run(main))