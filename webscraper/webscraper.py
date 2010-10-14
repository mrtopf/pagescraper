import urllib2
import sys
import lxml.html.soupparser
import lxml.etree

import finder
import imageprocessor

import quantumcore.storages as storages                                                                                           

class WebScraper(object):
    """a class for scraping websites. It tries to find the title, 
    content and all the images. It stores everything in a dictionary
    with the key ``content``, ``all_image_urls`` and ``title``."""

    def __init__(self, url, image_dir="/tmp/"):
        """initialize the web scraper with a url"""
        self.url = url
        # TODO: error conditions
        self.results = {}
        self.filestore = storages.FilesystemStore(image_dir+"images", "%Y/%m/%d")
        self.image_processor = imageprocessor.ImageProcessor(self.filestore)

    def process(self):
        data = urllib2.urlopen(self.url).read()
        print "read"
        try:
            print 1
            tree = lxml.html.soupparser.fromstring(data)
        except:
            try:
                print 2
                tree = lxml.etree.fromstring(data)
            except:
                return {'error' : 'could not parse document'}
        print "ok"
        for p in finder.finders:
            f = p(tree, self.results, self.url)
            f.process()
        print self.results
        for url in self.results['all_image_urls']:
            print url
            print self.image_processor.process(url)

        # now create images
        return self.results



if __name__ == '__main__':
    url = sys.argv[1]
    s = WebScraper(url)
    s.process()
