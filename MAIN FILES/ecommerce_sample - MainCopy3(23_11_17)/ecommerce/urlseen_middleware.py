from scrapy import exceptions
import redis
from urlparse import urlparse

class URLSeenMiddleware(object):

    def __init__(self, redis_host, redis_port, max_depth):

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.max_depth = max_depth

        self.client = redis.StrictRedis(self.redis_host, self.redis_port)

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            redis_host = crawler.settings.get('REDIS_HOST'),
            redis_port = crawler.settings.get('REDIS_PORT'),
            max_depth =  crawler.settings.get('URL_SEEN_MAX_ALLOWED_DEPTH')
        )

    def process_request(self, request, spider):

        if 'depth' in request.meta and request.meta['depth'] > self.max_depth:

            url_tokens = urlparse(request.url)

            domain_key = 'domain:' + url_tokens.netloc

            if self.client.hexists(domain_key, request.url):
                raise exceptions.IgnoreRequest
            else:
                self.client.hset(domain_key, request.url, True)
