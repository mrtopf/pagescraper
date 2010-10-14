import urllib2
import uuid
import os
import tempfile
import quantumcore.media.image

class ImageProcessor(object):
    """an image processor for downscaling and storing images"""

    DEFAULT_SPEC = {
        "thumb" : {'width':100},
        "small" : {'width':123, 'height':82},
        "medium" : {'width':270,'height':180},
        "big" : {'width':500},
        "squared" : { 'square' : 100}
    }

    def __init__(self, filestore, spec=None):
        """initialize the image processor with a file storage and a specification 
        on how to scale images. 

        ``filestore`` is an object implementing a ``quantumcore.resources`` file
        storage.
        
        This ``spec`` is a dictionary like this::

            {
                "thumb" : {'width';100},
                "small" : {'width':123, 'height';82},
                "medium" : {'width':270,'height':180},
                "big" : {'width':500},
                "squared" : { 'square' : 100)
            }
       
        if a ``width`` only is given, then this width is fixed and the height
        adjusted accordingly. The same goes for a single ``height`` attribute. If 
        both are given, then the biggest version wins. If ``squared`` is given,
        then the image is first scaled and then cropped to make it square.
        """
        
        if spec is None:
            self.spec = self.DEFAULT_SPEC
        else:
            self.spec = spec
        self.filestore = filestore

    def process(self, url):
        """process an image identified by a URL. It creates all the scales
        and stores them inside the file storage. It returns a dictionary with all
        the created scales like this::

            {
                "<name>" : {'filename' "/images/....", 'width': 60, 'height' : 70},
            }

        Note, that it also contains a key ``_original`` pointing to the original
        image and size.

        """
        # TODO: error conditions, e.g. content type testing etc.
        filename = unicode(uuid.uuid4())
        image = urllib2.urlopen(url)
        filename = self.filestore.add(image.fp, filename)
        image.close()
        
        file = self.filestore[filename] # retrieve the file pointer
        img = quantumcore.media.image.Image(file)

        result = {
            '_original' : {
                    'filename' : filename,
                    'width' : img.image.size[0],
                    'height' : img.image.size[1]
                }
        }
        for name, spec in self.spec.items():
            if spec.has_key("square"):
                x = spec['square']
                img2 = img.fit(x,x).sharpen()
            else:
                img2 = img.scale(**spec)
                
            fno, tmpfilename = tempfile.mkstemp()
            
            # now save the file and store it in the file store
            # unfortunately PIL does not give us an fp (I think)
            img2.image.save(tmpfilename, "PNG")
            fp = open(tmpfilename, "rb")
            tfilename = self.filestore.add(fp, filename)
            fp.close()
            os.close(fno)
            os.remove(tmpfilename)
            
            entry = {'filename': tfilename, 'width': img2.image.size[0], 'height': img2.image.size[1]}
            result[name] = entry
        return result


