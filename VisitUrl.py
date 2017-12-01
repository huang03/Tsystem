from urllib import request,parse,error
class VisitUrl:
    '''
    # https://www.cnblogs.com/Lands-ljk/p/5447127.html
    urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
        url:  需要打开的网址
        data：Post提交的数据
        timeout：设置网站的访问超时时间
    urlopen（）的data参数默认为None，当data参数不为空的时候，urlopen（）提交方式为Post。
    urlopen返回对象提供方法：

    read() , readline() ,readlines() , fileno() , close() ：对HTTPResponse类型数据进行操作
    info()：返回HTTPMessage对象，表示远程服务器返回的头信息
    getcode()：返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
    geturl()：返回请求的url
    '''
    def __init__(self,header=None):
        self._error = None
        self._response = None
        self._status = None
        if header is None:
            self.headers = {
                'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
                'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
                'Connection': 'keep-alive'
            }
        else:
            self.headers = header


    # def getR
    def getRequest(self,url):
        if not self._checkUrl(url):
            return False
        req = request.Request(url,headers=self.headers)
        try:

            response = request.urlopen(req)
            self._setResponse(response)
            self._setStatus(response.code)
            return True
            # print(response.code)
            # page = response.read()
            # page = page.decode('utf-8')
            # response.close()
            # return page
        except error.HTTPError as e:
            # print(e.code)
            # print(self.response)

            self._dealException(e)
            # print(e.code())
            # print(e.read().decode('utf-8'))
            # self._setError(e.read().decode('utf-8'))
            # self._setResponse(None)
            return False
        pass

    def postRequest(self,url,data):

        if not self._checkUrl(url):
            return False
        if type(data) != dict or len(data)<1:
            self._setError('Data can not be empty')
            return False
        # Post的数据必须是bytes或者iterable of bytes，不能是str，因此需要进行encode（）编码
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=data, headers=self.headers)
        try:
            response = request.urlopen(req)
            self._setResponse(response)
            self._setStatus(response.code)
            # page = response.read()

            # page = page.decode('utf-8')
            # response.close()
            # return page
        except error.HTTPError as e:
            self._dealException(e)
            # print(e.code())
            # self._setError(e.read().decode('utf-8'))
            # print(e.read().decode('utf-8'))
            return False
        pass
    #代理
    def proxy(self,url,data):
        proxy = request.ProxyHandler({})
        opener = request.build_opener(proxy)
        request.install_opener(opener)
        data = parse.urlencode(data).encode('utf-8')
        page = opener.open(url, data).read()
        page = page.decode('utf-8')
        return page
    def _checkUrl(self,url):
        if url == '' or  type(url) != str:
            self._setError('url is illegal')
            return False
        return True
    def getError(self):
        return self._error
    def _setError(self,error):
        self._error = error

    def getResponse(self):
        return self._response
    def _setResponse(self,response):
        self._response = response
    def getContent(self):
        if self._response is None:
            return None
        # print(response.code)
        content = self._response.read()
        content = content.decode('utf-8')
        self._response.close()
        self._setResponse(None)
        return content
    def _dealException(self,E):
        self._setStatus(E.code)
        self._setStatus(E.code)
        # print(E.__dict__)
        # self._setError(E.read().decode('utf-8'))
        self._setError('%d %s' %(E.code,E.msg))
        self._setResponse(None)
    def getStatus(self):
        return self._status
    def _setStatus(self,code):
        self._status = code