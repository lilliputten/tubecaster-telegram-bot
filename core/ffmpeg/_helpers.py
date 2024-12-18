class Error(Exception):
    def __init__(self, cmd, stdout, stderr):
        super(Error, self).__init__('{} error (see stderr output for detail)'.format(cmd))
        self.stdout = stdout
        self.stderr = stderr


def convertKwargsToCmdLineArgs(kwargs):
    """Helper function to build command line arguments out of dict."""
    args = []
    for k in sorted(kwargs.keys()):
        v = kwargs[k]
        args.append('-{}'.format(k))
        if v is not None:
            args.append('{}'.format(v))
    return args
