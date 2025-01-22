"""Class for managing state of the AO system
"""

import sched
import time
import numpy as np

from numpy.typing import NDArray
from ichigo.strmanip import print_color
from ichigo.servers import create_server, ImakaRTCServer, TelescopeServer, EhuServer
from ichigo.managers import Manager
from ichigo.config import SETTINGS

class StateManager(Manager):
    """Regularly checks the state of the system. Performs telescope offsets to
    offload tip/tilt and opens the loop if the DM is saturating.
    """
    def __init__(self, t_update, ehu_alias: str = "ehu", rtc_alias: str = "rtc", tcs_alias: str = "max") -> None:
        """Initializes the StateManager object.

        Parameters
        ----------
        ehu_alias: str, optional
            Alias for server used to retrieve and operate on AO telemetry. Server
            type must be EhuServer.
        rtc_alias: str, optional
            Alias for server hosting the RTC. This is used to open the loop and
            leak off voltages if the DM in emergencies. Server type must be
            ImakaRTCServer or EhuServer.
        tcs_alias: str, optional
            Alias for server that should be used to communicate with the TCS.
            Set to "max" by default for IRTF.
        
        Returns
        -------
        None
        """
        super().__init__()

        self.t_update = t_update

        # Add the relevant servers
        expected_types = {
            rtc_alias: ImakaRTCServer,
            ehu_alias: EhuServer,
            tcs_alias: TelescopeServer
            }

        for alias, server_type in expected_types.items():
            server = create_server(alias)
            assert isinstance(server, server_type), f"{alias} server must be of type {server_type}"
            self.add_server(alias, server)

        self.ehu: EhuServer = self.get_server(ehu_alias)
        self.rtc: ImakaRTCServer = self.get_server(rtc_alias)
        self.tcs: TelescopeServer = self.get_server(tcs_alias)

        print_color("Created StateManager. Make sure that each server is connected." \
                    , "magenta")

    def run(self) -> None:
        """Begins running the StateManager. Once this method is executed, the
        StateManager will run continuously until the program is forced to stop.
        """
        # Initialize the scheduler and schedule one call to check_state. Because
        # check_state will schedule another call to itself, this causes it to
        # run continuously
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(self.t_update, 1, self.check_state, (scheduler,))
        print_color("Starting now. The state of the system will be checked continously" 
                    + " until this program is terminated.", "green")
        scheduler.run()
    
    def check_state(self, scheduler: sched.scheduler) -> None:
        """Checks the state of the system.

        Parameters
        ----------
        scheduler: sched.scheduler
            An event scheduler.

        Returns
        -------
        None
        """
        print_color("Checking state...", "yellow")
        # Schedule the next call to this function
        scheduler.enter(self.t_update, 1, self.check_state, (scheduler, ))
        # Get average actuator commands via ehu
        c_act = self.ehu.get_average_actuator_cmd()
        # See if DM is saturating
        #if np.max(np.abs(c_act)) > 0.5:
        #    self.rtc.panic()
        # Tip/tilt offsets
        print_color("Computing telescope offsets...", "yellow")
        dra, ddec = self.calc_tel_offset(c_act)
        print(dra, ddec)
        #self.tcs.offset_rel(dra, ddec)
        #print_color("Done", "yellow")

    def calc_tel_offset(self, c_act: NDArray) -> tuple[float, float]:
        """Returns the required RA, Dec offsets to zero the tip/tilt on the DM.

        Parameters
        ----------
        c_act: nd_array
            Actuator commands.

        Returns
        -------
        ra: float
            RA offset in arcseconds.
        dec: float
            Dec offset in arcseconds.
        """
        # Convert actuator commands to Noll Zernike coefficients on the surface
        # of the DM
        n_act = SETTINGS["AO"]["n_actuators"]
        c_act = c_act[:n_act]  # remove excess channels
        a_z = np.dot(self.rtc.a2z, c_act)
        # Convert to RA, Dec offsets and apply the negative sign
        surf2radec = SETTINGS["AO"]["NollSurface_to_RADec"]
        dra, ddec = -1 * np.dot(surf2radec, a_z[:2])
        return dra, ddec
