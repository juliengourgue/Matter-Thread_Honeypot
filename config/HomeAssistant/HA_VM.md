# How to run Home Assistant in a VM

https://www.virtualbox.org/manual/ch08.html

https://community.home-assistant.io/t/install-home-assistant-os-with-virtualbox-on-ubuntu-headless-cli-only/384249


#### List running vm
```
VBoxManage list runningvms | cut -d '"' -f 2 | while read machine; do    echo "$machine"; done
```

#### Shutdown vm
```
VBoxManage controlvm homeassistant acpipowerbutton
```
#### Start vm
```
VBoxManage startvm "homeassistant" --type headless
```

#### To run the HA vm
```bash
VBoxManage createvm --name homeassistant --register
VBoxManage modifyvm homeassistant --ostype Linux_64
VBoxManage modifyvm homeassistant --memory 6144 --vram 16
VBoxManage modifyvm homeassistant --cpus 4

wget https://github.com/home-assistant/operating-system/releases/download/14.2/haos_ova-14.2.vdi.zip

unzip haos_ova-14.2.vdi.zip

rm haos_ova-14.2.vdi.zip
mv haos_ova-14.2.vdi VirtualBox\ VMs/homeassistant/

VBoxManage storagectl homeassistant --name "SATA Controller" --add sata --controller IntelAHCI

VBoxManage storageattach homeassistant --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ~/VirtualBox\ VMs/homeassistant/haos_ova-14.2.vdi

VBoxManage modifyvm homeassistant --nic1 bridged --nictype1 82540EM --bridgeadapter1 eno1

VBoxManage modifyvm homeassistant --firmware efi

# Filter to add the nrf Donggle
VBoxManage usbfilter add 0 --target "homeassistant" --name "nRFDongle" --vendorid 0x1915 --productid 0xcafe
VBoxManage modifyvm "homeassistant" --usb on
VBoxManage modifyvm "homeassistant" --usbehci on  # For USB 2.0


VBoxManage startvm homeassistant --type headless

```
