'''
Work with virtual machines managed by libvirt
:depends: libvirt Python module

'''
# Import python libs
import re
import subprocess
from xml.dom import minidom
   
# Import libvirt libs
try:
    import libvirt
    HAS_LIBVIRT = True
except ImportError:
    HAS_LIBVIRT = False
    
import yaml
   
# Import salt libs
from salt._compat import StringIO as _StringIO
from salt.exceptions import CommandExecutionError




'''
Virtual Machine State
'''
   
VIRT_STATE_NAME_MAP = {0: 'running',
                       1: 'running',
                       2: 'running',
                       3: 'paused',
                       4: 'shutdown',
                       5: 'shutdown',
                       6: 'crashed'}
   
def __virtual__():
    if not HAS_LIBVIRT:
        return False
    return 'virt'
   
   
def __get_conn():
    try:
        conn = libvirt.open('qemu+tcp://192.168.0.244/system')
#        conn = libvirt.open('qemu+tcp://121.138.109.61/system')
        
    except Exception:
        raise CommandExecutionError(
            'Sorry, {0} failed to open a connection to the libvirt '
        )
    return conn
   

def _get_vm(name):

    conn = __get_conn()
    vm_ = conn.lookupByName(name)
    return vm_
   
   
def _get_dom(vm_):
    conn = __get_conn()
    if vm_ not in list_vms():
        raise CommandExecutionError('The specified libvirt is not present')
    return conn.lookupByName(vm_)
   
   
def _libvirt_creds():
    g_cmd = 'grep ^\s*group /etc/libvirt/qemu.conf'
    u_cmd = 'grep ^\s*user /etc/libvirt/qemu.conf'
    try:
        group = subprocess.Popen(g_cmd,
            shell=True,
            stdout=subprocess.PIPE).communicate()[0].split('"')[1]
    except IndexError:
        group = 'root'
    try:
        user = subprocess.Popen(u_cmd,
            shell=True,
            stdout=subprocess.PIPE).communicate()[0].split('"')[1]
    except IndexError:
        user = 'root'
    return {'user': user, 'group': group}

   
def list_vms():
    vms = []
    vms.extend(list_active_vms())
    vms.extend(list_inactive_vms())
    return vms
   


   
def list_active_vms():
    conn = __get_conn()
    vms = []
    for id_ in conn.listDomainsID():
        vms.append(conn.lookupByID(id_).name())
    return vms
   

   
def list_inactive_vms():
    conn = __get_conn()
    vms = []
    for id_ in conn.listDefinedDomains():
        vms.append(id_)
    return vms
   

   
def vm_info(vm_=None):
    def _info(vm_):
        dom = _get_dom(vm_)
        raw = dom.info()
        return {'cpu': raw[3],
                'cputime': int(raw[4]),
                'disks': get_disks(vm_),
                'maxMem': int(raw[1]),
                'mem': int(raw[2]),
                'state': VIRT_STATE_NAME_MAP.get(raw[0], 'unknown')}
    info = {}
    if vm_:
        info[vm_] = _info(vm_)
    else:
        for vm_ in list_vms():
            info[vm_] = _info(vm_)
    return info
   

   
def vm_state(vm_=None):
    def _info(vm_):
        state = ''
        dom = _get_dom(vm_)
        raw = dom.info()
        state = VIRT_STATE_NAME_MAP.get(raw[0], 'unknown')
        return state
    info = {}
    if vm_:
        info[vm_] = _info(vm_)
    else:
        for vm_ in list_vms():
            info[vm_] = _info(vm_)
    return info
   
   
def node_info():
    conn = __get_conn()
    raw = conn.getInfo()
    info = {'cpucores': raw[6],
            'cpumhz': raw[3],
            'cpumodel': str(raw[0]),
            'cpus': raw[2],
            'cputhreads': raw[7],
            'numanodes': raw[4],
            'phymemory': raw[1],
            'sockets': raw[5]}
    return info
   

   
