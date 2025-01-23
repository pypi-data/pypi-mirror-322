from contextvars import ContextVar
import logging
import os
from nemo_library.features.config import Config
from nemo_library.utils.migmanutils import (
    getNEMOStepsFrompAMigrationStatusFile,
    initializeFolderStructure,
    load_database,
)
from nemo_library.utils.utils import log_error
import pandas as pd


__all__ = ["MigManCreateProjectTemplates"]

config_var = ContextVar("config")
local_project_directory_var = ContextVar("local_project_path")
projects_var = ContextVar("projects")
multi_projects_var = ContextVar("multi_projects")
database_var = ContextVar("database")


def MigManCreateProjectTemplates(
    config: Config,
    local_project_directory: str,
    projects: list[str] = None,
    proALPHA_project_status_file: str = None,
    multi_projects: dict[str, str] = None,
) -> None:

    # if there is a status file given, we ignore the given projects and get the project list from the status file
    if proALPHA_project_status_file:
        projects = getNEMOStepsFrompAMigrationStatusFile(proALPHA_project_status_file)

    # store parameters als global objects to avoid passing them to each and every funtion
    config_var.set(config)
    local_project_directory_var.set(local_project_directory)
    projects_var.set(projects)
    multi_projects_var.set(multi_projects)

    # initialize project folder structure
    initializeFolderStructure(local_project_directory)

    dbdf = load_database()
    database_var.set(dbdf)
    for project in projects:

        # check for project in database
        filtereddbdf = dbdf[dbdf["project_name"] == project]
        if filtereddbdf.empty:
            log_error(f"project '{project}' not found in database")

        # get list of postfixes
        postfixes = filtereddbdf["postfix"].unique().tolist()

        # init project
        multi_projects_list = (
            multi_projects[project] if project in multi_projects else None
        ) if multi_projects else None
        if multi_projects_list:
            for addon in multi_projects_list:
                for postfix in postfixes:
                    _create_project_template_file(project, addon, postfix)
        else:
            for postfix in postfixes:
                _create_project_template_file(project, None, postfix)


def _create_project_template_file(
    project: str,
    addon: str,
    postfix: str,
) -> None:

    logging.info(
        f"Create project template file for '{project}', addon '{addon}', postfix '{postfix}'"
    )

    dbdf = database_var.get()
    dbdf = dbdf[(dbdf["project_name"] == project) & (dbdf["postfix"] == postfix)]
    columns = dbdf["import_name"].to_list()
    data = {col: [""] for col in columns}
    templatedf = pd.DataFrame(data=data, columns=columns)
    templatedf.to_csv(
        os.path.join(
            local_project_directory_var.get(),
            "templates",
            f"{project}{" " + addon if addon else ""}{(" (" + postfix + ")") if postfix else ""}.csv",
        ),
        index=False,
        sep=";",
        encoding="UTF-8",
    )
