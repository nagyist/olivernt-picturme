'''
Created on Nov 19, 2011

@author: arthurnn
'''
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.core.files.base import ContentFile

from StringIO import StringIO
import urllib,hashlib
from PIL import Image

from fivehundred import FiveHundredPx

from pixel.models import Pixel
from pixel.image2 import average_color,quantize_color


class Command(BaseCommand):
    help = "Cron job to fetch images"
    
    def handle(self, *args, **options):
        #t0 = datetime.datetime.now()
        
        api = FiveHundredPx(settings.PX_CONSUMER_KEY)
        
        iiter = api.get_photos(feature = args[0], limit=1000)
        
        for p in iiter:
            url = p['image_url']
            fileIm = urllib.urlopen(url)
        
            im = StringIO(fileIm.read())
            try:
                img = Image.open(im)
            except:
			    print 'problem featching image path: %s' % (url)
			    continue
            
            
            pixel = Pixel()
            
            pixel.url = 'http://500px.com/photo/%d' % p['id']
            
            filename = hashlib.md5(im.getvalue()).hexdigest()+'.jpg'
            pixel.image1.save(name=filename, content=ContentFile(im.getvalue()), save=False)
            
            
            color = (r,g,b) = average_color(img)
            (qr,qg,qb) = quantize_color(color)
            
            pixel.r=r
            pixel.g=g
            pixel.b=b
            
            pixel.qr=qr
            pixel.qg=qg
            pixel.qb=qb
            
            pixel.save()
                
        
        #self.stdout.write("Popular Looks reloaded, in %s" % delta_t)
