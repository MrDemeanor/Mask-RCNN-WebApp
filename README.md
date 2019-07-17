# We will run this with an NGINX instance

## Connect to server via ssh and forward your local machine's port 8000 to the server's port 8000. Be sure to have saved the private key to ~/.ssh. 

```bash
ssh -i ~/.ssh/uni_tx <user_name>@34.73.225.25 -L 8000:localhost:8000
```
where "<user_name>" would be replaced by your actual username. 

## How to run

CD into the directory of this project and running the following command: 

```bash
source setup.sh
```

The setup file will create a virtual environment, install dependencies, download the weights file, and start the program. If you want to stop the server, press "Control + C" on your keyboard. Then, to restart the server:

```bash
uwsgi --socket 0.0.0.0:8000 --protocol=http -w main
```
You'll know the script has finished when you encounter the following screen:

On your local machine, navigate to 

```bash
localhost:8000
```
You should be presented with a screen like this:

Click on the button that says "Choose file" and select an image to send to the server:

Wait for the server to process the image. When finished, a JSON file containing all detections in the image will start downloading. 
