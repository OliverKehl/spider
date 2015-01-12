import urllib2
import crawlers.chazidian
import config
def crawl(file):
    f = open(file,'r')
    for line in f.readlines():
        url = 'http://www.chazidian.com/ci/?q='+line
        req = urllib2.urlopen(url)
        response = req.read()
        
        #page jump
        offset =  response.find('title=\"'+ line +'\">')
        target_url = response[(offset-65):(offset-2)]
        req = urllib2.urlopen(target_url)
        response = req.read()
        print response
if __name__=='__main__':
    print config.sqlalchemy_zidian_url
        