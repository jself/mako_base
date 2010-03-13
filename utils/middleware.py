from johnny.cache import local
class LocalCache:
    def process_request(self,request):
        local['request'] = request

