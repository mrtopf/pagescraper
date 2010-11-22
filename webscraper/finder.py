import urlparse

###
### find text
###

class Finder(object):

    def __init__(self, tree, result, url):
        """initialize the finder object"""
        self.tree = tree
        self.result = result
        self.url = url

class ImageFinder(Finder):

    def process(self):
        imgs = self.tree.findall(".//img")
        urls = []
        for img in imgs:
            rel_url = img.get("src")
            urls.append(urlparse.urljoin(self.url, rel_url))
        self.result['all_image_urls'] = urls

class TitleFinder(Finder):
    
    def process(self):
        title = self.tree.find(".//title")
        if title is None:
            title = self.tree.find(".//h1")
        if title is None:
            self.result['title'] = u""
            return 
        text = title.text
        if text is not None:
            self.result['title'] = title.text.strip()
            return
        self.result['title'] = u""

class TextFinder(Finder):
    MAX_WORDS = 30

    def process(self):
        text = self.find_text_in_content(self.tree)
        if text is not None:
            t = text.split()
            if len(t)>self.MAX_WORDS:
                text = " ".join(t[:self.MAX_WORDS])+"..."
        if text is not None:
            self.result['content'] = text
            return
        text = self.find_text_in_p(self.tree)
        if text is not None:
            t = text.split()
            if len(t)>self.MAX_WORDS:
                text = " ".join(t[:self.MAX_WORDS])+"..."
        if text is not None:
            self.result['content'] = text
            return
        self.result['content'] = u""

    def find_text_in_p(self, el):
        """search all <p> and extract their content"""

        all = []
        for el in el.findall(".//p"):
            t = el.text_content().strip()
            if len(t)<40:
                continue
            all.append(t)

        return " ".join(all)

    def find_text_in_content(self, el):
        """try to obtain some content div and extract text from there"""
        try:
            content_divs = [el.get_element_by_id("content")]
        except KeyError:
            # try class
            content_divs = el.find_class("content")

        if content_divs == []:
            return None
        
        # iterate over divs and extract text
        all = []
        for div in content_divs:
            r = self.find_text_in_p(div)
            all.append(r)
        return " ".join(all)

finders  = [TitleFinder, TextFinder, ImageFinder]
