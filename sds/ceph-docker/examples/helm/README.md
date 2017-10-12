# Ceph Helm
Authors: Hee Won Lee <knowpd@research.att.com> and Yu Xiang <yxiang@research.att.com>    
Created on 10/1/2017  
Adapted for Ubuntu 16.04 and Ceph Luminous  
Based on https://github.com/ceph/ceph-docker/tree/master/examples/helm  

### Qucikstart

Assuming you have a Kubeadm managed Kubernetes 1.7+ cluster and Helm 2.6.1 setup, you can get going straight away! [1]

1. Install helm and tiller
```
curl -O https://storage.googleapis.com/kubernetes-helm/helm-v2.6.1-linux-amd64.tar.gz
tar xzvf helm-v2.6.1-linux-amd64.tar.gz 
sudo cp linux-amd64/helm /usr/local/bin

helm init       # or helm init --upgrade
helm serve &
```

2. Run ceph-mon, mgr, etc. 
```
./create-secret-kube-config.sh
./helm-install-ceph.sh ceph
```

3. Run an OSD chart
- Usage:
```
./helm-install-ceph-osd.sh <node_label> <osd_device>
```

- Example:
   - bluestore:
   ```
   ./helm-install-ceph-osd.sh voyager1 /dev/sdc
   ```

   - filestore
   ```
   OSD_FILESTORE=1 ./helm-install-ceph-osd.sh voyager1 /dev/sdc
   ```

   - filestore with journal (recommended for production environment)
   ```
   OSD_FILESTORE=1 OSD_JOURNAL=/dev/sdb1 ./helm-ceph-osd.sh voyager1 /dev/sdc
   ```
      
      - NOTE: Use `diskpart.sh` to prepare for journal disk partitions in each host.
         Example: Create 8 journal partitions in /dev/sdb with the size of 10GiB.
         ```
         ./diskpart.sh /dev/sdb 10 1 8 ceph-journal 
         ```
   
### Namespace Activation

To use Ceph Volumes in a namespace a secret containing the Client Key needs to be present.

Once defined you can then activate Ceph for a namespace by running:
```
./activate-namespace.sh default
```

Where `default` is the name of the namespace you wish to use Ceph volumes in.

### Functional testing

Once Ceph deployment has been performed you can functionally test the environment by running the jobs in the tests directory, these will soon be incorporated into a Helm plugin, but for now you can run:

```
kubectl create -R -f tests/ceph
```


#### Notes
[1] You actually need to have the nodes setup to access the cluster network, and `/etc/resolv.conf` setup similar to the following:
```
$ cat /etc/resolv.conf
nameserver 10.96.0.10		# K8s DNS IP
nameserver 135.207.240.13	# External DNS IP; You would have a different IP.
search ceph.svc.cluster.local svc.cluster.local cluster.local client.research.att.com research.att.com
```

[2] To generate ceph keys, `ceph/templates/jobs/job.yaml` uses a docker image created by `docker-image-kubectl-ubuntu-16.04/Dockerfile`.

[3] Setting Up RBAC
Kubernetes >=v1.6 makes RBAC the default admission controller. OpenStack
Helm does not currently have RBAC roles and permissions for each
component so we relax the access control rules:
   ```
   kubectl update -f https://raw.githubusercontent.com/openstack/openstack-helm/master/tools/kubeadm-aio/assets/opt/rbac/dev.yaml
   ```
