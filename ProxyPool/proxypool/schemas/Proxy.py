from attr import attrs, attr

@attrs
class Proxy(object):
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)

    def __str__(self):
        return f"{self.host}:{self.port}"

    def string(self):
        return self.__str__()

# export 
# https_proxy=http://127.0.0.1:7890 
# http_proxy=http://127.0.0.1:7890 
# all_proxy=socks5://127.0.0.1:7890
if __name__ == "__main__":
    proxy = Proxy(host="8.8.8.8", port=7890)
    print("proxy: ", proxy)
    print("proxy: ", proxy.string())