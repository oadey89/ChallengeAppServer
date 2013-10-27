import webapp2


class UploadChallenge(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
        <html>
            <body>
                <form action="/addChallenge" enctype="multipart/form-data" method="post">
                    image<div><input type="file" name="image"></div>
                    xml file<div><input type="file" name="challenge"></div>
                    <div><input type="submit" value="Upload!"></div>
                </form>
            </body>
        </html>""")


class UploadProfilePic(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
        <html>
            <body>
                <form action="/addProfilePic" enctype="multipart/form-data" method="post">
                    <div><input type="file" name="image"/></div>
                    <div><input type="text" name="user"/></div>
                    <div><input type="submit" value="Upload!"></div>
                </form>
            </body>
        </html>""")

