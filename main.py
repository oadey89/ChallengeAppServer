import webapp2
import schema
import forms
from datetime import datetime
from google.appengine.ext import db
import xml.etree.ElementTree as ET
import logging as log


class AddUser(webapp2.RequestHandler):
    def get(self):
        x = self.request.get('user')
        if schema.User.gql("WHERE userName=:1", x).count() == 0:
            newUser = schema.User(userName=x, createdDate=datetime.now())
            newUser.put()
            self.response.write(1)
        else:
            self.response.write(0)


class AddProfilePic(webapp2.RequestHandler):
    def post(self):
        x = self.request.get('user')
        q = schema.User.gql("WHERE userName=:1", x)
        if q.count() == 0:
            self.response.write(0)
        else:
            image = self.request.get('image')
            for b in q:
                b.profilePic = db.Blob(image)
                b.put()
            self.response.write(1)


class AddChallenge(webapp2.RequestHandler):
    def post(self):
        chl = self.request.get('challenge')
        doc = ET.fromstring(chl)
        q = schema.User.gql("WHERE userName=:1", doc.find('creator').text)

        challenge = schema.Challenge(name=doc.find('name').text,
                                    description=doc.find('description').text,
                                    creator=q[0],
                                    createdDate=datetime.now(),
                                    startLocation=doc.find('startLocation').text,
                                    image=db.Blob(self.request.get('image')))

        log.info(chl)
        challenge.put()
        taskList = doc.findall('task')
        ii = 1
        for task in taskList:
            buildTask = schema.Task(description=task.find('description').text,
                                    sequenceNumber=ii,
                                    challengeLink=challenge)
            ii=ii+1
            buildTask.put()

            x = task.find('textEvidence')
            if x is not None:
                text = schema.TextValidation(textAnswer=x.text, taskLink=buildTask)
                text.put()

            y = task.find('timeEvidence')
            if y is not None:
                time = schema.TimeValidation(allowedTime=float(y.text), taskLink=buildTask)
                time.put()

            w = task.find('gpsEvidence')
            if w is not None:
                gpsList = w.split(',')
                gps = schema.GPSValidation(locationAnswer=gpsList[0] + ',' + gpsList[1],
                                           acceptedDist=float(gpsList[2]),
                                           taskLink=buildTask)
                gps.put()

            z = task.find('photoEvidence')
            if z is not None:
                img = schema.PhotoValidation(photoAnswer=db.Blob(self.request.get(z.text)),
                                             taskLink=buildTask)
                img.put()


class GetProfilePic(webapp2.RequestHandler):
    def get(self):
        x = self.request.get('user')
        q = schema.User.gql("WHERE userName=:1", x)
        q = list(q)
        self.response.headers['Content-Type'] = 'image/png'
        self.response.write(q[0].profilePic)


class ClearChallenges(webapp2.RequestHandler):
    def get(self):
        for u in schema.Challenge.all():
            u.delete()
        for v in schema.Task.all():
            v.delete()


class GetChallenges(webapp2.RequestHandler):
    def get(self):
        self.response.write('''
        <xml>
        ''')
        for u in schema.Challenge.all():
            tasks = ''
            response = ''
            qryString = "WHERE challengeLink = KEY('Challenge',%s)" % u.key().id()
            task_list = list(schema.Task.gql(qryString))
            task_list.sort(key = lambda t: t.sequenceNumber)
            for v in task_list:
                tasks += '''<task>
                    <id>%s</id>
                    <description>%s</description>
                    <sequenceNumber>%s</sequenceNumber>
                </task>''' % (v.key().id(), v.description, v.sequenceNumber)
            response += '''<challenge>
                <id>%s</id>
                <name>%s</name>
                <description>%s</description>
                <creator>%s</creator>
                <startLocation>%s</startLocation>
                %s
                </challenge>
            ''' % (u.key().id(), u.name, u.description, u.creator.userName, u.startLocation,tasks)
            self.response.write(response)
        self.response.write('</xml>')

class GetChallengePic(webapp2.RequestHandler):
    def get(self):
        x = self.request.get('id')
        qryString = "WHERE __key__ = KEY('Challenge',%s)" % x
        q = schema.Challenge.gql(qryString)
        self.response.headers['Content-Type'] = 'image/png'
        self.response.write(q[0].image)


class GetTaskPic(webapp2.RequestHandler):
    def get(self):
        x = self.request.get('id')
        qryString = "WHERE taskLink = KEY('Task',%s)" % x
        q = schema.PhotoValidation.gql(qryString)
        self.response.headers['Content-Type'] = 'image/png'
        self.response.write(q[0].photoAnswer)

app = webapp2.WSGIApplication([
    ('/clear', ClearChallenges),
    ('/addUser', AddUser),
    ('/addProfilePic', AddProfilePic),
    ('/uploadProfilePic', forms.UploadProfilePic),
    ('/profilePic', GetProfilePic),
    ('/uploadChallenge', forms.UploadChallenge),
    ('/addChallenge', AddChallenge),
    ('/getChallenges', GetChallenges),
    ('/challengePic', GetChallengePic),
    ('/taskPic', GetTaskPic)
], debug=True)
