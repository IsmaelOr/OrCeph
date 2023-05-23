    def zoom_in(self):
        self.web_view.page().runJavaScript("document.getElementById('sizer').style.width = '1205px';")
        self.web_view.page().runJavaScript("document.getElementById('sizer').style.height = '5106px';")