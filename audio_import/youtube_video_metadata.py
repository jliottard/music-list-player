class YouTubeVideoMetadata:
    """ Class describing video metadata """

    def __init__(self, video_id: int, url: str, title: str, author: str, duration: str, views: int, publication_date: str):
        self.id = video_id
        self.url = url
        self.title = title
        self.author = author
        self.duration = duration
        self.views = views
        self.publication_date = publication_date

    def __str__(self) -> str:
        return f"{self.id} {self.url} {self.title} {self.author} {self.duration}"
