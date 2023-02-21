class PoolEmptyException(Exception):
    def __str__(self):
        return repr("no proxy in proxypool!")