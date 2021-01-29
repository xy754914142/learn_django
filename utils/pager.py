class PageInfo(object):
    def __init__(self,current_page,date_count,per_page,jump_url,show_page=11):
        """

        :param current_page: 当前页的序号
        :param date_count: 数据库中数据的总数
        :param per_page: 每页显示多少条数据
        :param jump_url:分页跳转的网页
        :param show_page:每页显示的分页个数
        """
        self.current_page = int(current_page)
        self.per_page = per_page
        self.show_page = show_page
        self.jump_url = jump_url
        a,b = divmod(date_count,per_page)
        if b:
            a+=1
        self.all_page = a

    def start(self):
        return(self.current_page-1)*self.per_page

    def end(self):
        return(self.current_page*self.per_page)

    def page(self):
        half = int((self.show_page-1)/2)
        #如果数据总页小于11
        if self.all_page < self.show_page:
            begin = 1
            stop = self.all_page + 1
        else:#如果当前页<=5 那么始终显示1-11
            if self.current_page<=5:
                begin = 1
                stop = self.show_page
            elif self.current_page + half > self.all_page:#当当前页+后面显示多少页 大于总页数时
                begin = self.all_page - 10
                stop = self.all_page + 1
            else:
                begin = self.current_page - half
                stop = self.current_page + half +1
        page_list = []
        home_page = "<li><a href='%s1.html'>首页</a></li>" % (self.jump_url)
        page_list.append(home_page)
        if self.current_page <= 1:
            prve = "<li><a href='#' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a>"
        else:
            prve = "<li><a href='%s%s.html' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a>"%(self.jump_url,self.current_page-1)
        page_list.append(prve)
        for i in range(begin,stop):
            if i == self.current_page:
                temp = "<li class='active'><a href='%s%s.html'>%s</a></li>" % (self.jump_url,i, i)
            else:
                temp="<li><a href='%s%s.html'>%s</a></li>"%(self.jump_url,i,i)
            page_list.append(temp)
        if self.current_page >= self.all_page:
            nex = "<li><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a>"
        else:
            nex = "<li><a href='%s%s.html' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a>"%(self.jump_url,self.current_page+1)
        page_list.append(nex)
        trailer_page = "<li><a href='%s%s.html'>末页</a></li>" % (self.jump_url,self.all_page)
        page_list.append(trailer_page)
        return ''.join(page_list)

