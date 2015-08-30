## Getting started.

### Installation:

```bash
# grab ansible devel
git clone https://github.com/ansible/ansible.git

# apply vm-floppy patch from @nivanko
cd ansible/lib/ansible/modules/core
git remote add nivanko https://github.com/nivanko/ansible-modules-core.git
git fetch nivanko
git checkout nivanko/feature-virtual-floppy
git rebase origin/devel
cd ../../..
python setup.py install 
```
### Configuration:
#### /etc/ansible/group_vars/all
```yaml
vsphere_hostname: # IP or FQDN of vsphere host
vsphere_username: # vsphere username with permissions to create instances
vsphere_password: # password
```
### Inventory:
Configure x number of fuzz nodes in hosts

### Datastore Access:
This setup logs directly into the esxi host to place a necessary file in the
datastore. This can be easily modified to suit your setup. 

#### Location:


#### Alternatives:


### Creating the workers:
```bash
ansible-playbook example-fuzz.yml
```

### Destroying the workers:

```bash
ansible-playbook example-destroy.yml
```

