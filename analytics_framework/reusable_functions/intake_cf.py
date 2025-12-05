import intake
from analytics_framework import INTAKE_LOC
from pathlib import Path

CATALOG_LOC = Path.joinpath(INTAKE_LOC, "catalog_entry.yml")


def initiate_catalog():
    """
    Load the Intake catalog from the catalog_entry.yml file.

    Returns:
        intake.catalog.Catalog: The loaded catalog object.
    """
    catalog = intake.open_catalog(CATALOG_LOC)
    return catalog


def list_catalog_entry():
    """
    Return a list of all entries inside the catalog.

    Returns:
        list: A list of catalog entry names.
    """
    return list(catalog)


def view_catalog(catalog):
    """
    Display the catalog in the Intake GUI.
    
    Args:
        catalog (intake.catalog.Catalog): The catalog to display.

    Returns:
        intake.gui: The Intake GUI application with the catalog added.
    """
    intake_app = intake.gui
    intake_app.add(catalog)
    return intake_app
