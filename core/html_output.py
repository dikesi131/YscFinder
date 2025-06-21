import os
import sys
import subprocess
import webbrowser
from argparse import Namespace


class HtmlOutput:
    def __init__(self, template: str, args: Namespace):
        self.template = template
        self.args = args

    def save(self, output: str):
        ''' Save the output to an HTML file and open it in a web browser.
        Args:
            output (str): The content to be saved in the HTML file.
        '''
        hide = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            text_file = open(self.args.output, "wb")
            text_file.write(self.template.replace('$$content$$',
                                                  output).encode('utf-8'))
            text_file.close()

            print('URL to access output: file://%s' % os.path.abspath(self.args.output))  # noqa
            file = 'file:///%s' % (os.path.abspath(self.args.output))
            if sys.platform == 'linux' or sys.platform == 'linux2':
                subprocess.call(['xdg-open', file])
            else:
                webbrowser.open(file)
        except Exception as err:
            print('Output can\'t be saved in %s due to exception: %s' % (self.args.output, err))  # noqa
        finally:
            os.dup2(hide, 1)
