# HMx Labs sysinfo
Platform / OS agnostic (hopefully!) way to get basic information such as disk size, RAM, CPU count, SMT Status

Really nothing clever, just uses psutil and py-cpuinfo under the cover but fairly handy for some of our use cases

Install by running

    python3 -m pip install --upgrade hmxlabs.sysinfo

Can be run from the command line as

    python3 -m hmxlabs.sysinfo [--file] [--filename]

Default behaviour is to output to `stdout`. Using the `--file` switch will output to the default filename of `sysinfo.json`and an alternative filename can be specified with `--filename`

Can be used from python as:

    from hmxlabs.sysinfo import sysinfo

    results = sysinfo.get_sysinfo()

The output results in something like:

    {
        "arch": "X86_64",
        "smt_on": false,
        "core_count": 4,
        "cpu_count": 4,
        "cpu_vendor": "GenuineIntel",
        "cpu_model": "Intel(R) Core(TM) i9-9980HK CPU @ 2.40GHz",
        "cpu_frequency": 2400000000,
        "cpu_frequency_actual": 2400000000,
        "cpu_freq_min": 0.0,
        "cpu_freq_max": 0.0,
        "installed_memory": 8199159808,
        "l3_cache_size": 16777216,
        "l2_cache_size": 1048576,
        "l1_data_cache_size": 131072,
        "l1_instruction_cache_size": 131072,
        "l2_cache_line_size": 256,
        "l2_cache_associativity": 6,
        "cpu_flags": [
            "3dnowprefetch",
            "abm",
            "adx",
            "aes",
            "apic",
            "arat",
            "arch_capabilities",
            "arch_perfmon",
            "avx",
            "avx2",
            "bmi1",
            "bmi2",
            "clflush",
            "clflushopt",
            "cmov",
            "constant_tsc",
            "cpuid",
            "cpuid_fault",
            "cx16",
            "cx8",
            "de",
            "erms",
            "f16c",
            "flush_l1d",
            "fma",
            "fpu",
            "fsgsbase",
            "fxsr",
            "hypervisor",
            "ibpb",
            "ibrs",
            "ibrs_enhanced",
            "invpcid",
            "invpcid_single",
            "lahf_lm",
            "lm",
            "mca",
            "mce",
            "md_clear",
            "mmx",
            "movbe",
            "msr",
            "mtrr",
            "nonstop_tsc",
            "nopl",
            "nx",
            "osxsave",
            "pae",
            "pat",
            "pcid",
            "pclmulqdq",
            "pdpe1gb",
            "pge",
            "pni",
            "popcnt",
            "pse",
            "pse36",
            "rdrand",
            "rdrnd",
            "rdseed",
            "rdtscp",
            "sep",
            "smap",
            "smep",
            "ss",
            "ssbd",
            "sse",
            "sse2",
            "sse4_1",
            "sse4_2",
            "ssse3",
            "stibp",
            "syscall",
            "tsc",
            "tsc_adjust",
            "tsc_deadline_timer",
            "tsc_known_freq",
            "tsc_reliable",
            "tscdeadline",
            "vme",
            "x2apic",
            "xgetbv1",
            "xsave",
            "xsavec",
            "xsaveopt",
            "xsaves",
            "xtopology"
        ],
        "disks": [
            {
                "device": "/dev/sda2",
                "mount_point": "/",
                "size": 115127644160,
                "used": 52791611392,
                "free": 56440627200,
                "percent_used": 48.3
            },
            {
                "device": "/dev/sda1",
                "mount_point": "/boot/efi",
                "size": 535805952,
                "used": 5492736,
                "free": 530313216,
                "percent_used": 1.0
            }
        ]
    }