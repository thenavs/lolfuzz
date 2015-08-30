from pysphere import VIServer, VITask
from pysphere.resources import VimService_services as VI
from pysphere.resources.vi_exception import VIApiException
import sys
import socket

class Specs(object):
    @staticmethod
    def get_boot_order_spec(empty=False):

        # type: VirtualMachineBootOptions
        _def = VI.ns0.VirtualMachineBootOptions_Def("boot_options")
        boot_options = _def.pyclass()

        if empty:
            boot_options.set_element_bootOrder([0])
            return boot_options

        # type: VirtualMachineBootOptionsBootableCdromDevice
        _def = VI.ns0.VirtualMachineBootOptionsBootableCdromDevice_Def("cdrom")
        cdrom = _def.pyclass()

        boot_options.set_element_bootOrder([cdrom])
        return boot_options


class Vcenter(object):
    def __init__(self, vcenter, username, password):
        self.server = VIServer()
        self.server.connect(vcenter, username, password)


class VmManager(object):
    def __init__(self, vcenter, vmname):
        self.vcenter = vcenter
        self.vmname = vmname
        self.vm = self.vcenter.server.get_vm_by_name(vmname)
                                                                                                                                 
    def set_boot_cd(self):
        self.reconfigure(Specs.get_boot_order_spec())

    def set_boot_default(self):
        self.reconfigure(Specs.get_boot_order_spec(True))

    def reconfigure(self, spec_content, sync=True):
        try:
            request = VI.ReconfigVM_TaskRequestMsg()
            _this = request.new__this(self.vm._mor)
            _this.set_attribute_type(self.vm._mor.get_attribute_type())
            request.set_element__this(_this)
            spec = request.new_spec()
            spec.set_element_bootOptions(spec_content)
            request.set_element_spec(spec)
            task = self.vm._server._proxy.ReconfigVM_Task(request)._returnval
            vi_task = VITask(task, self.vm._server)
            if sync:
                status = vi_task.wait_for_state([vi_task.STATE_SUCCESS,
                                                 vi_task.STATE_ERROR])
                if status == vi_task.STATE_ERROR:
                    raise VIException(vi_task.get_error_message(),
                                      FaultTypes.TASK_ERROR)
                return
            return vi_task
        except (VI.ZSI.FaultException), e:
            raise VIApiException(e)


if __name__ == '__main__':
    import os 
    import sys
    import json
    from time import sleep
    vcenter = Vcenter(os.environ['vsphere_hostname'],
                      os.environ['vsphere_username'],
                      os.environ['vsphere_password'])

    vm_manager = VmManager(vcenter,os.environ['vm_hostname'])
    try:
      vm_manager.set_boot_cd()
      sys.exit(0)
    except Exception as ex:
      print str(ex)
      sys.exit(-1)
    #vm_manager.set_boot_default()
