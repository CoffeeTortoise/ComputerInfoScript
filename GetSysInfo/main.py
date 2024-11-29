import sounddevice as sd
import platform as pt
import psutil as ps
import cpuinfo as cp
import GPUtil as gp
from tabulate import tabulate
from screeninfo import get_monitors


def get_cpu() -> None:
    print('CPU info:')
    print(f'Processor architecture: {pt.machine()}')
    print(f'Processor arch string raw: {pt.processor()}')
    cpu = cp.get_cpu_info()
    print(f'Full CPU name: {cpu['brand_raw']}')
    print(f'Hz Advertised Friendly: {cpu['Hz Advertised Friendly'.lower().replace(' ', '_')]}')
    print(f'Hz Actual Friendly: {cpu['Hz Actual Friendly'.lower().replace(' ', '_')]}')
    print(f'Hz Advertised: {cpu['Hz Advertised'.lower().replace(' ', '_')]}')
    print(f'Hz Actual: {cpu['Hz Actual'.lower().replace(' ', '_')]}')
    print(f'Processor architecture: {cpu['arch']}')
    print(f'CPU bits: {cpu['bits']}')
    print(f'Number of CPUs: {cpu['count']}')
    print(f'L2 Cache Size: {cpu['L2 Cache Size'.lower().replace(' ', '_')]:_} B')
    print(f'L3 Cache Size: {cpu['L3 Cache Size'.lower().replace(' ', '_')]:_} B')
    print(f'Processor family: {cpu['family']}')


def get_comp() -> None:
    memory = ps.virtual_memory()
    k: int = 1e6
    print('Main comp/lap info: ')
    print(f'Operating system: {pt.platform()}')
    print(f'All ram: {memory.total / k:_} MB')
    print(f'Used ram: {memory.used / k:_} MB; {memory.percent} %')
    print(f'Free ram: {memory.free / k:_} MB; {100 - memory.percent} %')
    swap = ps.swap_memory()
    print(f'Total swap: {swap.total / k:_} MB')
    print(f'Used swap: {swap.used / k:_} MB; {swap.percent} %')
    print(f'Free swap: {swap.free / k:_} MB; {100 - swap.percent} %')
    print(f'Disk parititons: {ps.disk_partitions()}')
    disk_mem = ps.disk_usage('/')
    print(f'Total disk memory: {disk_mem.total / k:_} MB')
    print(f'Used disk mem: {disk_mem.used / k:_} MB; {disk_mem.percent} %')
    print(f'Free disk mem: {disk_mem.free / k:_} MB; {100 - disk_mem.percent} %')
    print(f'Users: {ps.users()}')


def get_audio() -> None:
    print('Audio devices:')
    print(sd.query_devices())


def get_gpu() -> None:
    gpus = gp.getGPUs()
    gpus_ls = []
    for gpu in gpus:
        gpus_ls.append((
            gpu.id,
            gpu.name,
            f'{gpu.load*100}%',
            f'{gpu.memoryFree:_}MB',
            f'{gpu.memoryUsed:_}MB',
            f'{gpu.memoryTotal:_}MB',
            f'{gpu.temperature}'
        ))
    table: str = str(tabulate(
        gpus_ls,
        headers=(
            'id',
            'name',
            'load',
            'free memory',
            'used memory',
            'total memory',
            'temperature'
        ),
        tablefmt='pretty'
    ))
    print(table)


def get_screen() -> None:
    for monitor in get_monitors():
        print(f'{monitor.name}: {monitor.width}x{monitor.height}')
    

def main() -> None:
    options = [get_cpu, get_audio, get_comp, get_gpu, get_screen]
    names = ['CPU information', 'Audio devices', 'Main computer information', 'Graphic devices', 'Screen information']
    choice = '  |  '.join([f'[{i}] {option}' for i, option in enumerate(names)])
    num_ls = [str(i) for i in range(len(choice))]
    running: bool = True
    while running:
        print('Enter the option(index) or print something else if you want to quit')
        print(choice)
        user = input()
        if user not in num_ls:
            running = False
            break
        ind = int(user)
        options[ind]()
        

if __name__ == '__main__':
    main()
