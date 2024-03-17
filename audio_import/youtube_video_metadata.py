import datetime

class YouTubeVideoMetadata:
    """ Class describing video metadata """

    def __init__(self, video_id: int, link: str, title: str, author: str, duration: str, views: int, publish_date: str):
        self.id = video_id
        self.link = link
        self.title = title
        self.author = author
        self.duration = duration
        self.views = views
        self.publish_date = publish_date
