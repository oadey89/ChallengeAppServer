__author__ = 'Oliver'
from google.appengine.ext import db

class User(db.Model):
    userName = db.StringProperty()
    createdDate = db.DateTimeProperty()
    kudosBalance = db.IntegerProperty(default=0)
    kudosRevenue = db.IntegerProperty(default=0)
    profilePic = db.BlobProperty()

    def __unicode__(self):
        return self.userName

class Challenge(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    image = db.BlobProperty()
    startLocation = db.GeoPtProperty()
    creator = db.ReferenceProperty(reference_class=User)
    createdDate = db.DateTimeProperty()
    #firstSuccessUser = db.ReferenceProperty(reference_class=User)
    #fastestSuccessUser = db.Reference(reference_class=User)
    #fastestSuccess = db.FloatProperty()

    def __unicode__(self):
        return self.name


class Task(db.Model):
    description = db.TextProperty()
    challengeLink = db.Reference(reference_class=Challenge)
    sequenceNumber = db.IntegerProperty()

    def __unicode__(self):
        return self.name


class GPSValidation(db.Model):
    taskLink = db.ReferenceProperty(reference_class=Task)
    locationAnswer = db.GeoPtProperty()
    #accepted distance from answer in metres
    acceptedDist = db.FloatProperty()


class TextValidation(db.Model):
    taskLink = db.ReferenceProperty(reference_class=Task)
    textAnswer = db.StringProperty()


class TimeValidation(db.Model):
    taskLink = db.ReferenceProperty(reference_class=Task)
    #allowed time for task start to completion in seconds
    allowedTime = db.FloatProperty()

class PhotoValidation(db.Model):
    taskLink = db.ReferenceProperty(reference_class=Task)
    photoAnswer = db.BlobProperty()

class PhotoSubmissions(db.Model):
    userLink = db.ReferenceProperty(reference_class=User)
    taskLink = db.ReferenceProperty(reference_class=Task)
    photoSubmission = db.BlobProperty()
    submissionTime = db.DateTimeProperty()
    validatedBool = db.BooleanProperty()
    validationTime = db.DateTimeProperty()
    #validationUser = db.ReferenceProperty(reference_class=User)













