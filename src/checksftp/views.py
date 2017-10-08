import re
import socket

from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/index.mak')
def on_page_load(request):
    return {'project': 'checksftp'}

@view_config(route_name='runthecheck', renderer='json')
def on_run_check(request):

    try:

        #import pdb;pdb.set_trace()

        host = request.GET['host']
        port = int(request.GET['port'])

        trace = False
        if 'trace' in request.GET and request.GET['trace']:
            trace = True

        sct = sftp_conn_tester(host, port, trace)

        return sct.test_basic_connect()

    except Exception as err:
        return {
            'result' : 1,
            'msg'    : 'Encountered internal error while running checks',
        }


class sftp_conn_tester:

    def __init__(self, host, port, trace):
        self.host_  = host
        self.port_  = port
        self.trace_ = trace
        self.sbuff_ = []
        self.rbuff_ = []

    def _create_sock(self):
        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        return sock

    def test_basic_connect(self):
        try:

            self.rbuff_ = []
            trace = ""

            # Connect to remote host and attempt to read SSH server banner
            with self._create_sock() as sock:

                trace = "<div class='div-trace-line'> >> Attempting sonnection to host '{0}' on port {1}</div>".format(
                            self.host_,
                            self.port_)

                sock.connect((self.host_, self.port_))

                trace += "<div class='div-trace-line'> >> Connection succeeded; checking SFTP version</div>"

                # Read server connection banner
                buff = []
                while (len(self.rbuff_) < 1024):
                    buff = sock.recv(1024)
                    self.rbuff_ += buff
                    if len(buff) < 1024:
                        break;

                trace += "<div class='div-trace-line'> >> Server version string received</div>"
            
            # Validate SSH server banner
            # Pattern for banner is
            # SSH-<majvers>.<minvers>-<PrintableAsciiButSpaceOrDash> <PrintableAscii>\n
            verstr = bytes(self.rbuff_).decode()
            pattern = re.compile('SSH-\d.\d-[!\-!-~]+ [ -~]*\n')
            match = pattern.match(verstr)

            trace += "<div class='div-trace-line'> >> Server version string = '{0}'</div>".format(verstr)

            message = {
                'result' : 0,
                'msg'    : 'Successful SFTP connection',
                'trace'  : trace
            }

            if match is None:
                message['result'] = 2
                message['msg'] = "Service at host '{0}', port {1} doesn't appear to be SFTP"

            return message

        except ConnectionRefusedError as err:
            
            trace += "<div class='div-trace-line'> >> Connection error ='{0}'</div>".format(err)
            return {
                'result' : 4,
                'msg'    : "No active service found at host '{0}', port {1}.".format(
                    self.host_,
                    self.port_),
                'trace'  : trace
            }

        except OSError as err:
            trace += "<div class='div-trace-line'> >> Service error ='{0}'</div>".format(err)

            return {
                'result' : 8,
                'msg'    : "Encountered internal error connecting to SFTP service.",
                'trace'  : trace
            }

    def test_loop_connect(self):
        pass

    def test_full_connect(sefl):
        pass
