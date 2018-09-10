import sys


class App():
    def __init__(self, init="", args=[], demo=[]):
        self.init = init
        self.demo = [[sys.argv[0], e] for e in demo]
        self.parse(args)

    def parse(self, args):
        names = {}
        self.args = []
        self.argx = {}
        for arg in args:
            name = arg[1].replace('-', '')
            names[arg[0]] = name
            names[arg[1]] = name
            self.argx[name] = None
            self.args.append(["{0}, {1} ".format(arg[0], arg[1]), arg[2]])
            [self.args.append(['', line]) for line in arg[3:]]

        argv = [names[i] if i in names else i for i in sys.argv]

        if len(argv) <= 1:
            self.exit('Kio okazas? (Specify arguments. Please)')

        if argv[1] == 'help':
            self.exit()

        first = -1 * len(argv) % 2
        for i in range(0, len(argv) - 1, 2):
            k, v = [argv[i + first], argv[i + first + 1]]
            if k in self.argx:
                self.argx[k] = v

    def echo(self, text, color=""):
        sys.stderr.write({
          '': "{0}",
          'red': "\033[31m{0}\033[0m",
          'green': "\033[32m{0}\033[0m",
          'white': "\033[37m{0}\033[0m",
          'red_bold': "\033[1;31m{0}\033[0m",
          'green_bold': "\033[1;32m{0}\033[0m"
        }[color].format(text))

    def log(self, text, prefix='    '):
        self.echo(prefix + text + '\n', 'green')

    def error_log(self, text, prefix='[-] '):
        self.echo(prefix, 'red_bold')
        self.echo(text + '\n', 'red')

    def success_log(self, text, prefix='[+] '):
        self.echo(prefix, 'green_bold')
        self.echo(text + '\n', 'green')

    def params(self, items):
        space = max([len(name) for name, desc in items]) + 1
        for name, desc in items:
            name += ' ' * (space - len(name))
            self.echo('  ' + name, 'green_bold')
            self.echo(desc + '\n', 'green')
        self.echo('\n')

    def default(self, name, value):
        if name not in self.argx:
            self.argx[name] = value
        if self.argx[name] is None:
            self.argx[name] = value

    def exit(self, cause=False):
        if cause is not False:
            self.echo('Error:\n', 'red')
            self.echo('  ' + cause + '\n\n', 'red_bold')

        if self.init is not "":
            self.echo('Usage:\n', 'white')
            self.params([[sys.argv[0], self.init]])

        if len(self.args) > 0:
            self.echo('Optional arguments:\n', 'white')
            self.params(self.args)

        if len(self.demo) > 0:
            self.echo('Examples:\n', 'white')
            self.params(self.demo)

        sys.exit(1 if cause else 0)
