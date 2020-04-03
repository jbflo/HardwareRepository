"""
FLEX HCD maintenance mockup.
"""
from HardwareRepository.BaseHardwareObjects import Equipment


TOOL_FLANGE, TOOL_UNIPUCK, TOOL_SPINE, TOOL_PLATE, TOOL_LASER, TOOL_DOUBLE_GRIPPER = (
    0,
    1,
    2,
    3,
    4,
    5,
)

TOOL_TO_STR = {
    "Flange": TOOL_FLANGE,
    "Unipuck": TOOL_UNIPUCK,
    "Rotat": TOOL_SPINE,
    "Plate": TOOL_PLATE,
    "Laser": TOOL_LASER,
    "Double": TOOL_DOUBLE_GRIPPER,
}


class FlexHCDMaintenance(Equipment):

    __TYPE__ = "FLEX_HCD"
    NO_OF_LIDS = 3

    """
    """

    def __init__(self, *args, **kwargs):
        Equipment.__init__(self, *args, **kwargs)

    def init(self):
        self._sc = self.getObjectByRole("sample_changer")

    def get_current_tool(self):
        return self._sc.get_gripper()

    def _do_abort(self):
        """
        Abort current command

        :returns: None
        :rtype: None
        """
        return self._sc._do_abort()

    def _do_home(self):
        """
        Abort current command

        :returns: None
        :rtype: None
        """
        self._sc._do_abort()
        return self._sc._do_reset()

    def _do_reset(self):
        """
        Reset sample changer

        :returns: None
        :rtype: None
        """
        self._sc._do_reset()

    def _do_defreeze_gripper(self):
        """
        :returns: None
        :rtype: None
        """
        self._sc.defreeze()

    def _do_change_gripper(self):
        """
        :returns: None
        :rtype: None
        """
        self._sc.change_gripper()

    def _do_reset_sample_number(self):
        """
        :returns: None
        :rtype: None
        """
        self._sc.reset_loaded_sample()

    def _update_global_state(self):
        state_dict, cmd_state, message = self.get_global_state()
        self.emit("globalStateChanged", (state_dict, cmd_state, message))

    def get_global_state(self):
        """
        """
        state = self._sc._read_state()
        ready = self._sc._is_device_busy()
        running = state in ("RUNNING",)

        state_dict = {"running": running, "state": state}

        cmd_state = {
            "home": True,
            "defreeze": True,
            "reset_sample_number": True,
            "change_gripper": True,
            "abort": True,
        }

        message = ""

        return state_dict, cmd_state, message

    def get_cmd_info(self):
        """ return information about existing commands for this object
           the information is organized as a list
           with each element contains
           [ cmd_name,  display_name, category ]
        """
        """ [cmd_id, cmd_display_name, nb_args, cmd_category, description ] """
        cmd_list = [
            [
                "Actions",
                [
                    ["home", "Home", "Actions"],
                    ["defreeze", "Defreeze gripper", "Actions"],
                    ["reset_sample_number", "Reset sample number", "Actions"],
                    ["change_gripper", "Change Gripper", "Actions"],
                    ["abort", "Abort", "Actions"],
                ],
            ]
        ]
        return cmd_list

    def send_command(self, cmdname, args=None):
        tool = self.get_current_tool()

        if cmdname in ["home"]:
            self._do_home()
        if cmdname in ["defreeze"]:
            self._do_defreeze_gripper()
        if cmdname in ["reset_sample_number"]:
            self._do_reset_sample_number()
        if cmdname == "change_gripper":
            self._do_change_gripper()
        if cmdname == "abort":
            self._do_abort()

        return True
