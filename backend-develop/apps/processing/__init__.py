import redis
import logging
logger = logging.getLogger(__file__)

publisher = redis.Redis(host = '192.168.0.114', port = 6379)