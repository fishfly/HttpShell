import readline
import sys
import httplib
from ansicolors import colorize
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter


class HttpVerb(object):
    def __init__(self, connection, verb):
        self.connection = connection
        self.verb = verb

    def print_response_code(self, response):
        colors = ["grey", "green", "yellow", "red", "red"]

        print "{0} {1}".format(
            response.status,
            colorize(
                response.reason,
                colors[response.status / 100 - 1]))

    def print_headers(self, response):
        for header in response.getheaders():
            print "{0}: {1}".format(
                colorize(header[0], "yellow", "bright"),
                colorize(header[1], "white"))

    def print_data(self, response):
        data = response.read()

        print highlight(data,
            guess_lexer(data),
            TerminalFormatter())

    def run(self, args):
        path = args[0] if args else "/"
        self.connection.request(self.verb, path)
        return self.connection.getresponse()


class HttpHead(HttpVerb):
    def __init__(self, connection):
        super(HttpHead, self).__init__(connection, "HEAD")

    def run(self, args):
        response = super(HttpHead, self).run(args)
        self.print_response_code(response)
        self.print_headers(response)


class HttpGet(HttpVerb):
    def __init__(self, connection):
        super(HttpGet, self).__init__(connection, "GET")

    def run(self, args):
        response = super(HttpGet, self).run(args)
        self.print_response_code(response)
        self.print_headers(response)
        self.print_data(response)


class HttpShell(object):
    def __init__(self):
        self.map = {
             "head": self.head, "get": self.get,
             "post": self.post, "put": self.put,
             "delete": self.delete
        }

        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")

    def head(self, args):
        HttpHead(self.connect()).run(args)

    def get(self, args):
        HttpGet(self.connect()).run(args)

    def post(self, args):
        print "Not implemented."

    def put(self, args):
        print "Not implemented."

    def delete(self, args):
        print "Not implemented."

    def complete(self, text, state):
        commands = ["get", "post", "head", "delete"]
        matches = None

        if state == 0:
            if text:
                matches = [s for s in commands if s and s.startswith(text)]
            else:
                matches = commands[:]

        return matches[state]

    def connect(self):
        return httplib.HTTPConnection(self.host)

    def input(self):
        command = None

        while command != "quit":
            try:
                command = raw_input(self.host + "> ").split()
                args = command[1:] if len(command) > 1 else None
                self.map[command[0]](args)
            except EOFError:
                break

        self.connection.close()
        sys.exit(0)

shell = HttpShell()
shell.host = "catalog.lv3.hbogo.com"
shell.input()
# /apps/mediacatalog/rest/timeService/HBO/servertime
