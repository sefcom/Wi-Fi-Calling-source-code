# Overview
In this repository you will find the experimental data along with source code for our paper, 'Wi Not Calling: Practical Privacy and Availability Attacks in Wi-Fi Calling'
The instructions for setting the experimental environment is illustrated in the sections below.
  
*Authors: Jaejong Baek, Sukwha Kyung, Haehyun Cho, Ziming Zhao, Yan Shoshitaishvili, Adam Doupé, and Gail-Joon Ahn*

# Test Environment
The diagram below shows two different test environment setup. In the first environment two physical hosts are used to prepare rogue AP and fake IPSec server, while only one physical host is used for both rogue AP and fake IPSec server in the second setup. We use the second setup (i.e., one physical host with VM) for our experiment.  
![Two Physical Hosts](/images/diagram.eps)  
![One Host](/images/Diagram1.eps)  
  
For rogue AP, we use Kali Linux set as a rogue AP and Ubuntu 16.04 virtual machine on virtualbox as fake IPSec Server.  
For installation and setting up the rogue AP, please refer to the document named "SoftAP.pdf" in "install" folder.  
For fake IPSec server installation and settings, please refer to the documentation named "strong_swan.pdf" in the same folder.  

# Performing the Test
Please proceed with the following steps to perform the IMSI privacy attack described in our paper:  
  
1. Run the phase 1 script (named "et1_[Service Provider Name].py") on the rogue AP and phase 2 script ("et2_[Service Provider Name].py") on the fake IPSec server, along with WireShark to collect packets exchanged.
2. Connect the victim UE to the rogue AP.
3. Once the UE is connected to the AP, enable Wi-Fi calling on the UE.
4. Using the key materials appear on fake IPSec server (i.e., strong_swan), decrypt the forged response packet on WireShark and you are able to see the payload including IMSI.