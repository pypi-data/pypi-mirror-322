from html.parser import HTMLParser
from .function20 import Fonted
#===========================================================================

class Txtformat(HTMLParser):

    def __init__(self, code=None):
        super().__init__()
        self.result = []
        self.codes = code
    
    def handle_starttag(self, tag, attrs):
        if attrs:
            aing = " ".join(f"{name}='{value}'" for name, value in attrs)
            self.result.append(f"<{tag} {aing}>")
        else:
            self.result.append(f"<{tag}>")
    
    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")
    
    def handle_data(self, data):
        formatted_data = Fonted(self.codes, data)
        self.result.append(formatted_data)
    
    def format_text(self, text):
        self.result = []
        self.feed(text)
        return ''.join(self.result)

#===========================================================================
