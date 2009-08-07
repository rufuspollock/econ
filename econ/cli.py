#!/usr/bin/env python

import cmd

class EconAdmin(cmd.Cmd):

    prompt = 'econ-admin > '

    def __init__(self):
        cmd.Cmd.__init__(self) # cmd.Cmd is not a new style class
        import econ
        # TODO: this should be set via a cli option
        econ.register_config('development.ini')

    def run_interactive(self, line=None):
        """Run an interactive session.
        """
        print 'Welcome to econ-admin interactive mode\n'
        self.do_about()
        print 'Type:  "?" or "help" for help on commands.\n'
        while 1:
            try:
                self.cmdloop()
                break
            except KeyboardInterrupt:
                raise

    def do_help(self, line=None):
        cmd.Cmd.do_help(self, line)

    def do_about(self, line=None):
        import econ
        version = econ.__version__
        about = \
'''Open Econ version %s. Copyright the Open Knowledge Foundation.
Open Econ is open-knowledge and open-source. See LICENSE.txt for details.
''' % version
        print about

    def do_quit(self, line=None):
        sys.exit()

    def do_EOF(self, *args):
        print ''
        sys.exit()

    # --------------
    # start commands

    def do_store_index(self, line=None):
        import econ.store
        if line:
            basePath = line
        else:
            basePath = econ.get_config()['data_store_path']
        indexList = econ.store.make_index(basePath)
        for item in indexList.list():
            print item.name
            print '  Title: ', item.metadata['title']
            print
        # for key, item in indexList.items():
        #    print str(item) + '\n'

    def help_store_index(self, line=None):
        usage = \
'''store_index <store-path>

Print an index of the data store located at <store-path>. If <store-path> not
supplied then use data_store_path specified in config.'''
        print usage

    def do_runserver(self, line=None):
        self.help_runserver()

    def help_runserver(self, line=None):
        usage = \
'''To run a web server to provide a web user interface to the econ package use::

  paster serve <config-file-name>

To generate a configuration file do::

  paster make-config <config-file-name>
'''
        print usage

    def do_bundle(self, line=None):
        args = []
        if line:
            args = line.split()
        import econ
        if args and args[0] == 'make': # default
            args = line.split() 
            if len(args) > 1:
                path = args[1]
            else:
                store_path = econ.get_config()['data_store_path']
                path = store_path
            import econ.store.bundle
            bndl = econ.store.bundle.create(path)
            print 'Created new data bundle %s at %s' % (bndl.id, bndl.path)
        elif args and args[0] == 'show':
            id = args[1]
            import econ.store
            index = econ.store.index()
            print index[id]
        else:
            print 'Unknown argument: %s' % line
            self.help_bundle()

    def help_bundle(self, line=None):
        usage = \
'''Do things with data bundles.

  1. bundle make [path]

     make: create a new data empty data bundle at path. If path not provided
     create the bundle in the default data store (as specified in the config
     file).

  2. bundle show id

     Show information on bundle with 'id' id. The bundle will be located in the
     data store specified in the configuration file.
'''
        print usage


def main():
    import optparse
    usage = \
'''%prog [options] <command>

Run about or help for details.'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-v', '--verbose', dest='verbose', help='Be verbose',
            action='store_true', default=False) 
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        return 1
    else:
        cmd = EconAdmin()
        args = ' '.join(args)
        cmd.onecmd(args)