def get_nics(vm_):
    nics = {}
    doc = minidom.parse(_StringIO(get_xml(vm_)))
    for node in doc.getElementsByTagName('devices'):
        i_nodes = node.getElementsByTagName('interface')
        for i_node in i_nodes:
            nic = {}
            nic['type'] = i_node.getAttribute('type')
            for v_node in i_node.getElementsByTagName('*'):
                if v_node.tagName == 'mac':
                    nic['mac'] = v_node.getAttribute('address')
                if v_node.tagName == 'model':
                    nic['model'] = v_node.getAttribute('type')
                if v_node.tagName == 'target':
                    nic['target'] = v_node.getAttribute('dev')
                # driver, source, and match can all have optional attributes
                if re.match('(driver|source|address)', v_node.tagName):
                    temp = {}
                    for key in v_node.attributes.keys():
                        temp[key] = v_node.getAttribute(key)
                    nic[str(v_node.tagName)] = temp
                # virtualport needs to be handled separately, to pick up the
                # type attribute of the virtualport itself
                if v_node.tagName == 'virtualport':
                    temp = {}
                    temp['type'] = v_node.getAttribute('type')
                    for key in v_node.attributes.keys():
                        temp[key] = v_node.getAttribute(key)
                    nic['virtualport'] = temp
            if 'mac' not in nic:
                continue
            nics[nic['mac']] = nic
    return nics
   
   
def get_macs(vm_):
    macs = []
    doc = minidom.parse(_StringIO(get_xml(vm_)))
    for node in doc.getElementsByTagName('devices'):
        i_nodes = node.getElementsByTagName('interface')
        for i_node in i_nodes:
            for v_node in i_node.getElementsByTagName('mac'):
                macs.append(v_node.getAttribute('address'))
    return macs
   
   
def get_graphics(vm_):
    out = {'autoport': 'None',
           'keymap': 'None',
           'listen': 'None',
           'port': 'None',
           'type': 'vnc'}
    xml = get_xml(vm_)
    ssock = _StringIO(xml)
    doc = minidom.parse(ssock)
    for node in doc.getElementsByTagName('domain'):
        g_nodes = node.getElementsByTagName('graphics')
        for g_node in g_nodes:
            for key in g_node.attributes.keys():
                out[key] = g_node.getAttribute(key)
    return out


   
def get_disks(vm_):
    disks = {}
    doc = minidom.parse(_StringIO(get_xml(vm_)))
    for elem in doc.getElementsByTagName('disk'):
        sources = elem.getElementsByTagName('source')
        targets = elem.getElementsByTagName('target')
        if len(sources) > 0:
            source = sources[0]
        else:
            continue
        if len(targets) > 0:
            target = targets[0]
        else:
            continue
        if target.hasAttribute('dev'):
            qemu_target = ''
            if source.hasAttribute('file'):
                qemu_target = source.getAttribute('file')
            elif source.hasAttribute('dev'):
                qemu_target = source.getAttribute('dev')
            elif source.hasAttribute('protocol') and \
                    source.hasAttribute('name'): # For rbd network
                qemu_target = '%s:%s' %(
                        source.getAttribute('protocol'),
                        source.getAttribute('name'))
            if qemu_target:
                disks[target.getAttribute('dev')] = {\
                    'file': qemu_target}
    for dev in disks:
        try:
            output = []
            qemu_output = subprocess.Popen(['qemu-img', 'info',
                disks[dev]['file']],
                shell=False,
                stdout=subprocess.PIPE).communicate()[0]
            snapshots = False
            columns = None
            lines = qemu_output.strip().split('\n')
            for line in lines:
                if line.startswith('Snapshot list:'):
                    snapshots = True
                    continue
                elif snapshots:
                    if line.startswith('ID'):  # Do not parse table headers
                        line = line.replace('VM SIZE', 'VMSIZE')
                        line = line.replace('VM CLOCK', 'TIME VMCLOCK')
                        columns = re.split('\s+', line)
                        columns = [c.lower() for c in columns]
                        output.append('snapshots:')
                        continue
                    fields = re.split('\s+', line)
                    for i, field in enumerate(fields):
                        sep = ' '
                        if i == 0:
                            sep = '-'
                        output.append(
                            '{0} {1}: "{2}"'.format(
                                sep, columns[i], field
                            )
                        )
                    continue
                output.append(line)
            output = '\n'.join(output)
            disks[dev].update(yaml.safe_load(output))
        except TypeError:
            disks[dev].update(yaml.safe_load('image: Does not exist'))
    return disks

   
def get_xml(vm_):
    dom = _get_dom(vm_)
    return dom.XMLDesc(0)

   