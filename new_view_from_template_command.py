import sublime
import sublime_plugin

import os.path

from sublime_lib.util import create_view

import yaml

def load_template(path):
    template = sublime.load_resource(path)

    i = template.find('\n---\n')
    ret = yaml.load(template[:i])
    text = template[i+5:]

    if text[-1] == '\n':
        text = text[:-1]

    ret['text'] = text
    ret.setdefault('name', os.path.splitext(os.path.basename(path))[0])
    ret.setdefault('description', path)

    return ret

class NewViewFromTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        templates = [
            load_template(path)
            for path in sublime.find_resources('*.sublime-template')
        ]

        def callback(i):
            if i == -1: return
            self.create_view_from_template(
                text=templates[i]['text'],
                settings=templates[i].get('settings', None)
            )

        self.window.show_quick_panel(
            [
                [ template['name'], template['description'] ]
                for template in templates
            ],
            callback
        )

    def create_view_from_template(self, *, text, settings=None):
        view = create_view(self.window, settings=settings)
        view.run_command('insert_snippet', {'contents': text})
