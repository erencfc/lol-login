from argparse import ArgumentParser
from requests import put
from client import start_client
from lcu import LCUInfo

parser = ArgumentParser()
parser.add_argument('--username', required=True, help='Username for authentication')
parser.add_argument('--password', required=True, help='Password for authentication')

args = parser.parse_args()

lcu = LCUInfo()
print("🟨 Starting to authenticate...")

lcu_port = lcu.port
lcu_endpoint = lcu.endpoint
lcu_password = lcu.password
lcu_user = lcu.user

user_nickname = args.username
user_password = args.password

payload = {
  'username': user_nickname,
  'password': user_password,
  'persistLogin': False
}

print("🟨 Trying to send request...")
try:
  response = put(lcu_endpoint, json=payload, verify=False, auth=(lcu_user, lcu_password))
  print("🟩 Request sent.")
except Exception as e:
  print("❗ Request failed.")
  if 'target machine actively refused it' in str(e):
    print('❗ Connection refused. Make sure you have the Riot Client running.')
  exit()

json = response.json()
message = json.get('message')
json_type = json.get('type')

if json_type == 'authenticated':
  print(f'🟩 Successfully logged in as {user_nickname}!')
  start_client('LeagueClient.exe', 'C:\\Riot Games\\League of Legends\\LeagueClient.exe')

if message == 'session_not_found: No previous RSO session found':
  print('❗ Login failed. Riot client is already logged in.')
  start_client('LeagueClient.exe', 'C:\\Riot Games\\League of Legends\\LeagueClient.exe')

if json_type == 'needs_credentials':
  print('❗ Login failed. Invalid credentials.')

print(f'JSON: {json}')
print()
print(f'Message: {message}')
print(f'Type: {json_type}')
print()