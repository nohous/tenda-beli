import click
import requests
import json

@click.group()
@click.option("--ip", default="192.168.25.1", help="IP of the device")
def cli(ip):
    global ip_addr, host, headers
    ip_addr = ip
    host = f"{ip_addr}:5000" 
    headers = {
        "Host": host,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.10.0"
    }

@cli.group()
def setup():
    pass

@setup.command()
def get_detail():
    r = requests.get(url=f"http://{host}/getDetail", headers=headers)
    if r.status_code != 200:
        print("Device responded with error code", r.status_code)
        return
    print(r.json())

@setup.command()
def wifi_list():
    r = requests.post(url=f"http://{host}/getWifi", headers=headers)
    if r.status_code != 200:
        print("Device responded with error code", r.sttus_code)
        return
   
    wifi_list = r.json()["data"]["result"]
    print(json.dumps(wifi_list))
@setup.command()
def finish():
    print("Not implemented")

@cli.command()
def turn_on():
    r = requests.post(url=f"http://{host}/setSta", headers=headers,json={"status": 1})
    if r.status_code != 200:
        print("Device responded with error code", r.sttus_code)
        return

@cli.command()
def turn_off():
    r = requests.post(url=f"http://{host}/setSta", headers=headers,json={"status": 0})
    if r.status_code != 200:
        print("Device responded with error code", r.sttus_code)
        return

@cli.command()
def get_state():
    r = requests.post(url=f"http://{host}/getSta", headers=headers)
    if r.status_code != 200:
        print("Device responded with error code", r.sttus_code)
        return
    print(r.json())

if __name__ == "__main__":
    cli()