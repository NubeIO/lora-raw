# lora-raw



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