
  Virtual Storage Manager for Ceph
==========================================================

**Version:** 0.7

**Source:** 2014-10

**Keywords:** Ceph, Virtual Storage Management

Preparation
===================================
Before you get ready to install VSM, you should prepare your environment. The sections here are very helpful for you to understand the deployment concepts.

**Note**For a stable Ceph System, and VSM cluster, you should prepare at least three nodes to install VSM cluster. Otherwise, when VSM creates the Ceph cluster, VSM may raise an error.

#Roles
There are two roles for the VSM cluster.
## Controller Node
Controller node is used to run mysql, rabbitmq, web ui services for vsm cluster.
## Storage Node
Storage node is used to run vsm-agent service which will manage the ceph and physical resources.

#Network
There are three kinds of networka defined in VSM.
## Management Network
Management Network is used to manage the whole VSM cluster. So, every node in VSM cluster should have this kind of network.
## Ceph Public Network
Ceph Public Network is used by ceph to manage ceph client and server IO operations. 
## Ceph Cluster Network
Ceph Cluster Network is used by ceph to transfer data between OSDs for replication and rebalancing.

##Recommendations
Controller node should contain at least:

    - Management Network

Storage Node should contain:

    - Management Network
    - Ceph Public Network
    - Ceph Cluster Network

###Sample 1
**Controller node** contains the networks listed below:

    - 172.169.32.0/21 # accessing internet.
    - 192.168.123.0/24

**Storage node** contains networks below:

    - 192.168.123.0/24
    - 192.168.124.0/24
    - 192.168.125.0/24

Then we may assign these networks as below:

    - Management network: 192.168.123.0/24
    - Ceph public netwok: 192.168.124.0/24
    - Ceph cluster network: 192.168.125.0/24

The configuration for VSM in the `cluster_manifest` file should be:

    [management_addr]
    192.168.123.0/24

    [ceph_public_addr]
    192.168.124.0/24

    [ceph_cluster_addr]
    192.168.125.0/24

**Note** Here we do not use the public network for accessing the internet in our VSM cluster, so, there are no settings for this.

**cluster_manifest** Do not worry about this file right now, we will talk  about it later.

### Sample 2
But how about when all the node just have two NICs. Such as controller node and storage node just have:

    - 192.168.124.0/24
    - 192.168.125.0/24

We may assign these two networks as below:

    - Management network: 192.168.124.0/24
    - Ceph public network: 192.168.124.0/24
    - Ceph cluster network: 192.168.125.0/24

The configuration for VSM in `cluster_manifest` file should be:

    [management_addr]
    192.168.124.0/24

    [ceph_public_addr]
    192.168.124.0/24

    [ceph_cluster_addr]
    192.168.125.0/24

### Sammple 3
It's quite common to have just one NIC for demo environments. Such as all nodes just have:

    - 192.168.124.0/24

We may assign this network as below:

    - Management network: 192.168.124.0/24
    - Ceph public network: 192.168.124.0/24
    - Ceph cluster network: 192.168.124.0/24

So all the network just use the same network. The configurations in VSM `cluster_manifest` file would then be:

    [management_addr]
    192.168.124.0/24

    [ceph_public_addr]
    192.168.124.0/24

    [ceph_cluster_addr]
    192.168.124.0/24

#Operating System
We are developing/testing based on CentOS 6.5 Linux system. For successful installation of VSM, it's best to install system with **CentOS-6.5 Basic Server**.

After install of CentOS system, do not run:

    yum update

Otherwise you may get conflicts between yum packages when you install VSM.

