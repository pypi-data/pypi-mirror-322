import logging
import os
import sys
import shutil
import coloredlogs
import traceback

from PySide6 import QtCore, QtWidgets, QtUiTools
from PySide6.QtGui import Qt

from famegui.mainwindow import MainWindow
from famegui.usersettings import UserSettings
from famegui.appworkingdir import AppWorkingDir
from famegui import __version__


def _tr(text):
    return QtCore.QCoreApplication.translate("app", text)


_APP_NAME = "FAME GUI"
_APP_VERSION = __version__


def _setup_logs():
    logging_format = "%(asctime)s %(levelname)s %(message)s"
    coloredlogs.install(level="INFO", fmt=logging_format)


def _init_working_dir_location() -> AppWorkingDir:
    logging.debug("initializing working dir")

    s = UserSettings()
    if s.working_dir is None:
        QtWidgets.QMessageBox.information(
            None,
            _tr(f"{_APP_NAME} working directory"),
            _tr(
                f"The {_APP_NAME} working directory is not defined for this user account.\n\n"
                "This directory will be used as the root location for all the files required or referenced by the application.\n\n"
                "Click OK to configure the path to the FAME working directory."
            ),
        )
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            _tr("Select {} working directory").format(_APP_NAME),
            "",
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        if len(dir_path) == 0:
            raise RuntimeError(
                "can't start the application without a valid working directory"
            )
        s.set_working_dir(dir_path)

    logging.info("working directory: {}".format(s.working_dir))
    return AppWorkingDir(s.working_dir)


def _init_schemas_dir(work_dir: AppWorkingDir):
    logging.debug("initializing schemas dir")

    schemas_dir = work_dir.schemas_dir
    if os.path.isdir(work_dir.schemas_dir):
        if len(work_dir.list_existing_schema_files()) > 0:
            return
    else:
        logging.info("creating directory {}".format(schemas_dir))
        os.mkdir(schemas_dir)

    # copy the default schema
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_schema_path = os.path.join(script_dir, "data", "schema-example.yaml")
    logging.info(
        "copying default schema file '{}' to {}".format(
            default_schema_path, schemas_dir
        )
    )
    try:
        shutil.copy(default_schema_path, schemas_dir)
    except Exception as e:
        raise RuntimeError(
            "failed to copy default schema file to {}".format(schemas_dir)
        ) from e


def _init_scenarios_dir(work_dir: AppWorkingDir):
    logging.debug("initializing scenarios dir")

    scenarios_dir = work_dir.scenarios_dir
    if not os.path.isdir(scenarios_dir):
        logging.info("creating directory {}".format(scenarios_dir))
        os.mkdir(scenarios_dir)


def _init_timeseries_dir(work_dir: AppWorkingDir):
    logging.debug("initializing timeseries dir")

    timeseries_dir = work_dir.timeseries_dir
    if not os.path.isdir(timeseries_dir):
        logging.info("creating directory {}".format(timeseries_dir))
        os.mkdir(timeseries_dir)


def _init_protobuf_dir(work_dir: AppWorkingDir):
    logging.debug("initializing protobuf dir")

    protobuf_dir = work_dir.protobuf_dir
    if not os.path.isdir(protobuf_dir):
        logging.info("creating directory {}".format(protobuf_dir))
        os.mkdir(protobuf_dir)


def _init_working_dir() -> AppWorkingDir:
    work_dir = _init_working_dir_location()
    _init_schemas_dir(work_dir)
    _init_scenarios_dir(work_dir)
    _init_timeseries_dir(work_dir)
    _init_protobuf_dir(work_dir)

    logging.debug("work dir location")
    logging.debug(work_dir.root_dir)

    return work_dir


_main_wnd = None


def _excepthook(exc_type, exc_value, exc_tb):
    """Sets up logging configuration, logging error to text file"""
    logging.basicConfig(
        filename="error_log.txt",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a",
    )

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_tb))

    if isinstance(exc_value, ValueError):
        logging.error("{}".format(exc_value))
    else:
        logging.error(
            "Exception: {}\n{}".format(exc_value, "".join(traceback.format_tb(exc_tb)))
        )

    msg = _tr("Error: {}.").format(exc_value)
    # remove the extra final dot from the message, if any (error from fameio...)
    if msg.endswith(".."):
        msg = msg[:-1]

    if exc_value.__cause__:
        msg += _tr("\n\nDetails: {}").format(exc_value.__cause__)
    QtWidgets.QMessageBox.critical(_main_wnd, _tr("Error"), msg)


def _is_debugger_attached() -> bool:
    """Return True if the debugger is currently attached"""
    gettrace = getattr(sys, "gettrace", lambda: None)
    return gettrace() is not None


def run():
    _setup_logs()

    if _is_debugger_attached():
        # do not handle unexpected exceptions but let them be caught by the debugger
        logging.info(
            "running inside a debugger: disabling the global exception handler"
        )
    else:
        sys.excepthook = _excepthook

    ui_file_loader = QtUiTools.QUiLoader()
    app = QtWidgets.QApplication([])

    app.setOrganizationDomain("dlr.de")
    app.setOrganizationName("DLR")
    app.setApplicationName(_APP_NAME)
    app.setApplicationVersion(_APP_VERSION)
    app.setApplicationDisplayName(
        "{} (version {})".format(app.applicationName(), app.applicationVersion())
    )
    app.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)

    work_dir = _init_working_dir()

    logging.debug("creating main window")
    _main_wnd = MainWindow(work_dir,ui_file_loader)
    _main_wnd.show()

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        logging.debug("processing command line argument '{}'".format(file_path))
        _main_wnd.load_scenario_file(file_path)

    logging.debug("running the application")
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
    logging.info("exiting the application")
