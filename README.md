# We will run this with an NGINX instance

## Connect to server via ssh and forward your local machine's port 8000 to the server's port 8000

ssh <username>@<server_ip> -L 8000:localhost:8000

## If you don't have NGINX on your server:
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev nginx
```

## How to run

```bash
git clone https://git.txstate.edu/M12/IMA_MaskRCNN_Web_Service.git
cd IMA_MaskRCNN_Web_Service
virtualenv -p python3 venv
source venv/bin/activate
source requirements.txt
```
Make a folder called _weights_ in the root of the project directory. Download the pretrained coco weights and place .h5 weights file in this folder.

```bash
mkdir weights
cd weights
wget https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5
cd ..
uwsgi --socket 0.0.0.0:8000 --protocol=http -w main
```

On your local machine, navigate to 

```bash
localhost:8000
```
