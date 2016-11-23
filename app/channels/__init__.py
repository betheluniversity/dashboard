import importlib
from app.channels.channel_base import *


def get_section(section):

    section_type = section.find('channel-type').text

    if section_type == 'Text':
        from app.channels.cascade_content_channel.cascade_content import TextSection
        channel = TextSection(section)
        return channel

    elif section_type == 'RSS':
        from app.channels.rss_channel.rss_channel import RSSChannel
        channel = RSSChannel(section)
        return channel

    elif section_type == 'Python Class':
        clspath = section.find('python-class/python-class').text
        module_name, class_name = clspath.rsplit(".", 1)

        module = importlib.import_module(module_name)

        return getattr(module, class_name)()

    else:
        return NotFoundChannel(section_type)


class NotFoundChannel(ChannelBase):

    def __init__(self, section_type):
        self.section_type = section_type
        super(NotFoundChannel, self).__init__()

    def render(self):
        return "No handler found for channel type %s" % self.section_type
