"""Python scripts. This module is accessed by the scripting CLI. Functions with
names that begin with a '_' are ignored by the CLI and cannot be accessed by the
user.

NOTE: The scripting CLI allows the user to reload this module without restarting
the Python kernel. This is done via the built-in function importlib.reload, which
will overwrite old definitions but will not remove functions that have been deleted.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import ichigo.calc.cmat as ch

from astropy.io import fits
from numpy.typing import NDArray
from ichigo.servers import *
from ichigo.strmanip import print_color, get_timestamp
from ichigo.config import SETTINGS


def update_dmflat(servers_dict: dict[str, Server], path_old_rtc: str, path_new_rtc: str,
                  rtc_alias: str = "rtc", ehu_alias: str = "ehu") -> None:
    """Creates a new DM flat in the ~/cals/ directory of the RTC.

    Parameters
    ----------
    servers_dict: dict of ichigo.servers.Server or a child of this class
        Defines a mapping between aliases and Server object. For example,
        {"rtc": instance of ImakaRTCServer}
    path_old_rtc: str
        Path of the file containing the old flat commands on the RTC.
    path_new_rtc: str
        Path of the new file to save to on the RTC.
    rtc_alias: str, optional
        Alias of the RTC in servers_dict.
    ehu_alias: str, optional
        Alias of ehu (the telemetry server) in servers_dict.

    Returns
    -------
    None
    """
    # Need ehu to save telemetry and data from the RTC
    rtc = servers_dict[rtc_alias]
    ehu = servers_dict[ehu_alias]
    assert isinstance(rtc, ImakaRTCServer), "rtc must be an instance of ImakaRTCServer"
    assert isinstance(ehu, EhuServer), "ehu must be an instance of EhuServer"

    print("Saving 'imaka data and copying to local...")
    newcmd = ehu.get_average_actuator_cmd()
    print("Copying old flat commands to local...")
    path_oldflat_local = SETTINGS["RESOURCES"]["dm_flat"]
    rtc.sftp_get(path_old_rtc, path_oldflat_local)

    # Add the commands together
    oldflat = fits.getdata(path_oldflat_local)
    newflat = oldflat + newcmd
    
    # Save the data and SFTP the file to the RTC
    print("Saving new flat commands to RTC...")
    hdu = fits.PrimaryHDU(newflat)
    hdu.writeto(SETTINGS["RESOURCES"]["dm_flat"], overwrite=True)
    rtc.sftp_put(SETTINGS["RESOURCES"]["dm_flat"], path_new_rtc)


def generate_cacofoni(servers_dict: dict[str, Server], gain: float, leak: float, 
                      pbgain: float, minfreq: float, maxfreq: float, synth: bool,
                      filternmodes: int = 1, n_aocb: int = 3,
                      rtc_alias: str = "rtc", ehu_alias: str = "ehu",
                      **kwargs) -> tuple[NDArray, NDArray]:
    """Makes a CACOFONI cmat and sends to it to the RTC.

    This assumes that the appropriate playback buffer is loaded into the RTC.

    Parameters
    ----------
    servers_dict: servers_dict: dict of asmtools.servers.network.Server or a child of this class
        Defines a mapping between aliases and Server object. For example,
        {"rtc": instance of ImakaRTCServer}
    n_aocb: int, optional
        Number of aocbs to average over.
    rtc_alias: str, optional
        Alias of the RTC in servers_dict.
    ehu_alias: str, optional
        Alias of ehu (the telemetry server) in servers_dict.

    Returns
    -------
    imat: nd_array
        Interaction matrix.
    cmat: nd_array
        Control matrix.
    """
    # So we don't accidentally request a very large number of telemetry files...
    assert n_aocb < 10, "Number of requested telemetry files must be < 10"

    # Need ehu to save telemetry and data from the RTC
    rtc = servers_dict[rtc_alias]
    ehu = servers_dict[ehu_alias]
    assert isinstance(rtc, ImakaRTCServer), "rtc must be an instance of ImakaRTCServer"
    assert isinstance(ehu, EhuServer), "ehu must be an instance of EhuServer"

    # Get telemetry
    rtc.set_loop_pid(gain, leak, pbgain)
    fnames, indices = ehu.save_aocbs_autoidx(n_aocb)
    aocb_data, fns_aocb = ehu.get_aocbs_by_index(indices)

    # Create CACOFONI matrices using Olivier's IDL routines
    fn_imat = "imat.cacofoni." + get_timestamp(date_only=True) + ".fits"
    fn_cmat = "cmat.cacofoni." + get_timestamp(date_only=True) + ".fits"
    path_local_imat = os.path.join(SETTINGS["PATHS"]["temp"], fn_imat)
    path_local_cmat = os.path.join(SETTINGS["PATHS"]["temp"], fn_cmat)

    imat = ch.make_cacophony_imat(fns_aocb, minfreq, maxfreq, fn_out=path_local_imat, **kwargs)
    cmat = ch.make_cmat_from_imat(imat, synth, filternmodes=filternmodes, fn_out=path_local_cmat)

    # SFTP files to the RTC
    path_rtc_imat = rtc.cals_path + fn_imat
    path_rtc_cmat = rtc.cals_path + fn_cmat
    rtc.sftp_put(fn_imat, path_rtc_imat)
    rtc.sftp_put(fn_cmat, path_rtc_cmat)
    print_color("CACOFONI cmat saved to the RTC in: " + path_rtc_cmat, "green")

    rtc.open_loop_noleak()
    return imat, cmat


def _compute_strehl(servers_dict: dict[str, Server]) -> tuple[float, NDArray]:
    """Takes an image and shows it with the computed Strehl ratio.

    Parameters
    ----------
    None

    Returns
    -------
    strehl: float
        The Strehl ratio.
    img: nd_array
        Image used to compute the Strehl ratio.
    """
    return (0, np.zeros(1))