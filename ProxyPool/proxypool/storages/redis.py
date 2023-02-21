import redis
import random
from proxypool.exceptions.empty import PoolEmptyException
from proxypool.schemas.Proxy import Proxy
from proxypool.setting import REDIS_CONNECTION_STRING, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, \
    REDIS_DB, REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN, PROXY_SCORE_INIT
from typing import List
from loguru import logger
from proxypool.utils.proxy import is_valid_proxy, convert_proxy_or_proxies


REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.starswith("2.")

class RedisClinet(object):
    """
    redis connection client of proxypool
    """
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB,
                    connection_string=REDIS_CONNECTION_STRING, **kwargs):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        :param connection_string: redis connection_string
        """
        if connection_string:
            self.db = redis.StrictRedis.from_url(connection_string, decode_responses=True, **kwargs)
        else:
            self.db = redis.StrictRedis(
                host=host, port=port, password=password, db=db, decode_responses=True, **kwargs
            )
    
    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> Int:
        """
        add proxy and set it to init score
        :param proxy: proxy, ip:port, like 8.8.8.8:88
        :param score: int score
        :return: result
        """
        if not is_valid_proxy(f"{proxy.host}:{proxy.port}"):
            logger.info(f"invalid proxy {proxy}, throw it")
            return 
        if not self.exists(proxy):
            # different kind of redis version 
            if IS_REDIS_VERSION_2:
                return self.db.zadd(REDIS_KEY, score, proxy.string())
            return self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def exists(self, proxy: Proxy) -> bool:
        """
        if proxy exists
        :param proxy: proxy
        :return: is exists, bool
        """
        return not self.db.zscore(REDIS_KEY, proxy.string()) is None
    
    def random(self) -> Proxy:
        """
        get random proxy
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:88
        """
        proxies = self.db.zrangebyscore(
            REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX
        )
        if len(proxies):
            return  convert_proxy_or_proxies(random.choice(proxies))
        # else get proxy by rank
        proxies = self.db.zrevrange(
            REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX
        )
        if len(proxies):
            return convert_proxy_or_proxies(random.choice(proxies))
        raise PoolEmptyException
    
    def decrease(self, proxy: Proxy) -> int:
        if IS_REDIS_VERSION_2:
            self.db.zincrby(REDIS_KEY, proxy.strign(), -1)
        else:
            self.db.zincrby(REDIS_KEY, -1, proxy.string())
        score = self.db.zscore(REDIS_KEY, proxy.string())
        logger.info(f"{proxy.string()} current score {score}, remove")
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{proxy.string()} current score {score}, remove')
            self.db.zrem(REDIS_KEY, proxy.string())
        
    def max(self, proxy: Proxy) -> int:
        logger.info(f'{proxy.string()} is valid, set to {PROXY_SCORE_MAX}')
        if IS_REDIS_VERSION_2:
            return self.db.zadd(REDIS_KEY, PROXY_SCORE_MAX, proxy.string())
        return self.db.zadd(REDIS_KEY, {proxy.string(): PROXY_SCORE_MAX})
    
    def count(self) -> int:
        return self.db.zcard(REDIS_KEY)
    
    def all(self) -> List[Proxy]:
        return convert_proxy_or_proxies(self.db.zremrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX))

    def batch(self, cursor, count) -> List[Proxy]:
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, convert_proxy_or_proxies([i[0] for i in proxies])


if __name__ == "__main__":
    conn = RedisClinet()
    result = conn.random()
    print(result)
