import sublime
import sublime_plugin

import os.path

from sublime_lib.util import create_view

import yaml

def load_template(path):
    template = sublime.load_resource(path)

    i = template.find('\n---\n')
    ret = yaml.load(template[:i])

    ret.setdefault('name', os.path.splitext(os.path.basename(path))[0])
    ret['text'] = template[i+5:]

    return ret

class NewViewFromTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        templates = [
            load_template(path)
            for path in sublime.find_resources('*.sublime-template')
        ]

        def callback(i):
            if i == -1: return
            self.create_view_from_template(**templates[i])

        self.window.show_quick_panel(
            [
                [ template['name'], template['description'] ]
                for template in templates
            ],
            callback
        )

    def create_view_from_template(self, name, description, text, **kwargs):
        view = create_view(self.window, **kwargs)
        view.run_command('insert_snippet', {'contents': text})
