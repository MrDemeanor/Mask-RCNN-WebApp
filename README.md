# We will run this with an NGINX instance

## If you don't have NGINX on your server:
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev nginx
```

## How to run

```bash
virtualenv -p python3 venv
source venv/bin/activate
source requirements.txt
uwsgi --socket 0.0.0.0:8000 --protocol=http -w main
```

Then find out what the IP of your server is by typing in:
```bash
ifconfig
```
Go to that IP address at port 8000 in your web browser
```bash 
<your_ip_address>:8000
```
