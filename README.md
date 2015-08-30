## Getting started.
### Configuration:
#### /etc/ansible/group_vars/all
```
vsphere_hostname
vsphere_username
vsphere_password
```
### Inventory:
Configure x number of fuzz nodes in hosts

### Datastore Access:
This setup logs directly into the esxi host to place a necessary file in the
datastore. This can be easily modified to suit your setup. 

#### Location:


#### Alternatives:


### Creating the workers:
```
ansible-playbook example-fuzz.yml
```

### Destroying the workers:

```
ansible-playbook example-destroy.yml
```

