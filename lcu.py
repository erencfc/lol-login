from os import popen
from client import start_client, check_client

class LCUInfo:
    def __init__(self):
        isLeagueRunning = check_client("LeagueClient.exe")
        if isLeagueRunning:
            print("🟥 League Client is already running. Exiting...")
            exit(1)

        start_client("RiotClientUx.exe", "C:\\Riot Games\\Riot Client\\UX\\RiotClientUx.exe")

        info_cmd = popen("wmic PROCESS WHERE name='RiotClientUx.exe' GET commandline").read().replace(' ', '')
        splits = info_cmd.split('--')
        auth_token = None
        port = None

        for item in splits:
            if "remoting-auth-token" in item:
                auth_token = item.split("=")[1]
            if "app-port" in item:
                port = item.split("=")[1]

        if not auth_token:
            print("🟥 Failed to get auth token. Exiting...")
            exit(1)
        if not port:
            print("🟥 Failed to get access port. Exiting...")
            exit(1)

        self.port = port
        self.endpoint = f'https://127.0.0.1:{port}/rso-auth/v1/session/credentials'
        self.user = 'riot'
        self.password = auth_token