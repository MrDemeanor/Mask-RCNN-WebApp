sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
source requirements.txt
mkdir weights
cd weights
wget https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5
cd ..
uwsgi --socket 0.0.0.0:8000 --protocol=http -w main
