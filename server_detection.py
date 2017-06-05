from __future__ import print_function

import sys
sys.path.append('openface_pi/demos')
import classifier
import tornado.ioloop
import tornado.web
import base64
from tornado import gen
import cStringIO
import cv2
import numpy
import time

get_curr = False
curr_score = 0

THRESHOLD_SCORE = 0.8

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        global get_curr
        global curr_score
        if get_curr == False:
            if curr_score >= THRESHOLD_SCORE:
                self.write('1')
            else:
                self.write('0')
            curr_score = 0
            get_curr = True
        else:
            self.write('0')
        return

    @gen.coroutine
    def post(self):
        header_length = self.request.headers.get('Content-Length')
        header_time = self.request.headers.get('time')
        image = self.request.body

        if not header_length or not image or len(self.request.body) != int(header_length): # something's wrong
            self.set_status(400)
            self.finish()
            return
        else: # send OK to client
            self.set_status(200)
            self.finish()

        # save image
        with open("curr.jpg", 'wb') as out_img:
            out_img.write(image)

        # convert image to cv2.image form
        image_string = cStringIO.StringIO(image)
        image_array = numpy.asarray( bytearray( image_string.read()), dtype=numpy.uint8)
        cv2image = cv2.imdecode( image_array, -1 )

        # get scores
        processing_time = time.time()
        scores = classifier.infer('./data/train/classifier.pkl', cv2image, True)
        processing_time = time.time() - processing_time

        # update score
        global curr_score
        global get_curr
        for score in scores:
            if curr_score < score:
                curr_score = score
                get_curr = False
        print(scores, 'delay:', time.time() - float(header_time), 'pct:', processing_time, curr_score)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7777)
    print('Server starts!')
    tornado.ioloop.IOLoop.current().start()
