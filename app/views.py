import json

from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect

from app.controller import DashboardController

from app import app

# Overall Todos:
# 1) DONE - add number indexing to each row/column/channel. We need to use the 'name' attr to pass the fields along
# 2) DONE - use those numbers to create a tab in the DB
# 3) DONE - delete channels/rows
# 4) be able to set tab_order (maybe in the side nav, have arrows to move order up or down.
# 5) DONE - limit channels based on the size of the column
# 6) Edit a tab

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
        title, tab_results = self.base.render_tab(1)
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    @route('/tab/<tab_name>')
    def render_tab(self, tab_name):
        title, tab_results = self.base.render_tab(tab_name)
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    # todo: remove this once testing is done
    def clear_db(self):
        self.base.db_controller.clear_db_generated_content()
        self.base.db_controller.init_db()
        self.base.db_controller.create_new_user()
        return redirect('/', code=302)

    def admin_view(self):
        tabs = self.base.get_tabs()
        tab_options = self.base.get_tabs(True)
        # tab_select = render_template('/snippets/select.html', **locals())

        return render_template('admin_base.html', **locals())

    # adds a new spot for a channel to be added
    @route('/admin/tool/add-channel', methods=['POST'])
    def admin_add_channel(self):
        # zero based indexing for current_column_count and channel_id
        current_row_count = request.form['current_row_count']
        current_column_count = int(request.form['current_column_count']) - 1
        channel_id = int(request.form['channel_id']) - 1
        column_format = request.form['column_format']

        select_id = 'channel-%s-%s-%s' % (current_row_count, current_column_count, channel_id)
        select_class = 'choose-channel'

        # this is the minimum size a channel can be
        option_array = column_format.split('-')
        min_channel_size = int(option_array[current_column_count])

        # todo: make sure this options list only contains channels that fit the column_format
        all_channels = self.base.db_controller.get_all_channels_values()
        options = []
        # loop over options removing any that don't work
        for channel in all_channels:
            channel['min-size']
            if int(channel['min-size']) <= min_channel_size:
                options.append(channel)

        channels = render_template('/snippets/select.html', **locals())

        return render_template('/snippets/add_channel.html', **locals())

    # adds a new format chooser and div
    @route('/admin/tool/add-row', methods=['POST'])
    def admin_add_row(self):
        row_id = request.form['row_id']
        select_class = 'choose-format'
        select_id = 'columnformat-' + str(row_id)
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

    # changes the format to the one provided
    @route('/admin/submit-tab', methods=['POST'])
    def admin_submit_tab(self):

        rform = request.form

        self.base.db_controller.create_new_tab(rform)
        return redirect("/admin_view", code=302)
        # return render_template('admin_base.html', **locals())
