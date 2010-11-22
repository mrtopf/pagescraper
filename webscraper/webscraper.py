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
        self.image_processor = imageprocessor.ImageProcessor(self.filestore,None,'http://pagescraper.mrtopf.clprojects.net/images/')

    def process(self):
        data = urllib2.urlopen(self.url).read()
        print "read"
        try:
            tree = lxml.html.soupparser.fromstring(data)
        except:
            try:
                tree = lxml.etree.fromstring(data)
            except:
                return {'error' : 'could not parse document'}
        for p in finder.finders:
            f = p(tree, self.results, self.url)
            f.process()

        images = {}
        r = 0
        for url in self.results['all_image_urls']:
            res = self.image_processor.process(url)
            if res is not None:
                images[url] = res
                r=r+1
                if r>5: break
            else:
                print "problem with %s" %url
        self.results['images'] = images
        self.results['all_image_urls'] = images.keys()

        # now create images
        return self.results



if __name__ == '__main__':
    url = sys.argv[1]
    s = WebScraper(url)
    s.process()
