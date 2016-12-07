import importlib
import re
from app.channels.channel_base import *



def render_channel(class_name):
    module_name = '_'.join(re.findall('[A-Z][^A-Z]*', class_name)).lower()
    module = importlib.import_module('app.channels.' + module_name + '.' + module_name)

    return getattr(module, class_name)().render()


class NotFoundChannel(ChannelBase):

    def __init__(self, section_type):
        self.section_type = section_type
        super(NotFoundChannel, self).__init__()

    def render(self):
        return "No handler found for channel type %s" % self.section_type
