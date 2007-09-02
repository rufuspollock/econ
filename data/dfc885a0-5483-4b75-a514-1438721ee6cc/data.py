'''Download article statistics from econlit.

Note econlit is *not* open and you need set a username/password in the code
below for the data extraction to work.
'''
import urllib

baseurl = \
'http://www.econlit.org/vivisimo/cgi-bin/query-meta?input-form=advanced&query=&v%3Asources=journal&num=100&v%3Aproject=econlit&author=&title=&so=&subjdesc=&year=' 

# http://www.econlit.org/vivisimo/cgi-bin/query-meta?input-form=advanced&query=&v%3Asources=journal&num=200&v%3Aproject=econlit&author=&title=&so=&subjdesc=&year=1970&yearmin=&yearmax=#list-stats

import urllib2
base_auth_url = 'http://www.econlit.org/vivisimo/cgi-bin/query-meta'
# set your username here
username = 'USERNAME_HERE'
password = 'PASSWORD_HERE'

def setup_auth():
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, base_auth_url, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    # print passman.find_user_password('EconLit', baseurl)
    # print passman.find_user_password('EconLit', baseurl + '1970')

def setup_auth_2():
    # set up authentication info
    authinfo = urllib2.HTTPBasicAuthHandler()
    authinfo.add_password('EconLit', 'www.econlit.org/', username, password)
    # build a new opener that adds authentication and caching FTP handlers
    opener = urllib2.build_opener(None, authinfo, urllib2.CacheFTPHandler)
    # install it
    urllib2.install_opener(opener)
    print authinfo.find_user_password('EconLit', baseurl)

def extract_stat(html):
    import re
    regex = r'at least\n.*>(.*)<.+\n\s*retrieved for the query'
    matches = re.findall(regex, html)
    # assert len(matches) == 1
    total = matches[0].replace(',', '')
    return int(total)

def get_data(year):
    url = baseurl + str(year)
    out = urllib2.urlopen(url)
    html = out.read()
    out = extract_stat(html) 
    return out

def get_all_data():
    from time import sleep
    results = []
    years = range(1970, 2007)
    for year in years:
        out = get_data(year)
        print year, out
        results.append(out)
        sleep(1)
    return years, results

def test_1():
    setup_auth()
    out = get_data(1970)
    assert out == 5081

if __name__ == '__main__':
    setup_auth()
    # get_data(1970)
    years, results = get_all_data()
    out = zip(years, results)
    print out