#Build RPM
After you download the source code from github. The first step is to build VSM RPMs. If you already have VSM RPMs, please directly jump to [VSM RPM Install](#RPM_Install).

## Setup Yum Repo
###Step 1
Mout CentOS-6.5-DVD1.iso as you repo.

    mount -o loop CentOS-6.5-x86_64-bin-DVD1.iso /media/CentOS/

Then add a repo file `dvd.repo` in /etc/yum.repos.d/:

    [dvdrepo]
    name=CentOS-DVD
    baseurl=file:///media/CentOS/
    gpgcheck=0
    enabled=1
    proxy=_none_

Then run:

    yum makecache

###Step 2
Add out public repo, make sure you can access internet. Add a public repo file `public.repo`:

    [theforeman-plugin-source]
    name=theforeman-plugins
    baseurl=http://yum.theforeman.org/plugins/1.5/el6/source
    gpgcheck=0
    enabled=1

    [theforman-plugins-x86_64]
    name=theforman-plugins-x86_64
    baseurl=http://yum.theforeman.org/plugins/1.5/el6/x86_64
    gpgcheck=0
    enabled=1

    [theforeman-release-source]
    name=theforeman-release-source
    baseurl=http://yum.theforeman.org/releases/1.5/el6/source
    gpgcheck=0
    enabled=1

    [theforeman-release-x86_64]
    name=theforeman-release-x86_64
    baseurl=http://yum.theforeman.org/releases/1.5/el6/x86_64
    gpgcheck=0
    enabled=1

    [puppetlabs-products-x86_64]
    name=puppetlabs-products-x86_64
    baseurl=http://yum.puppetlabs.com/el/6/products/x86_64
    gpgcheck=0
    enabled=1

    [puppetlabs-dependencies]
    name=puppetlabs-dependencies
    baseurl=http://yum.puppetlabs.com/el/6/dependencies/x86_64
    gpgcheck=0
    enabled=1

    [puppetlabs-devel]
    name=puppetlabs-devel
    baseurl=http://yum.puppetlabs.com/el/6/devel/x86_64
    gpgcheck=0
    enabled=1

    [puppetlabs-products-srpms]
    name=puppetlabs-products-srpms
    baseurl=http://yum.puppetlabs.com/el/6/products/SRPMS
    gpgcheck=0
    enabled=1

    [puppetlabs-dependencies-srpms]
    name=puppetlabs-dependencies-srpms
    baseurl=http://yum.puppetlabs.com/el/6/dependencies/SRPMS
    gpgcheck=0
    enabled=1

    [puppetlabs-devel-srpms]
    name=puppetlabs-devel-srpms
    baseurl=http://yum.puppetlabs.com/el/6/devel/SRPMS
    gpgcheck=0
    enabled=1

    [openstack-icehouse]
    name=openstack-icehouse
    baseurl=http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/epel-6/
    gpgcheck=0
    enabled=1

    [ceph]
    name=ceph
    baseurl=http://ceph.com/rpm/el6/x86_64
    gpgcheck=0
    enabled=1

    [ceph-extras]
    name=ceph-extras
    baseurl=http://ceph.com/packages/ceph-extras/rpm/centos6/x86_64
    gpgcheck=0
    enabled=1

    [epel]
    name=epel
    baseurl=http://mirror.steadfast.net/epel/6/x86_64/
    gpgcheck=0
    enabled=1

    [rpmfind]
    name=rpmfind
    baseurl=http://rpmfind.net/linux/centos/6.5/os/x86_64/
    gpgcheck=0
    enabled=1

    [nac-net]
    name=nac-net
    baseurl=http://centos.mirror.nac.net/6.5/os/x86_64/
    gpgcheck=0
    enabled=1

    [cs.vt]
    name=cs-vt
    baseurl=http://mirror.cs.vt.edu/pub/CentOS/6.5/updates/x86_64/
    gpgcheck=0
    enabled=1

    [download-fedoraproject]
    name=download-fedoraporject
    baseurl=http://download.fedoraproject.org/pub/epel/6/x86_64
    gpgcheck=0
    enabled=1

    [maridaDB]
    name=maridaDB
    baseurl=http://yum.mariadb.org/5.5.36/centos6-amd64/
    gpgcheck=0
    enabled=1

**Note** There are no extra spaces at the beginning of each line in `public.repo` file. If they exist, delete the beginning extra spaces. Downloading packages from the internet sometimes may be quit slow. You could for example set `keepcache=1` in /etc/yum.conf, then you can find all the downloaded RPM packages under /var/cache/yum directory. Then you can use these packages to build a offline repo for VSM.

Then rum:

    yum makecache

##<a name="RPM_Install"></a> VSM RPM Build
After you setup the repo, and make sure it works, then begin you can build the RPMs from source code.

    cd $source_code_path
    ./buildrpm

After building, all the rpms are located in $source_code_path/vsmrepo directory.

## VSM RPM Install

You can use `yum localinstall` to install vsm packages by:

    cd vsmrepo
    yum localinstall python-vsmclient-2014.10-0.7.1.el6.noarch.rpm \
        vsm-dashboard-2014.10-0.7.1.el6.noarch.rpm \
        vsm-2014.10-0.7.1.el6.noarch.rpm \
        vsm-deploy-2014.10-0.7.1.el6.x86_64.rpm

**Note**: vsm-dashboard will use the httpd service to setup Web UI. Sometimes it will conflicts with OpenStack dashboard, so try to install OpenStack dashboard and VSM dashboard into different nodes.


# Installation

Here are the information about the sample installation environment and its roles:

* 1. test1-controll: 192.168.123.4
* 2. test1-storage1: 192.168.123.40, 192.168.124.54, 192.168.125.117
* 3. test1-storage2: 192.168.123.179, 192.168.124.122, 192.168.125.109
* 4. test1-storage3: 192.168.123.193, 192.168.124.59, 192.168.125.77

So we configure the network as below in VSM:

    - Management network: 192.168.123.0/24
    - Ceph public network: 192.168.124.0/24
    - Ceph cluster network: 192.168.125.0/24

**Note**You should set network appending on your netowrk environment or check network settings mentioned before.

## Dependcies
For every node, no matter controller node or storage node. Do steps below:

    - Firstly, assume you've build & install VSM RPM packages as mentioned before.
    - After that, install required services for VSM.
    
        preinstall

## Firewall and SELinux
### Solution 1
1>  Disable SELinux in the file /etc/selinux/config

    SELINUX=disabled

2>  Close the firewall

    service iptables stop

### Solution 2
1> If you want to open selinux, you should run commands below to add policies httpd:

    setsebool -P httpd_can_network_connect 1 &
    chcon -R -h -t httpd_sys_content_t /var/www/html/
    chmod -R a+r /var/www/html/

2> Settings for iptables. You should open these ports on every nodes in VSM.

    22 ssh
    80 http
    443 https for future use
    6789 Ceph Monitor 
    6800:8100 Ceph
    123 ntp
    8778  vsm
    5673  rabbitmq
    35357 keystone
    5000  keysone
    3306 mariadb

Here is one sample configuration `iptables`, take it as references.

    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    -A INPUT -p icmp -j ACCEPT
    -A INPUT -i lo -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 443 -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 6789 -j ACCEPT
    -A INPUT -p tcp -m multiport --dports 6800:8100 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 123 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 8778 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 5673 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 35357 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 5000 -j ACCEPT
    -A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT
    -A INPUT -j REJECT --reject-with icmp-host-prohibited
    -A FORWARD -j REJECT --reject-with icmp-host-prohibited
    COMMIT

##Hosts file

VSM will sync /etc/hosts file from the controller node. Make sure your controller node's /etc/hosts file follows these rules:

    - All the ip address should be listed in /etc/hosts file for very node.
    - Lines with `localhost`, `127.0.0.1` and `::1` should not contains truely hostname.

Take the right version as an example to set your /etc/hosts file in controller-node.

### Right version

    127.0.0.1       localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1             localhost localhost.localdomain localhost6 localhost6.localdomain6
    192.168.123.4 test1-control

    192.168.122.172 test1-storage1
    192.168.123.40 test1-storage1
    192.168.124.54 test1-storage1
    192.168.125.117 test1-storage1

    192.168.122.216 test1-storage2
    192.168.123.179 test1-storage2
    192.168.124.122 test1-storage2
    192.168.125.109 test1-storage2

    192.168.122.167 test1-storage3
    192.168.123.193 test1-storage3
    192.168.124.59 test1-storage3
    192.168.125.77 test1-storage3

**Note**Although 192.168.122.0/24 network is not used by VSM, but you should inclued in /etc/hosts file.

### Wrong version

    127.0.0.1       test1-control localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1             test1-control localhost localhost.localdomain localhost6 localhost6.localdomain6
    192.168.123.4 test1-control

    192.168.123.40 test1-storage1
    192.168.124.54 test1-storage1
    192.168.125.117 test1-storage1

    192.168.123.179 test1-storage2
    192.168.124.122 test1-storage2
    192.168.125.109 test1-storage2

    192.168.122.167 test1-storage3
    192.168.123.193 test1-storage3
    192.168.124.59 test1-storage3
    192.168.125.77 test1-storage3

**Error**:

    - Can not put `hostname` in lines with localhost.
    - Not all the IP address are listed for test1-storage1 and test1-storage2.


## Setup controller node
====================
###Edit the file /etc/manifest/cluster.manifest

**modify three IP addresses**

1>  For vsm controller, edit the file /etc/manifest/cluster.manifest and modify it as described below:

mainly focus on the validity of the three IP addresses, and modify them according to your environment.
`management_addr` is used by VSM to communicate with different services, such as using rabbitmq to transfer messages, rpc.call/rpc.cast etc.`ceph_public_addr` is a public (front-side) network address. `ceph_cluster_addr` is a cluster (back-side) network address.

    [management_addr]
    192.168.123.0/24

    [ceph_public_addr]
    192.168.124.0/24

    [ceph_cluster_addr]
    192.168.125.0/24

###Install

2>  Install vsm controller.

    vsm-controller

**Note**After this command, it will generate a configuration file located in /etc/vsmdeploy/deployrc owned by root. If you want to use the old version of /etc/vsmdeploy/deployrc, you may run `vsm-controller -f /etc/vsmdeploy/deployrc`.

**Warning** Do not set proxy env during installation.

## Setup storage node
### server_manifest
**step 1**
For vsm storage nodes, edit the file `/etc/manifest/server.manifest` and modify it as described below:

    [vsm_controller_ip]
    #10.239.82.168

Update `vsm_controller_ip` to the vsm controller's IP address under subnet `management_addr`

    [vsm_controller_ip]
    192.168.123.4  #refer to test1-controll node.

**step 2*

Generate the `auth_key` by running the following command on the vsm controller node:

    [root@test1-control manifest]# agent-token
    9291376733ec4662929eadcf9eda3b44-e38aeba41c884fc88321ac84028792e4

Then run command below for every storage node:

    replace-str 9291376733ec4662929eadcf9eda3b44-e38aeba41c884fc88321ac84028792e4

**step 3**
Change disks in `/etc/manifest/server_manifest` file appending on your disks. Such as, change lines below:

    [10krpm_sas]
    #format [sas_device]  [journal_device] 
    %osd-by-path-1%   %journal-by-path-1%
    %osd-by-path-2%   %journal-by-path-2%
    %osd-by-path-3%   %journal-by-path-3%

to be:

    [10krpm_sas]
    #format [sas_device]  [journal_device] 
    /dev/sdb /dev/sdc1
    /dev/sdd /dev/sdc2
    /dev/sde /dev/sdf

Then delete the redundant lines with %osd-by-path%, if you have less disks.

**step 4**
Using disk-by-path is better to use for the disk path. Use the command below to find the true by-path:

    ls -al /dev/disk/by-path/* | grep `disk-path` | awk '{print $9,$11}'

Suc as:

    ls -al /dev/disk/by-path/* | grep sdb | awk '{print $9,$11}'
    /dev/disk/by-path/pci-0000:00:0c.0-virtio-pci-virtio3 ../../sdb

Then replace the /dev/sdb with `/dev/disk/by-path/pci-0000:00:0c.0-virtio-pci-virtio3` in `/etc/manifest/server.manifest` file. Also do these steps for all the other disks listed in this file.

**Warning** It may cause an error when you add a disk without by-path. So, If you can not find the by-path for a normal disk, you should not use it. Or if you use it to create cluster, when it fails, please delete from `/etc/manifest/server.manifest` file.

After that the disk list may be changed to as below:

    [10krpm_sas]
    #format [sas_device]  [journal_device]
    /dev/disk/by-path/pci-0000:00:0c.0-virtio-pci-virtio3   /dev/disk/by-path/pci-0000:00:0d.0-virtio-pci-virtio4
    /dev/disk/by-path/pci-0000:00:0e.0-virtio-pci-virtio5   /dev/disk/by-path/pci-0000:00:0f.0-virtio-pci-virtio6
    /dev/disk/by-path/pci-0000:00:10.0-virtio-pci-virtio7   /dev/disk/by-path/pci-0000:00:11.0-virtio-pci-virtio8

**step 5**
If you have several kinds of storage medium, and you want these disks into different storage groups in VSM. You may follow the operations below. Otherwise, you may skip this step and just put all the disks into [10krpm_sas] section.

You may want to add disks into other sections in `/etc/manifest/server.manifest` file. Such as beyong [10krpm_sas] section. Take [ssd] as an example:

1> Add storage class in `/etc/manifest/cluster.manifest` in controller node.

    [storage_class]
    ssd # add this line
    10krpm_sas

2> Add storage group in `/etc/manifest/cluster.manifest` in controller node.

    [storage_group]
    high_performance_test  High_Performance_SSD_test ssd

**Note** No extra spaces in word, use \_ to instead spaces.

3> Add disks under `/etc/manifest/server.manifest` in storage node which has SSD, such as:

    [ssd]
    /dev/disk/by-path/pci-0000:00:0c.0-virtio-pci-virtio9   /dev/disk/by-path/pci-0000:00:0d.0-virtio-pci-virtio1
    /dev/disk/by-path/pci-0000:00:0e.0-virtio-pci-virtio11   /dev/disk/by-path/pci-0000:00:0f.0-virtio-pci-virtio14
    /dev/disk/by-path/pci-0000:00:10.0-virtio-pci-virtio23  /dev/disk/by-path/pci-0000:00:11.0-virtio-pci-virtio10

##Setup VSM for storage node
After the configuration of `/etc/manifest/server.manifest`, you may run:

    vsm-node

to setup storage node.

#Login the webUI

After the command is finished executing, to check if you have setup the controller correctly, do the following steps:

1.  Access http://vsm controller IP/dashboard/vsm.(for example http://192.168.123.4/dashboard/vsm)
2.  User name: admin
3.  Password can be get from: /etc/vsmdeploy/deployrc, the ADMIN_PASSWORD field

        cat /etc/vsmdeploy/deployrc |grep ADMIN_PASSWORD

4.  Then you can switch to `Create Cluster` Panel, and push the create cluster button to create a ceph cluster. Good Luck!
