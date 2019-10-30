from errbot import BotPlugin, botcmd, arg_botcmd, webhook

import requests
import urllib3
import time

import os
import logging
import json


logger = logging.getLogger("CogBot")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


cognito_username = os.getenv("COGNITO_USERNAME")
cognito_password = os.getenv("COGNITO_PASSWORD")
cognito_token = os.getenv("COGNITO_TOKEN")
cognito_url = os.getenv("COGNITO_URL")

if cognito_username is not None:
    logger.debug(
        "Read cognito_username from envrionent - username is %s", cognito_username
    )
else:
    logger.ERROR("Unable to read cognito_username from envrionemnt")

if cognito_password is not None:
    logger.debug(
        "Read cognito_password from envrionent - password is %s", cognito_password
    )
else:
    logger.ERROR("Unable to read cognito_password from envrionemnt")

if cognito_token is not None:
    logger.debug("Read cognito_token from envrionent - token is %s", cognito_token)
else:
    logger.ERROR("Unable to read cognito_token from envrionemnt")


class Cogbot(BotPlugin):
    """
    Cogbot integrates Cognito Detect with a variety of chat services.
    """

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        """
        return {"EXAMPLE_KEY_1": "Example value", "EXAMPLE_KEY_2": ["Example", "Value"]}

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation

        Raise a errbot.ValidationException in case of an error

        You should delete it if you're not using it to override any default behaviour
        """
        super(Cogbot, self).check_configuration(configuration)

    def callback_connect(self):
        """
        Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour
        """

        self.log.debug(
            "Querying the Cognito Detect brain for the number of hosts in the critical quadrant."
        )
        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json?page_size=all"}
        response = requests.get(
            url=vectra_brain_url + "/api/hosts/",
            auth=vectra_authentication,
            headers=headers,
            verify=False,
        )

        # Calculate number of hosts with active detections
        global last_poll_critical_hosts
        last_poll_critical_hosts = 0

        for host in range(len(response.json()["results"])):
            if response.json()["results"][host]["state"] == "active":

                current_host_category = self._score_host_(
                    response.json()["results"][host]["t_score"],
                    response.json()["results"][host]["c_score"],
                )

                if current_host_category == "critical":
                    last_poll_critical_hosts = last_poll_critical_hosts + 1
                    self.log.debug(
                        "On startup CogBot found {} hosts in the critical quadrant".format(
                            last_poll_critical_hosts
                        )
                    )

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    @webhook
    def example_webhook(self, incoming_request):
        """A webhook which simply returns 'Example'"""
        return "Example"

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def example(self, message, args):
        """A command which simply returns 'Example'"""
        return "Example"

    @arg_botcmd("name", type=str)
    @arg_botcmd("--favorite-number", type=int, unpack_args=False)
    def hello(self, message, args):
        """
        A command which says hello to someone.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            return f"Hello {args.name}."
        else:
            return f"Hello {args.name}, I hear your favorite number is {args.favorite_number}."

    @botcmd(split_args_with=None)
    def test(self, message, args):
        """ Test is just that, my first method on this class.  This is just a test
        """
        print(message)

        return "Completed Test"

    @botcmd(split_args_with=None)
    def lastpoll(self, message, args):
        """ Test is just that, my first method on this class.  This is just a test
        """
        yield (last_poll_critical_hosts)

        return "Completed Test"

    @botcmd(split_args_with=None)
    def ping(self, message, args):
        """The ping command will check CogBots connetion with the brain"""

        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(
                url=vectra_brain_url + "/api/system/info",
                auth=vectra_authentication,
                headers=headers,
                verify=False,
            )
            self.log.debug(response.json())

            if response.status_code == 200:
                return "PONG! Connection to brain {0} is successful! - status code {1}".format(
                    vectra_brain_url, response.status_code
                )
        except:
            return "PING FAILED!!"

    @botcmd(split_args_with=None)
    def host_status(self, message, args):
        """The ping command will check CogBots connetion with the brain"""

        yield "Querrying the Cognito Detect Brain"
        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json?page_size=all"}
        response = requests.get(
            url=vectra_brain_url + "/api/hosts/",
            auth=vectra_authentication,
            headers=headers,
            verify=False,
        )

        self.log.debug(response.json())
        total_hosts = response.json()["count"]

        # Calculate number of hosts with active detections
        host_with_active_detections = 0
        critical_hosts = 0
        high_hosts = 0
        medium_hosts = 0
        low_hosts = 0

        for host in range(len(response.json()["results"])):
            if response.json()["results"][host]["state"] == "active":
                self.log.debug("Active host")
                host_with_active_detections = host_with_active_detections + 1

                current_host_category = self._score_host_(
                    response.json()["results"][host]["t_score"],
                    response.json()["results"][host]["c_score"],
                )
                if current_host_category == "low":
                    low_hosts = low_hosts + 1
                elif current_host_category == "medium":
                    medium_hosts = medium_hosts + 1
                elif current_host_category == "high":
                    high_hosts = high_hosts + 1
                elif current_host_category == "critical":
                    critical_hosts = critical_hosts + 1

            else:
                self.log.debug("not active host")

        yield "Done"

        # for host in response.json()["results"]:
        #     if response.json()["results"][host]["state"] == "active":
        #         yield "Host id has active detections"

        yield "The total number of hosts seen is {}".format(total_hosts)
        yield "The number of hosts with active detections is {}".format(
            host_with_active_detections
        )
        yield "Of the {} hosts with active detections".format(
            host_with_active_detections
        )
        yield "{} hosts are scored as low".format(low_hosts)
        yield "{} hosts are scored as medium".format(medium_hosts)
        yield "{} hosts are scored as high".format(high_hosts)
        yield "{} hosts are scored as critical".format(critical_hosts)

    @arg_botcmd("--hostid", dest="hostid", type=str)
    def host_isolate(self, message, hostid):
        """isolate --hostid <hostid> will isolate the specified hostid"""

        yield "Querrying the Cognito Detect Brain"
        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json?page_size=all"}
        response = requests.get(
            url=vectra_brain_url + "/api/hosts/{}".format(hostid),
            auth=vectra_authentication,
            headers=headers,
            verify=False,
        )

        self.log.debug(response.json())
        host_ip_address = response.json()["last_source"]
        yield "isolating host hostid {} ip_address {}".format(hostid, host_ip_address)
        yield "communicating with CrowdStrike API"
        self._isolate_with_crowdstrike(message, hostid)

        yield "Completed"

    @arg_botcmd("--hostid", dest="hostid", type=str)
    def host_unisolate(self, message, hostid):
        """unisolate --hostid <hostid> will unisolate the specified hostid"""

        yield "Querrying the Cognito Detect Brain"
        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json?page_size=all"}
        response = requests.get(
            url=vectra_brain_url + "/api/hosts/{}".format(hostid),
            auth=vectra_authentication,
            headers=headers,
            verify=False,
        )

        self.log.debug(response.json())
        host_ip_address = response.json()["last_source"]
        yield "unisolating host hostid {} ip_address {}".format(hostid, host_ip_address)
        yield "communicating with CrowdStrike API"
        self._isolate_with_crowdstrike(message, hostid)

        yield "Completed"

    @arg_botcmd("--interval", dest="interval", type=int)
    def scan_critical_hosts(self, message, interval):
        """start scan will start reporting
        """
        self.start_poller(interval, self.count_critical_hosts, times=3)

    @botcmd()
    def stop_scan(self, message, interval):
        """start scan will start reporting
        """
        self.stop_poller(None)

    def count_critical_hosts(self):
        global last_poll_critical_hosts
        self.log.debug("count_critical_hosts() Called!")

        vectra_authentication = (cognito_username, cognito_password)
        vectra_brain_url = cognito_url
        headers = {"Content-Type": "application/json?page_size=all"}
        response = requests.get(
            url=vectra_brain_url + "/api/hosts/",
            auth=vectra_authentication,
            headers=headers,
            verify=False,
        )
        # Now let's see how many critical hosts exist now
        critical_hosts = 0

        for host in range(len(response.json()["results"])):
            if response.json()["results"][host]["state"] == "active":

                current_host_category = self._score_host_(
                    response.json()["results"][host]["t_score"],
                    response.json()["results"][host]["c_score"],
                )

                if current_host_category == "critical":
                    critical_hosts = critical_hosts + 1
        self.log.debug(
            "last critical hosts = {} this querry critical hosts={}".format(
                last_poll_critical_hosts, critical_hosts
            )
        )
        if last_poll_critical_hosts == critical_hosts:
            self.send(
                self.build_identifier("#chatsecops"),
                "No change in number of hosts in the critical quanrant.",
            )
            last_poll_critical_hosts = critical_hosts

        if last_poll_critical_hosts < critical_hosts:
            self.send(
                self.build_identifier("#chatsecops"),
                "ALERT - In increase of {} hosts in the critical quandrant has occured!".format(
                    critical_hosts - last_poll_critical_hosts
                ),
            )
            last_poll_critical_hosts = critical_hosts

    def _score_host_(self, threat, certainty):
        """score_host will return a string to describe the current hosts scoring"""

        if threat <= 50 and certainty <= 50:
            self.log.debug("host score low")
            return "low"

        elif threat >= 51 and certainty <= 50:
            self.log.debug("host score high")
            return "high"

        elif threat >= 50 and certainty <= 50:
            self.log.debug("host score medium")
            return "medium"

        elif threat >= 51 and certainty >= 51:
            self.log.debug("host score critical")
            return "critical"

        else:
            self.log.debug("This shouldn't happen!")

    def _isolate_with_crowdstrike(self, message, hostid):

        time.sleep(5)
        yield "Isolation with CrowdStrike completed successfully!"
