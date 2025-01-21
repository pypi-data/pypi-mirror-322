__version__ = "0.0.8"

import subprocess


def get_hostname():
    """Retrieve the hostname of the machine/cluster."""
    # Execute the hostname command
    name = subprocess.check_output(
        "hostname", shell=True, text=True
    ).strip()
    name = '.'.join(name.split('.')[1:])

    locations = {
        'nmr.mgh.harvard.edu': 'MGH',
    }

    if name in locations:
        name = 'MGH'
    else:
        name = 'UNKNOWN'
    return name


HOSTNAME = get_hostname()
