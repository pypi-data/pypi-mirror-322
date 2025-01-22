"""Functions for manipulating control matrices.
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from numpy.typing import NDArray
from ichigo.calc.pupils import make_system_pupil
from ichigo.idlbridge import get_IDL, convert_IDL_kwargs
from ichigo.config import SETTINGS


def piston_filter(cmat: NDArray, z2a: NDArray | None = None, a2z: NDArray | None = None,
                  fn_out: str | None = None) -> NDArray:
    """Applies a piston filter to the control matrix.

    Parameters
    ----------
    cmat: nd_array
        Control matrix.
    z2a: nd_array, optional
        Piston-to-actuator matrix. If None, it is loaded from settings.ini.
    a2z: nd_array, optional
        Actuator-to-piston matrix. If None, it is loaded from settings.ini.
    fn_out: str or None, optional
        File name to save the filtered cmat to, including the file extension. If
        None, the file is not saved.

    Returns
    -------
    out: nd_array
        Control matrix with the piston coefficient zeroed out.
    """
    if not z2a:
        z2a = fits.getdata(SETTINGS["RESOURCES"]["z2a"], ext=0)
    if not a2z:
        a2z = fits.getdata(SETTINGS["RESOURCES"]["a2z"], ext=0)
    
    n_zernikes = a2z.shape[0]
    n_actuators = a2z.shape[1]
    n_channels = cmat.shape[0]
    n_slopes = cmat.shape[1]
    
    if n_actuators != SETTINGS["AO"]["n_actuators"]:
        warnings.warn("Number of actuators in a2z does not match n_actuators in settings.ini")
    if n_channels != SETTINGS["AO"]["n_channels"]:
        warnings.warn("Number of channels in cmat does not match n_channels in settings.ini")
    if n_slopes != 2*SETTINGS["AO"]["n_subaps"]:
        warnings.warn("Number of slopes in cmat does not match 2*n_subaps in settings.ini")

    # Zero out the piston coefficient
    z0 = np.identity(n_zernikes)
    z0[0, 0] = 0
    pf = np.dot(z2a, np.dot(z0, a2z))

    # Crop the cmat to the number of actuators in z2a and apply the piston filter
    cmat = cmat[:n_actuators, :]
    cmat_filtered = np.dot(pf.T, cmat)

    # Pad the result back to match the number of channels in the original cmat
    result = np.zeros((n_channels, n_slopes))
    result[:n_actuators, :] = cmat_filtered
    
    if fn_out:
        hdu = fits.PrimaryHDU(cmat_filtered)
        hdu.header["COMMENT"] = "Piston filtered cmat."
        hdu.writeto(fn_out, overwrite=True)
        
    return cmat


def make_cacophony_imat(fns_aocb: list[str], minfreq: float, maxfreq: float,
                        plot: bool = True, fn_out: str | None = None, **kwargs) -> NDArray:
    """Makes a CACOFONI interaction matrix from 'imaka aocb files.

    Parameters
    ----------
    fns_aocb: list of str
        List aocb file names.
    minfreq: float
        Minimum frequency.
    maxfreq: float
        Maximum frequency.
    plot: bool, optional
        If True, plots the imat.
    fn_out: str or None, optional
        File name to save imat to, including the file extension. If None, the
        file is not saved.
    **kwargs: parameters to make_cacophony.pro
        Optional parameters for the IDL function make_cacophony. See documentation
        for helpers.idlbridge.convert_IDL_kwargs().
        
    Returns
    -------
    out: nd_array 
        Interaction matrix. Expected shape is (n_actuators, 2*n_subaps), but this
        is currently hard-coded in make_cacophony.pro for IRTF-ASM-1.
    """
    assert minfreq < maxfreq, "minfreq must be less than maxfreq"
    minfreq = float(minfreq)
    maxfreq = float(maxfreq)

    IDL = get_IDL()

    # Create interaction matrices
    imats = []
    for i, fn in enumerate(fns_aocb):
        # Create variable name to assign in idl
        varname = "imat" + str(i)
        cmd_str = varname + "=make_cacophony(" + "\'" + fn + "\', " + str(minfreq) \
            + ", " + str(maxfreq)
        # Pass any other arguments
        if len(kwargs) > 0:
            cmd_str += ", " + convert_IDL_kwargs(**kwargs)
        cmd_str += ")"

        IDL.run(cmd_str, stdout=True)
        # Retrieve the variable as a numpy array and store it
        imats.append(eval("IDL." + varname))
        
    # Average all of the imats to get final imat
    imat = np.average(imats, axis=0)
    imat = imat.T
    
    if plot:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
        ax.imshow(imat, cmap="cividis", aspect="auto", origin="lower")
        ax.set_title("imat shape: " + str(imat.shape), fontsize=12)
        plt.show()

    # Unfortunately, the dimensions of imat are hard-coded in the IDL script.
    # Show a warning if it doesn't match the parameters in settings.ini.
    n_channels = SETTINGS["AO"]["n_channels"]
    n_actuators = SETTINGS["AO"]["n_actuators"]
    n_subaps = SETTINGS["AO"]["n_subaps"]
    if (imat.shape[0] != n_channels) and (imat.shape[0] != n_actuators):
        warnings.warn("imat does not match the number of actuators or channels in settings.ini!" \
                      + " Proceed with caution.")
    if imat.shape[1] != 2*n_subaps:
        warnings.warn("imat does not match the number of subapertures in settings.ini!" \
                      + " Proceed with caution.")
    
    if fn_out:
        hdu = fits.PrimaryHDU(imat)
        hdu.header["COMMENT"] = "CACOFONI interaction matrix. Function call: " + cmd_str
        hdu.writeto(fn_out, overwrite=True)

    return imat


def make_cmat_from_imat(imat: NDArray, synth: bool, filternmodes: int = 1, pad: bool = True,
                        plot: bool = True, fn_out: str | None = None) -> NDArray:
    """Returns a control matrix. It is created by inverting the interaction matrix.
    This function may also create a synthetic cmat my fitting the influence functions
    to the data.

    Parameters
    ----------
    imat: nd_array
        Interaction matrix.
    synth: bool
        If True, creates a synthetic cmat. If False, uses empirical data only.
    filternmodes: int, optional
        Number of modes to filter out of the SVD.
    pad: bool, optional
        If True, pads the cmat to match the number of channels.
    plot: bool, optional
        If True, plots the cmat.
    fn_out: str or None, optional
        File name to save cmat to, including the file extension. If None, the
        file is not saved.

    Returns
    -------
    out: nd_array of shape (n_channels, 2*n_subaps)
        Control matrix.
    """
    assert abs(filternmodes)/filternmodes == 1, "filternmodes must be an integer"
    assert filternmodes >= 0, "filternmodes must be greater than or equal to 0"
    filternmodes = int(filternmodes)

    IDL = get_IDL()
    IDL.imat = imat.T

    # Create empirical cmat by inverting imat
    if not synth:
        IDL.run("cmat = invert_svd(imat, filternmodes=" + str(filternmodes) + ")")
        cmat = IDL.cmat
        cmat = cmat.T

    # Synthetic cmat
    else:
        # not implemented yet
        pass
    
    # Pad to match number of channels
    if pad:
        cmat = pad_cmat(cmat)

    if plot:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
        ax.imshow(cmat, cmap="cividis", aspect="auto", origin="lower")
        ax.set_title("cmat shape: " + str(cmat.shape), fontsize=12)
        plt.show()

    if fn_out:
        hdu = fits.PrimaryHDU(cmat)
        hdu.header["SYNTH"] = synth
        hdu.header["MODESFTD"] = filternmodes
        hdu.header["COMMENT"] = "Control matrix."
        hdu.writeto(fn_out, overwrite=True)

    return cmat


def pad_cmat(cmat: NDArray) -> NDArray:
    """Returns a cmat padded with 0s to match the number of channels. The output
    shape is expected to be (2*n_subaps, n_channels). The first dimension of the
    output will match that of the input. If it does not equal to 2*n_subaps, this
    function will show a warning.

    Parameters
    ----------
    cmat: nd_array of shape (k, m)
        Matrix to pad.
    
    Returns
    -------
    out: nd_array of shape (n_channels, m)
        Padded control matrix. m is expected to be equal to 2*n_subaps.
    """
    m, k = cmat.shape

    # Show a warning if it doesn't match settings.ini.
    n_channels = SETTINGS["AO"]["n_channels"]
    n_actuators = SETTINGS["AO"]["n_actuators"]
    n_subaps = SETTINGS["AO"]["n_subaps"]
    if m != 2*n_subaps:
        warnings.warn("cmat does not match the number of subapertures in settings.ini!" \
                      + " Proceed with caution.")
    if (k != n_channels) and (k != n_actuators):
        warnings.warn("cmat does not match the number of actuators or channels in settings.ini!" \
                      + " Proceed with caution.")
    
    # Pad the cmat along the actuator axis
    cmat_padded = np.zeros((m, n_channels))
    cmat_padded[:, :k] = cmat
    return cmat_padded


def make_theoretical_imat(scale=1, rotation=0):
    """Returns a theoretical interaction matrix for the system defined in SETTINGS.ini.

    Parameters
    ----------
    scale: float, optional
        Scale factor.
    rotation: float, optional
        Rotation angle in degrees.

    Returns
    -------
    """
    pupil = make_system_pupil(grid_px=256, grid_size=1.2)
    imat = 1
    return