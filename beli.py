import click
import requests
import json

class BeliController:
    def __init__(self, ip):
        self._ip = ip
        self._host = f"{ip}:5000" 
        self._headers = {
            "Host": self._host,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0"
        }

    def _get(self, cmd, json=None):
        r = requests.get(url=f"http://{self._host}/{cmd}", headers=self._headers, json=json)
        if r.status_code != 200:
            print(f"Device responded with {r.status_code}")
        return r

    def _post(self, cmd, json=None):
        r = requests.post(url=f"http://{self._host}/{cmd}", headers=self._headers, json=json)
        if r.status_code != 200:
            print(f"Device responded with {r.status_code}")
        return r
        
    def get_detail(self):
        r = self._get("getDetail")
        print(r.json())
    def wifi_list(self):   
        r = self._post("getWifi")
        wifi_list = r.json()["data"]["result"]
        print(json.dumps(wifi_list))
    def finish(self):
        print("not implemented")
    def turn_off(self):
        self._post("setSta", json={"status": 0})
    def turn_on(self):
        self._post("setSta", json={"status": 1})
    def get_state(self):
        r = self._post("getSta")
        return r.json()
    def toggle(self):
        state = self.get_state()["data"]["status"]
        if state == 1:
            self.turn_off()
        else:
            self.turn_on()

@click.group()
@click.option("--ip", default="172.21.42.25", help="IP of the device")
def cli(ip):
    global beli
    beli = BeliController(ip)

@cli.group()
def setup():
    pass
@setup.command()
def get_detail():
    beli.get_detail()
@setup.command()
def wifi_list():
    beli.wifi_list()
@setup.command()
def finish():
    beli.finish()

@cli.command()
def turn_on():
    beli.turn_on()
@cli.command()
def turn_off():
    beli.turn_off()
@cli.command()
def get_state():
    state = beli.get_state()["data"]["status"]
    if state == 1:
        print("on")
    elif state == 0:
        print("off")
    else:
        print("unknown")

@cli.command()
def toggle():
    beli.toggle()
@cli.command()
def cycle():
    for i in range(10):
        beli.turn_off()
        beli.turn_on()

if __name__ == "__main__":
    cli()