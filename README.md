# lora-raw


### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:
```bash
sudo bash script.bash start -service_name=<service_name> -u=<pi|debian> -dir=<working_dir> -lib_dir=<common-py-libs-dir> -data_dir=<data_dir> -p=<port>
sudo bash script.bash start -service_name=nubeio-lora-raw.service -u=pi -dir=/home/pi/lora-raw -lib_dir=/home/pi/common-py-libs -data_dir=/data/lora-raw -p=1919
sudo bash script.bash -h
```


```
git clone --depth 1 https://github.com/NubeIO/lora-raw
cd lora-raw/
# if required install python3-venv
sudo apt-get install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```



```
sudo cp systemd/nubeio-lora-raw.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl disable nubeio-lora-raw.service
sudo systemctl enable nubeio-lora-raw.service
sudo journalctl -f -u nubeio-lora-raw.service
sudo systemctl status nubeio-lora-raw.service
sudo systemctl start nubeio-lora-raw.service
sudo systemctl stop nubeio-lora-raw.service
sudo systemctl restart nubeio-lora-raw.service

```