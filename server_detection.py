import tornado.ioloop
import tornado.web
import base64
from tornado import gen

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("It's working!")

    @gen.coroutine
    def post(self):
        header_length = self.request.headers.get('Content-Length')
        image = base64.b64decode(self.request.body)

        if not header_length or len(image) != int(header_length): # failed
            print(len(image), header_Length)
            self.set_status(400)
            self.finish()
            return
        else: # all good
            self.set_status(200)
            self.finish()

        # pass images to openface server

        # save image
        with open("test_img.jpg", 'wb') as out_img:
            out_img.write(image)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7777)
    tornado.ioloop.IOLoop.current().start()
