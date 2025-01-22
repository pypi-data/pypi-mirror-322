"""
TODO:
- maybe just listen to a socket and get rid of Pyro stuff?
"""

import os
import time
import ichigo.images as images

from astropy.io import fits
from numpy.typing import NDArray
from ichigo.servers.server import Server
from ichigo.strmanip import print_color
from ichigo.config import SETTINGS

class WindowsNUCServer(Server):
    """Communicates with a Windows machine that hosts software for the camera
    and HASO WFS. The camera is controlled by SharpCap 4.0.
    """
    def __init__(self, alias: str, host_name: str | None = None, jumps: list[str] = []) -> None:
        """Initializes the WindowsNUCServer.

        Parameters
        ----------
        See :class:`servers.server.Server`.

        Returns
        -------
        None
        """
        super().__init__(alias, host_name=host_name, os_type='windows', jumps=jumps)
        # Path to SharpCap scripts on the NUC
        self.path_scripts = "C:\\Users\\imaka\\Documents\\SharpCap\\scripts\\"
        self.path_spinview = "C:\\Users\\imaka\\Documents\\SpinView_auto\\"
        
        print_color("Created WindowsNUCServer. Please manually start SharpCap and the Pyro4 name server." \
              , "magenta")
    
    def spinview_capture_images(self, n: int, **kwargs) -> fits.HDUList:
        """Returns n images captured with SpinView.

        Parameters
        ----------
        n: int
            Number of images to capture.
        **kwargs:
            See capture_image.c.
        
        Returns
        -------
        out: fits.HDUList
            FITS data of the images.
        """
        assert n / n == 1, "n must be an integer"
        assert n > 0, "n must be greater than 0"
        n = int(n)

        # Set remote absolute path for output file
        path_remote = self.path_spinview + "images\\temp.fits"
        # Make the commmand string
        cmd = self.path_spinview + "capture_image.exe"
        cmd += " -f " + path_remote
        cmd += " -n " + str(n)
        if len(kwargs) > 0:
            cmd += " --"
            for key, value in kwargs:
                cmd += " -c " + key + "=" + str(value)
        self.execute(cmd)

        path_local = os.path.join(SETTINGS["PATHS"]["temp"], "spinview.fits")
        self.sftp_get(path_remote, path_local)
        return fits.open(path_local)

    def sharpcap_get_camera_names(self) -> None:
        """Prints a list containing the names of all of the cameras connected to
        the SharpCap software. The output of this function can be used to determine
        which camera index to use. out[i] corresponds to index i when calling the
        function set_camera in this module.
        """
        # Format command for the python script
        cmd = "python " + self.path_scripts + "get_camera_names.py"
        self.execute(cmd)

    def sharpcap_set_camera(self, idx: int) -> None:
        """Sets the active camera. The output format is set to fits by default.
        Use the method sharpcap_set_output_format to change the format.

        This function calls the script set_camera.py.

        Parameters
        ----------
        idx: int
            Index of the camera. Use SharpCapServer.get_camera_names to find this,
            if need be. If idx == -1, the camera is closed.
        
        Returns
        -------
        None
        """
        # Format command for the python script
        cmd = "python " + self.path_scripts + "set_camera.py"
        # Add arguments
        cmd += " -i " + str(idx)
        self.execute(cmd)

    def sharpcap_set_output_format(self, format: str) -> None:
        """Sets the output format of saved files.

        This function calls the script set_output_format.py.

        Parameters
        ----------
        format: str
            Determines the output format of the files, which is fits by default.
            Set to fits, png, or tif.

        Returns
        -------
        None
        """
        # Format command for the python script
        cmd = "python " + self.path_scripts + "set_output_format.py"
        # Add arguments
        cmd += " -f " + str(format)
        self.execute(cmd)

    def sharpcap_capture_single_frame(self, fnout: str, t: float, g: float = 1) -> str:
        """Saves a single image and returns the absolute directory of the image.
        The image is saved to fnout in the directory PATH_SING_IMAGES.

        Parameters
        ----------
        fnout: str
            Name of the output file WITHOUT an extension. The extension will be
            appended automatically depending on the output format set. If you want
            to change to output format, use the method sharpcap_set_output_format().
        t: float
            Exposure time in milliseconds.
        g: float, optional
            The gain.

        Returns
        -------
        out: str
            Remote path to the saved image.
        """
        # Format command for the python script
        cmd = "python " + self.path_scripts + "capture_single_frame.py"
        # Add arguments
        cmd += " -fo " + fnout
        cmd += " -t " + str(t)
        cmd += " -g " + str(g)
        # Identify the output directory
        result = self.execute(cmd)
        fn_out = self._find_sharpcap_output(result)
        return fn_out
        
    def sharpcap_capture_sequence(self, fout: str, n_frames: int, t: float, g: float = 1,
                                   fast: bool = True) -> None:
        """Saves a sequence of images. The image is saved under the folder fout
        in the directory PATH_SEQ_IMAGES.
        
        Unfortunately, it is difficult to get this function to return the remote
        directory of the saved images because of a bug in SharpCap's internal Python
        module.

        Parameters
        ----------
        fout: str
            Name of the output folder. Any spaces will be replaced by an underscore.
        n_frames: int
            Number of frames to capture.
        t: float
            Exposure time in milliseconds.
        g: float, optional
            The gain.
        fast: bool, optional
            If True, uses execute_fast to execute the command. I.e., do not wait
            for this sequence to finish before terminating this function.

        Returns
        -------
        None
        """
        # Format command for the python script
        cmd = "python " + self.path_scripts + "capture_sequence.py"
        # Add arguments
        cmd += " -fo " + fout.replace(' ', '_')
        cmd += " -n " + str(n_frames)
        cmd += " -t " + str(t)
        cmd += " -g " + str(g)
        if fast:
            self.execute_fast(cmd)
            print_color("Started sequence. Waiting a few seconds for it to go through...", "yellow")
            time.sleep(5)
        else:
            self.execute(cmd)
    
    def sharpcap_get_one_image(self, t: float, g: float = 1) -> NDArray:
        """Returns a single frame from the camera. This function runs the method
        sharpcap_capture_single_frame(), scps the file to a temporary directory
        on the machine running this package, and imports it to Python as a numpy
        array.

        Parameters
        ----------
        t: float
            Exposure time in milliseconds.
        g: float, optional
            The gain.

        Returns
        -------
        out: nd_array
            The most recent frame from the camera.
        """
        path_remote = self.sharpcap_capture_single_frame("junk_sharpcap", t, g)
        # SFTP this file to the temporary directory
        fname = path_remote.split('\\')[-1]
        path_local = os.path.join(SETTINGS["PATHS"]["temp"], fname)
        self.sftp_get(path_remote, path_local)
        # Import this image as a numpy array
        img = images.get_image(path_local)
        return img
    
    def _find_sharpcap_output(self, term_out: str) -> str:
        """Returns the output from the terminal filtered to locate the output
        path of SharpCap files..

        Parameters
        ----------
        term_out: str
            Output from the terminal.
        
        Returns
        -------
        out: str or None
            The filtered output.
        """
        lines = term_out.split('\n')  # split by newline
        prefix = SETTINGS["WINDOWS"]["sharpcap_prefix"]
        for i, line in enumerate(lines):
            # Check each line and see which one contains the correct prefix. Can't
            # use str.startswith because the raw strings contain a ton of escape
            # characters.
            if prefix in line:
                # Split the string according to the prefix, but only get everything
                # after the prefix
                remote_out = line.split(prefix)[1]
                # If the last character is '\r', it means the string continued to
                # the next line.
                if remote_out.endswith('\r'):
                    # Remove \r from the end of the output
                    remote_out = remote_out[:-1]
                    # Get the next line
                    next_line = lines[i+1]
                    # Remove ANSI escape sequence - split this string by finding
                    # '\x1b', and taking all of the characters before that
                    remote_out += next_line.split('\x1b')[0]
                return remote_out
        raise ValueError("Could not find the output path of the saved image.")