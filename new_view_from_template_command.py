import sublime
import sublime_plugin

import os.path

from sublime_lib.view_utils import new_view
from sublime_lib.collection_utils import projection
from sublime_lib import show_selection_panel

import yaml

def load_template(path):
    template = sublime.load_resource(path)

    i = template.find('\n---\n')
    ret = yaml.load(template[:i])
    contents = template[i+5:]

    if contents[-1] == '\n':
        contents = contents[:-1]

    ret['contents'] = contents
    ret.setdefault('name', os.path.splitext(os.path.basename(path))[0])
    ret.setdefault('description', path)

    return ret

class NewViewFromTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        show_selection_panel(
            self.window,
            [load_template(path) for path in sublime.find_resources('*.sublime-template')],
            labels=lambda template: (template['name'], template['description']),
            on_select=lambda template: self.create_view_from_template(
                **projection(template, {
                    'settings', 'syntax', 'scope', 'contents'
                })
            )
        )

    def create_view_from_template(self, *, contents, **kwargs):
        view = new_view(self.window, **kwargs)
        view.run_command('insert_snippet', {'contents': contents})
