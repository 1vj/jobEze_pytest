import datetime
import logging
import select
import time
from datetime import datetime
import allure
import paramiko
import pysftp
import pytest
import pytz
from jumpssh import SSHSession

log = logging


class SSH_Remote_Connect:

    def __init__(self):
        pass

    def get_current_time_hm(self):
        """
        Method to get the time with hours and minutes in given format
        """
        ts = time.time()
        currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        return currentTime

    def get_current_time_h(self):
        """
        Method to get the time with hours in given format
        """
        ts = time.time()
        currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H')
        return currentTime

    def ssh_into_site(self, remote_ip, username, password):
        """
        This function checks that logging into the site (via SSH) is successful
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            with allure.step('Attempt to SSH into IP:' + remote_ip + ' with user:' + username):
                log.info('Attempt to SSH into IP:' + remote_ip + ' with user:' + username)
                ssh.connect(hostname=remote_ip, port=22, username=username, password=password, timeout=10)
        except:
            pytest.fail(msg="Failed attempt to SSH into Remote machine with IP: " + remote_ip)

        return ssh

    def connect_to_remote_machine(self, remote_ip, username, password):
        """
         Method to establish a connection with remote machine with given IP, username and password

        :param remote_ip: remote machine IP Address
        :param username: remote machine SSH username
        :param password: remote machine SSH password
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_ip = remote_ip
        username = username
        password = password
        ssh_client.connect(remote_ip, username=username, password=password, timeout=12, allow_agent=False)
        return ssh_client

    def ssh_shell_cmds(self, remote_ip, username, password, command):
        """
            Method to connect the remote machine and execute the given SSH Command.
            Validate the Empty/None output for given command

        :param remote_ip: remote machine IP Address
        :param username: remote machine SSH username
        :param password: remote machine SSH password
        :param command: SSH Command to execute
        :return:
        """
        ssh_client = self.connect_to_remote_machine(remote_ip, username, password)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = []
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    tmp = stdout.channel.recv(1024)
                    # output = tmp.decode()
                    output.append(tmp.decode())
        log.info('output of ssh cmd at this point {}'.format(output))
        ssh_client.close()
        # return list
        return output

    def simple_shell_cmd(self, remote_ip, username, password, cmd):
        """
        Method to connect a remote machine and execute the given command.
        Validate and return the response as list
        """
        ssh_client = self.connect_to_remote_machine(remote_ip, username, password)
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        data = stdout.readlines()
        ssh_client.close()
        if data:
            log.info("Found the data from remote system by command")
        else:
            log.info("Not Found the data from remote system by command")
            assert False
        return data

    def shell_sudo_command(self, ssh_username, ssh_password, ssh_machine, command):
        """
            Executes a sudo command over a established SSH connection
        """
        jobid = "None"
        conn = self.connect_to_remote_machine(ssh_machine, ssh_username, ssh_password)
        command = "sudo -S -p '' %s" % command
        logging.info("Job[%s]: Executing: %s" % (jobid, command))
        stdin, stdout, stderr = conn.exec_command(command=command)
        stdin.write(ssh_password + "\n")
        stdin.flush()
        stdoutput = [line for line in stdout]
        stderroutput = [line for line in stderr]
        for output in stdoutput:
            logging.info("Job[%s]: %s" % (jobid, output.strip()))
        # Check exit code.
        logging.debug("Job[%s]:stdout: %s" % (jobid, stdoutput))
        logging.debug("Job[%s]:stderror: %s" % (jobid, stderroutput))
        logging.info("Job[%s]:Command status: %s" % (jobid, stdout.channel.recv_exit_status()))
        if not stdout.channel.recv_exit_status():
            logging.info("Job[%s]: Command executed." % jobid)
            conn.close()
            if not stdoutput:
                stdoutput = True
            return True, stdoutput
        else:
            logging.error("Job[%s]: Command failed." % jobid)
            for output in stderroutput:
                logging.error("Job[%s]: %s" % (jobid, output))
            conn.close()
            return False, stderroutput

    def connect_to_remote_machine_private_key(self, host_ip, username, private_key):
        """
        Establish a connection with remote machine using private key
        """
        log.info('ssh with private key and run command')
        k = paramiko.RSAKey.from_private_key_file(private_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        log.info('Connecting..')
        c.connect(hostname=host_ip, username=username, pkey=k)
        log.info('Connected')
        return c

    def connect_thru_jumphost(self, dest_addr, remote_ip, username, password, pemfile):
        """
        Establish the ssh connection with remote machine with jump host
        """
        jhost = self.connect_to_remote_machine(remote_ip, username, password)
        vmtransport = jhost.get_transport()
        dest_addrt = (dest_addr, 22)
        local_addrt = (remote_ip, 22)
        vmchannel = vmtransport.open_channel("direct-tcpip", dest_addrt, local_addrt)
        k = paramiko.RSAKey.from_private_key_file(pemfile)
        rhost = paramiko.SSHClient()
        rhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rhost.connect(hostname=dest_addr, port=22, username="view", pkey=k, sock=vmchannel)
        return jhost, rhost

    def jumphost_simple_shell_cmd(self, dest_addr, remote_ip, username, password, pemfile, cmd):
        """
        Method to get the list of response, over the connection established through jump remote machine
        """
        jhost, rhost = self.connect_thru_jumphost(dest_addr, remote_ip, username, password, pemfile)
        stdin, stdout, stderr = rhost.exec_command(cmd)
        data = stdout.readlines()
        rhost.close()
        jhost.close()
        if data:
            log.info("Got data from remote host by command: " + cmd)
        else:
            log.error("Error with command: " + cmd)
            log.error("Error output: " + str(stderr.read()))
        return data

    def connect_jump_ssh(self, port_num, remote_addr, remote_ip, username, password, pemfile):
        """
        Method to execute the command over the connection established through jump remote machine
        """
        jump_session = SSHSession(host=remote_ip, username=username, password=password)
        remote_session = jump_session.get_remote_session(host=remote_addr, username="view",
                                                         private_key_file=pemfile)
        log.info('Attempt to SSH into Port:' + str(port_num))
        try:
            with allure.step('Attempt to SSH into Port:' + str(port_num)):
                tunnel_session = remote_session.get_remote_session(host='127.0.0.1', username=username, port=port_num,
                                                                   password=password)
        except:
            tunnel_session = "Failed to SSH into Port:" + str(port_num)
            if remote_session.is_active():
                remote_session.close()
            if jump_session.is_active():
                jump_session.close()
        return jump_session, remote_session, tunnel_session

    def jump_ssh_cmd(self, port_num, remote_addr, remote_ip, username, password, pemfile, cmd):
        """
        Method to execute the command over the connection established through jump remote machine
        """
        log.info(cmd)
        js, rs, ts = self.connect_jump_ssh(port_num, remote_addr, remote_ip, username, password, pemfile)
        try:
            output = ts.get_cmd_output(cmd)
            if ts.is_active():
                ts.close()
            if rs.is_active():
                rs.close()
            if js.is_active():
                js.close()
            return output
        except Exception as e:
            log.error("%s\n%s" % (e, ts))
            raise Exception("%s\n%s" % (e, ts))

    def ssh_private_key_shell_cmds(self, remote_ip, username, private_key, command):
        """
        Method to validate the empty  response, over the connection established through private key
        """
        ssh_client = self.connect_to_remote_machine_private_key(remote_ip, username, private_key)
        time.sleep(10)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = []
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    tmp = stdout.channel.recv(1024)
                    # output = tmp.decode()
                    output.append(tmp.decode())
        log.info('output of ssh cmd at this point {}'.format(output))
        ssh_client.close()
        return output

    def ssh_private_key_simple_shell_cmd(self, remote_ip, username, private_key, cmd):
        """
        Method to get the list of response over the connection established through private key
        """
        ssh_client = self.connect_to_remote_machine_private_key(remote_ip, username, private_key)
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        data = stderr.readlines()
        ssh_client.close()
        if data:
            log.error("Given command was invalid...please check it - " + cmd)
            assert False
        else:
            log.info("Successfully run command!")

    def retry_shell_cmd(self, num_retry, ip, username, password, cmd_pass_to_shell):
        """
        Method to execute the SSH command in a loop with given loop count.
        Break the execution once got response with loop count.
        """
        # count = 0
        if 30 < num_retry or num_retry < 2:
            num_retry = 10
        for i in range(num_retry):
            # i = i + 1
            time.sleep(10)
            output_from_shell = self.ssh_shell_cmds(ip, username, password, cmd_pass_to_shell)
            log.info('retry_shell_cmd(): cmd to  shell will be: {}'.format(cmd_pass_to_shell))
            log.info('retry_shell_cmd(): ip {} output of shell line: {} '.format(ip, output_from_shell))
            log.info('\n retry provided: {}'.format(num_retry))
            if output_from_shell.__len__() > 0:
                break
        if len(output_from_shell) == 0:
            output_from_shell = ['no match']
        return output_from_shell

    @staticmethod
    def transfer_file_to_remote_machine(remote_ip, username, password, src_file, remote_path):
        """
        Method to transfer a file from local machine to remote machine
        """
        with allure.step('Transfer file from local to remote machine'):
            log.info("Transfer file from local to remote machine.")
            s = pysftp.Connection(host=remote_ip, username=username, password=password)
            log.info("Transfer file {0} from local to remote machine at path: {1}.".format(src_file, remote_path))
            s.put(src_file, remote_path)
            s.close()

    def get_time_zone_of_given_machine(self, remote_ip, username, password):
        """
        Method to get the time zone of the given machine
        """
        log.info("Method to get the time zone of given machine")
        timeZone_command = "timedatectl | grep 'Time zone'"
        output = self.shell_sudo_command(username, password, remote_ip, timeZone_command)
        tz = output[1][0].split(":")[1].split("(")[0].strip()
        return tz

    def get_current_time_of_given_machine(self, remote_ip, username, password):
        """
        Method to get current time of the given machine
        """
        log.info("Method to get current time of the given machine")
        tz = self.get_time_zone_of_given_machine(remote_ip, username, password)
        new_tz = pytz.timezone(tz)
        date_time = datetime.now(new_tz)
        return date_time

    def get_given_cronjob_path(self, ssh_machine, ssh_user, ssh_password, cron_job_value):
        """
        Method to get the cron job path
        """
        cron_cmd = 'crontab -l'
        cron_job_list = self.simple_shell_cmd(ssh_machine, ssh_user, ssh_password, cron_cmd)
        for output in cron_job_list:
            if cron_job_value in output:
                cronjob_path = output
                break
        return "/" + cronjob_path.split(" >")[0].split(" /")[1]
