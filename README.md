# Tenda Beli SP3 Smart Plug Python Control Library
Tenda Beli SP3 is a $10-range power plug with 10A wifi-controlled relay. Manufacturer however only provides access via proprietary cloud and Android application. This project has the ambition of closing the gap by providing python control library, hopefully bypassing vendor's cloud.

## Reverse Engineering
### Provisioning
After factory reset, the device boots up as an wireless access point with ESSID "Tenda_Smart Plug_EB44" on channel 1. There is no wireless security protocol (WEP, WPA) in place so the communication between official Android app and the device can easily eavesdropped with some third wlan adapter switched into monitor mode and Wireshark.

There is DHCP server in place. The device has address of `192.168.25.1/8` and DHCP leases start at `192.158.25.100`. 

The device listens at port 5000 and accepts standard non encrypted HTTP/1.1. When the Android app accesses the device for the first time, it makes following request:
```http
GET /getDetail HTTP/1.1
Host: 192.168.25.1:5000
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.10.0
```
Responded by the device with:
```http
HTTP/1.1 200 OK

{"resp_code":0,"data":{"rssi":0, "mac":"e8:65:d4:81:eb:44","time_zone":480,"nick":"","sn":"E9641010010000854","model":"SP3V1.0","sft_ver":"V1.1.0.13(115)_SP3_EU","hrd_ver":"V1.0"}}
```
Next, the Android app requests a list of networks visible to the Device:
```http
POST /getWifi HTTP/1.1
Content-Length: 0
Host: 192.168.25.1:5000
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.10.0
```
The device respods with:
```http
HTTP/1.1 200 OK

{"resp_code":0,"data":{"result":[{"rssi":-48,"ssid":"Melnik","open":0},{"rssi":-53,"ssid":"WFMYHM23","open":0},{"rssi":-68,"ssid":"UPCF8D1BB7","open":0},{"rssi":-68,"ssid":"fima","open":0},{"rssi":-68,"ssid":"UPC3575430","open":0},{"rssi":-71,"ssid":"O2-Internet-585","open":0},{"rssi":-72,"ssid":"Slunecnice","open":0},{"rssi":-72,"ssid":"UPC8433289","open":0},{"rssi":-74,"ssid":"Tramal","open":0},{"rssi":-74,"ssid":"UPC7599266","open":0},{"rssi":-76,"ssid":"Internet_40","open":0},{"rssi":-78,"ssid":"UPC3940741","open":0},{"rssi":-85,"ssid":"UPC0380947","open":0},{"rssi":-85,"ssid":"WLAN-430549","open":0},{"rssi":-86,"ssid":"UPC8483279","open":0},{"rssi":-87,"ssid":"WiFi Renata","open":0},{"rssi":-88,"ssid":"UPCA5D191E","open":0},{"rssi":-90,"ssid":"JTNH","open":0},{"rssi":-91,"ssid":"LK","open":0},{"rssi":-92,"ssid":"UPC7B71F23","open":0}]}}
```
Finally, when the user chooses network the device should connect to, the Android app finishes the provisioning process with:
```http
POST /guideDone HTTP/1.1
Content-Type: application/json; charset=UTF-8
Content-Length: 166
Host: 192.168.25.1:5000
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.10.0

{"account":"email.registered.with.tenda.account@server.tld","key":"wireless_password","location":"Europe/Prague","server":"beli.valley.device.cloud.tenda.com.cn","ssid":"HomeNetworkSSID","timezone":60}
```
### Normal Operation in Local Mode

```http
POST /setSta HTTP/1.1
Content-Type: application/json; charset=UTF-8
Content-Length: 12
Host: 10.42.0.197:5000
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.10.0

{"status":1}
```
Response:
```http
HTTP/1.1 200 OK

{"resp_code":0,"status":1}
```

Get Status request:
```http
POST /getSta HTTP/1.1
Content-Length: 0
Host: 10.42.0.197:5000
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.10.0
```
Response:
```http
HTTP/1.1 200 OK

{"resp_code":0,"data":{"status":1}}
```