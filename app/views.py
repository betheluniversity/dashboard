import json

from flask.ext.classy import FlaskView, route
from flask import render_template, request
from flask import session

from app.controller import DashboardController

from app import app

class DashboardView(FlaskView):

    def __init__(self):
        self.base = DashboardController()
        pass

    def before_request(self, name, *args, **kwargs):
        """
        :param name: the name of the function that will be called
        :param args: Any arguments that will be passed to the view.
        :param kwargs: Any keyword arguments that will be passed to the view.
        """

    def index(self):
        title, tab_results = self.base.render_tab(1) # currently this is just using 1 as the id. later, this should use tab_order
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    @route('/tab/<tab_name>')
    def test(self, tab_name):
        title, tab_results = self.base.render_tab(tab_name)  # currently this is just using 1 as the id. later, this should use tab_order
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    # todo: remove this once testing is done
    def clear_db(self):
        self.base.db_controller.clear_db_generated_content()
        return 'done'

    def admin_view(self):
        tabs = self.base.get_tabs()
        options = tabs # used to make the select easy (Todo: should probably specifically import)
        tab_select = render_template('/snippets/select.html', **locals())

        column_formats = self.base.db_controller.get_column_formats_values()
        channels = self.base.db_controller.get_all_channels_values()

        return render_template('admin_base.html', **locals())

    # Todo: Limit the channels shown, based on size.
    # adds a new spot for a channel to be added
    @route('/admin/tool/add-channel', methods=['POST'])
    def admin_add_channel(self):
        id = 'test'
        select_class = 'choose-channel'
        options = self.base.db_controller.get_all_channels_values()
        channels = render_template('/snippets/select.html', **locals())

        return render_template('/snippets/add_channel.html', **locals())

    # adds a new format chooser and div
    @route('/admin/tool/add-row', methods=['POST'])
    def admin_add_row(self):
        id = 'test'
        select_class = 'choose-format'
        options = self.base.db_controller.get_column_formats_values()

        column_formats = render_template('/snippets/select.html', **locals())
        # currently it is initialized to the first in the list
        chosen_column_format = options[0]
        row_contents = render_template('/snippets/row_contents.html', **locals())

        return render_template('/snippets/add_row.html', **locals())

    # changes the format to the one provided
    @route('/admin/tool/change-format', methods=['POST'])
    def admin_change_format(self):
        chosen_column_format = request.form['selected_option']
        return render_template('/snippets/row_contents.html', **locals())
