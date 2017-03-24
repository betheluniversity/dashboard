import json

from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect

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
        self.base.db_controller.create_new_user_if_new()
        return redirect('/', code=302)

    @route('/admin_view/', methods=['GET'])
    @route('/admin_view/<tab_order>', methods=['GET'])
    def admin_view(self, tab_order=1):
        tabs = self.base.get_tabs()
        tab_options = self.base.get_tabs(True)

        title, tab_results = self.base.render_tab(int(tab_order))
        if tab_results:
            rendered_tab = self.base.render_admin_tab(tab_results, title)
        else:
            rendered_tab = ''

        return render_template('admin_base.html', **locals())

    # adds a new spot for a channel to be added
    @route('/admin/tool/add-channel', methods=['POST'])
    def admin_add_channel(self):
        # zero based indexing for current_column_count and channel_id
        current_row_count = request.form['current_row_count']
        current_column_count = int(request.form['current_column_count']) - 1
        new_channel_count = int(request.form['new_channel_count']) - 1
        column_format = request.form['column_format']

        return self.base.render_add_channel(current_row_count, current_column_count, new_channel_count, column_format)

    @route('/admin/tool/new-tab', methods=['POST'])
    def admin_new_tab(self):
        row_id = request.form['row_id']

        return self.base.render_add_tab('', row_id)

    # adds a new format chooser and div
    @route('/admin/tool/add-row', methods=['POST'])
    def admin_add_row(self):
        row_id = request.form['row_id']

        return self.base.render_add_row(row_id)

    # changes the format to the one provided
    @route('/admin/tool/change-format', methods=['POST'])
    def admin_change_format(self):
        chosen_column_format = request.form['selected_option']
        return self.base.render_change_format(chosen_column_format)

    # changes the format to the one provided
    @route('/admin/submit-tab', methods=['POST'])
    def admin_submit_tab(self):
        rform = request.form
        return_url = "/admin_view/"

        if 'tab_id' in rform and rform['tab_id']:
            self.base.db_controller.delete_tab(rform['tab_id'])
            return_url += rform['tab_id']
        self.base.db_controller.create_new_tab(rform)
        return redirect(return_url, code=302)

    # changes the format to the one provided
    @route('/admin/submit-nav', methods=['POST'])
    def admin_submit_nav(self):
        rform = request.form
        new_nav_array = json.loads(rform['nav_order'])

        return str(self.base.db_controller.update_tab_order(new_nav_array))

    # todo: need to add a confirmation message
    # changes the format to the one provided
    @route('/admin/delete-tab', methods=['POST'])
    def admin_delete_tab(self):
        rform = request.form
        tab_id = rform['tab_id']

        return str(self.base.db_controller.delete_tab(tab_id))
