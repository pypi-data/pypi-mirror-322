"""Class that retrieves and parses data from FELIX.
"""

import socket
import re
import numpy as np

from numpy.typing import NDArray
from ichigo.servers import Server
from ichigo.servers.ehu import EhuServer
from ichigo.strmanip import print_color, get_timestamp
from ichigo.config import SETTINGS

class FELIXHelperServer(EhuServer):
    """Recieves data from the FELIX data client.
    """
    def __init__(self, alias: str, host_name: str | None = None, jumps: list[str] = []):
        """Initializes the FELIXHelperServer object.

        Parameters
        ----------
        See :class:`ichigo.servers.server.Server`.
        
        Returns
        -------
        None
        """
        super().__init__(alias, host_name, jumps=jumps)

        # Number of points used to define an image in FELIX. Add one to account
        # for the coordinates of the central point that determines the offset
        # of the entire spot pattern
        self.n_points = SETTINGS["FELIX"]["n_spots"] + 1
        self.recent_image = None

    def _process_command(self, command: str) -> tuple[str, list[float], list[float]] | str:
        """Returns a processed command from the FELIX data client. From Charles
        Lockhart.

        Parameters
        ----------
        command: str
            Command from FELIX.

        Returns
        -------
        timestamp: str
            Timestamp of the command.
        X_values: list of float
            List of X values.
        Y_values: list of float
            List of Y values.
        """
        # Define regex to match the command format: points [timestamp] [X1,Y1,X2,Y2,...X10,Y10]
        pattern = r"^points\s+\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+\[([0-9.,\s\-]+)\]$"
        match = re.match(pattern, command.strip())

        if not match:
            return "Invalid command format!"

        # Extract the timestamp and the comma-separated values
        timestamp = match.group(1)  # The first capture group is the timestamp
        values_str = match.group(2)  # The second capture group is the values

        try:
            # Split the values and convert them to float
            values = [float(v) for v in values_str.split(',')]
        except ValueError:
            return "Error: Non-numeric value encountered in coordinates."

        if len(values) != 20:
            return "Error: Expected 10 pairs of X,Y values!"

        # Separate X and Y values
        X_values = values[::2]  # Every second value starting from 0 (X1, X2, ..., X10)
        Y_values = values[1::2]  # Every second value starting from 1 (Y1, Y2, ..., Y10)

        # Print the timestamp and the X,Y pairs neatly
        print(f"Timestamp: {timestamp}")
        for i in range(10):
            print(f"Pair {i + 1}: X = {X_values[i]}, Y = {Y_values[i]}")

        return timestamp, X_values, Y_values

    def _listen_tcp(self) -> tuple[str, list[float], list[float]]:
        """Returns the timestamp, X, and Y values from the FELIX data client.
        Continuously listens for incoming data via TCP until a valid data string
        is recieved.
        """
        host = SETTINGS["FELIX"]["host"]
        port = SETTINGS["FELIX"]["port"]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()

            print(f"TCP Server listening on {host}:{port}")

            while True:
                # Accept a connection
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024).decode()  # Receive and decode the incoming data

                    if not data:
                        break

                    print_color(f"Received command: {data}", "yellow")

                    # Process the received command
                    result = self._process_command(data)

                    if isinstance(result, tuple):       
                        timestamp, X_values, Y_values = result
                        response = f"Timestamp: {timestamp}\nX values: {X_values}\nY values: {Y_values}"
                        # Send back the response and return the parsed data
                        conn.sendall(response.encode())
                        return timestamp, X_values, Y_values

                    response = result
                    conn.sendall(response.encode())                    

    def _listen_udp(self) -> tuple[str, list[float], list[float]]:
        """Returns the timestamp, X, and Y values from the FELIX data client.
        Continuously listens for incoming data via UDP until a valid data string
        is recieved.        
        """
        host = SETTINGS["FELIX"]["host"]
        port = SETTINGS["FELIX"]["port"]
        # Create a UDP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))

            print(f"UDP server listening on {host}:{port}")

            while True:
                # Receive data from the client
                data, addr = s.recvfrom(1024)  # Buffer size is 1024 bytes
                data = data.decode()

                print(f"Received command from {addr}: {data}")

                # Process the received command
                result = self._process_command(data)

                if isinstance(result, tuple):
                    timestamp, X_values, Y_values = result
                    response = f"Timestamp: {timestamp}\nX values: {X_values}\nY values: {Y_values}"
                    s.sendto(response.encode(), addr)
                    return timestamp, X_values, Y_values
                
                response = result  # This will be the error message
                # Send back the response to the client
                s.sendto(response.encode(), addr)

    def listen(self) -> tuple[str, list[float], list[float]]:
        """Returns processed FELIX data. Continuously listens for incoming data
        from the FELIX data client.

        Parameters
        ----------
        None

        Returns
        -------
        timestamp: str
            Timestamp of the command.
        X_values: list of float
            List of X values.
        Y_values: list of float
            List of Y values.
        """
        if SETTINGS["FELIX"]["protocol"] == "TCP":
            return self._listen_tcp()
        elif SETTINGS["FELIX"]["protcol"] == "UDP":
            return self._listen_udp()

        raise RuntimeError("Could not resolve protocol for recieving FELIX data. Check settings.ini.")
    
    def get_slopes(self) -> NDArray:
        """Returns x-, y- slopes of the measured data. The output is ordered so
        that the x-slopes are given before the y-slopes. For example, 4 spots
        (indices 0 through 3) would yield the following slopes:

            out = [sx0, sx1, sx2, sx3, sy0, sy1, sy2, sy3]

        Parameters
        ----------
        None

        Returns
        -------
        out: nd_array of size n_spots*2
            x, y slopes for each of the spots relative to the calibration image.
        """
        return self._get_slopes_imaka()  # test slopes from 'imaka RTC
        # Get points from FELIX
        timestamp, X_values, Y_values = self.listen()
        coords_test = np.array([X_values[:5], Y_values[:5]]).T
        coords_calib = np.array([X_values[5:], Y_values[5:]]).T
        # Subtract out the central point to remove tip/tilt in each set of coordinates
        coords_test = coords_test[1:] - coords_test[0]
        coords_calib = coords_calib[1:] - coords_calib[0]
        print(coords_test)
        print(coords_calib)
        # Convert spot positions to slopes
        slopes = (coords_test - coords_calib) / SETTINGS["FELIX"]["ap_size"]
        return np.reshape(slopes.T, 2 * SETTINGS["FELIX"]["n_spots"])
    
    def _get_slopes_imaka(self) -> NDArray:
        """Returns measured slopes from 'imaka RTC. Use for testing when FELIX
        data is unavailable. Inherit EhuServer in class definition.
        """
        # WFS data are stored in extension 3
        slopes = self.get_imaka_data()[3]
        slopes = slopes.data[0]
        # Flatten the array
        return slopes.flatten()