import json
import re
import socket

from paramiko.client        import SSHClient
from paramiko.sftp_client   import SFTPClient
from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/index.mak')
def on_page_load(request):

    #import pdb;pdb.set_trace()
    host_list = json.loads(request.registry.settings['checksftp.host_list'])

    return {'project'  : 'checksftp',
            'host_list' : host_list['hosts']}

@view_config(route_name='runthecheck', renderer='json')
def on_run_check(request):

    try:

        #import pdb;pdb.set_trace()

        host        = request.GET['host']
        port        = int(request.GET['port'])
        checktype   = request.GET['checktype']


        trace = False
        if 'trace' in request.GET and request.GET['trace']:
            trace = True

        sct = sftp_conn_tester(host, port, trace)

        if checktype == "simple" or checktype == "continuous":
            return sct.test_basic_connect()
        elif checktype == "full":
            test_acct = json.loads(request.registry.settings['checksftp.test_acct'])
            return sct.test_full_connect(test_acct['user'], test_acct['password'])
        else:
            raise Exception("Unrecognized check type '{0}'".format(checktype))

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
            pattern = re.compile('SSH-\d.\d-[!\-!-~]+ [ -~]*\r?\n')
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

    def test_full_connect(self, uname, passwd):

        trace = ""

        #import pdb;pdb.set_trace()
        try:
            with SSHClient() as sshClient:

                trace = "<div class='div-trace-line'> >> Attempting sonnection to host '{0}' on port {1}</div>".format(
                            self.host_,
                            self.port_)

                sshClient.load_host_keys("/home/{0}/.ssh/known_hosts".format(uname))

                sshClient.connect(self.host_,
                        port=self.port_,
                        username=uname,
                        password=passwd)

                trace += "<div class='div-trace-line'> >> Connection succeeded; requesting SFTP service</div>"

                sftpClient = sshClient.open_sftp()

                # Test simplest SFTP functionality

                trace += "<div class='div-trace-line'> >> Testing directory creation</div>"
                try:
                    sftpClient.mkdir(".checksftp_test_dir")
                    trace += "<div class='div-trace-line'> >> Directory creation successful</div>"
                except Exception as err:
                    trace += "<div class='div-trace-line'> >> Directory creation failed! {0}</div>".format(
                            err)

                trace += "<div class='div-trace-line'> >> Testing file write</div>"
                try:
                    sftpClient.put(".checksftp_test_file", ".checksftp_test_dir/.checksftp_test_file_up")
                    trace += "<div class='div-trace-line'> >> File write successful</div>"
                except Exception as err:
                    trace += "<div class='div-trace-line'> >> File write failed! {0}</div>".format(
                            err)

                trace += "<div class='div-trace-line'> >> Testing file read</div>"
                try:
                    sftpClient.get(".checksftp_test_dir/.checksftp_test_file_up", ".checksftp_test_file_down")
                    trace += "<div class='div-trace-line'> >> File read successful</div>"
                except Exception as err:
                    trace += "<div class='div-trace-line'> >> File read failed! {0}</div>".format(
                            err)

                trace += "<div class='div-trace-line'> >> Testing file removal</div>"
                try:
                    sftpClient.remove(".checksftp_test_dir/.checksftp_test_file_up")
                    trace += "<div class='div-trace-line'> >> File removal successful</div>"
                except Exception as err:
                    trace += "<div class='div-trace-line'> >> File removal failed! {0}</div>".format(
                            err)

                trace += "<div class='div-trace-line'> >> Testing directory removal</div>"
                try:
                    sftpClient.rmdir(".checksftp_test_dir")
                    trace += "<div class='div-trace-line'> >> Directory removal successful</div>"
                except Exception as err:
                    trace += "<div class='div-trace-line'> >> Directory removal failed! {0}</div>".format(
                            err)


            trace += "<div class='div-trace-line'> >> SFTP session completed successfully</div>"

            return {
                'result' : 0,
                'msg'    : 'Successful SFTP connection',
                'trace'  : trace
            }


        except SSHException as err:
            trace += "<div class='div-trace-line'> >> Service error ='{0}'</div>".format(err)

            return {
                'result' : 8,
                'msg'    : "Encountered internal error connecting to SFTP service.",
                'trace'  : trace
            }


