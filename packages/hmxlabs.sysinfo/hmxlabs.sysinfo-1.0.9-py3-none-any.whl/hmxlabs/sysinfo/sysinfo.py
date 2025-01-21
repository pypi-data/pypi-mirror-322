import os
import sys
import psutil
import json
import argparse
from cpuinfo import get_cpu_info

KEY_CLOCK_SPEED = "hz_advertised"
KEY_CLOCK_SPEED_ACTUAL = "hz_actual"

def get_diskinfo():
    disks = psutil.disk_partitions(all=False)

    results = []
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        disk_res = {
                        "device": disk.device,
                        "mount_point": disk.mountpoint,
                        "size": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent_used": usage.percent
        }
        results.append(disk_res)

    return results

def get_clock_speed(key: str, cpu_info):
    """Gets the clock speeds from the CPU Info object. For some reason on ARM platforms this isn't
    available and so needs to be accounted for"""
    
    if key not in cpu_info:
        return 0
    
    return cpu_info[key][0]

def get_cache_size(key: str, cpu_info):
    """Gets the cache sizes from the CPU Info object. This isn't always available and also is sometimes returned a numerical value
    and sometimes as a string with a suffix such as MiB or KiB. This function will attempt to convert the string to a numerical value.
    The odd thing is the py_cpuinfo library should already have done this, the code is there but for some reaon it doesn't work 
    on some rare occassions such as on a "Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz where the l1_data_cache_size ends up being
    reported as l1_data_cache_size": "1.1 MiB
    
    Should really be fixed in py_cpuinfo but the maintainer, as of March 2024, has stated he will no longer be maintaining the library.
    Might be an idea to simply fork it at this point and retain only the parts required for this project."""
    
    if key not in cpu_info:
        return 0
    
    cache_size = cpu_info[key]
    try:
        int_cache_size = int(cache_size)
        return int_cache_size
    except Exception:
        pass
    

    # This code is lifted from the py_cpuinfo library.
    cache_size_lower = cache_size.lower()
    size_formats = [
            {'gib' : 1024 * 1024 * 1024},
            {'mib' : 1024 * 1024},
            {'kib' : 1024},

            {'gb' : 1024 * 1024 * 1024},
            {'mb' : 1024 * 1024},
            {'kb' : 1024},

            {'g' : 1024 * 1024 * 1024},
            {'m' : 1024 * 1024},
            {'k' : 1024},
            {'b' : 1}
    ]

    try:
        for size_format in size_formats:
            pattern = list(size_format.keys())[0]
            multiplier = list(size_format.values())[0]
            if cache_size_lower.endswith(pattern):
                return int(cache_size_lower.split(pattern)[0].strip()) * multiplier
    except Exception as exp:
        pass

    return 0


def get_sysinfo() -> dict:
    cpu_count = os.cpu_count()
    cpu_info = get_cpu_info()
    core_count = psutil.cpu_count(logical=False)  # This will get the number of physical CPUs regardless of whether HT/ SMT is enabled or not
    smt_on = cpu_count > core_count
    mem = psutil.virtual_memory()
    cpu_f = psutil.cpu_freq(percpu=False)
    cpu_freq = get_clock_speed(KEY_CLOCK_SPEED, cpu_info)
    cpu_freq_act = get_clock_speed(KEY_CLOCK_SPEED_ACTUAL, cpu_info)
    cpu_freq_min = 0
    cpu_freq_max = 0
    if hasattr(cpu_f, "min"):
        cpu_freq_min = cpu_f.min

    if hasattr(cpu_f, "max"):
        cpu_freq_max = cpu_f.max

    disks = get_diskinfo()


    results = {
        "arch": cpu_info.get("arch", "unknown"),
        "smt_on": smt_on,
        "core_count": core_count,
        "cpu_count": cpu_count,
        "cpu_vendor":  cpu_info.get("vendor_id_raw", "unknown"),
        "cpu_model": cpu_info.get("brand_raw", "unknown"),
        "cpu_frequency": cpu_freq,
        "cpu_frequency_actual": cpu_freq_act,
        "cpu_freq_min": cpu_freq_min,
        "cpu_freq_max": cpu_freq_max,
        "installed_memory":  mem.total,
        "l3_cache_size": get_cache_size("l3_cache_size", cpu_info),
        "l2_cache_size": get_cache_size("l2_cache_size", cpu_info),
        "l1_data_cache_size": get_cache_size("l1_data_cache_size", cpu_info),
        "l1_instruction_cache_size": get_cache_size("l1_instruction_cache_size", cpu_info),
        "l2_cache_line_size": get_cache_size("l2_cache_line_size", cpu_info),
        "l2_cache_associativity": get_cache_size("l2_cache_associativity", cpu_info),
        "cpu_flags": cpu_info.get("flags", []),
        "disks": disks
    }

    return results



def main():
    argparser = argparse.ArgumentParser(description="HPC Mark Benchmarking and Pricing Tool",
                                        epilog="(C) HMx Labs Limited 2023. All Rights Reserved.")
    argparser.add_argument('--file', dest="file", required=False, action="store_true", default=False,
                            help="Specify if the output should be written to file")
    argparser.add_argument('--stdout', dest="stdout", required=False, action="store_true", default=True,
                            help="Specify if the output should be written to file")
    argparser.add_argument('--filename', dest="filename", required=False, default="sysinfo.json",
                            help="Specify if the output should be written to file")
                            
    args = None
    out_file = False
    out_stdouf = True
    filename = "sysinfo.json"
    try:
        args = argparser.parse_args()
        out_file = args.file
        out_stdouf = args.stdout
        filename = args.filename
    except Exception:
        argparser.print_help()
        sys.exit(1)

    try:
        results = get_sysinfo()

        if out_stdouf:
            print(json.dumps(results, indent=4))

        if out_file:
            with open(filename, 'w') as res_file:
                res_file.write(json.dumps(results))

    except Exception as exp:
        print(f"Error obtaining System information {exp}", file=sys.stderr)


if __name__ == "__main__":
    main()