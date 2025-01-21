from contextvars import ContextVar
from datetime import datetime
import json
import logging
import os
import re
import pandas as pd

from nemo_library.features.config import Config
from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.projects import (
    LoadReport,
    createImportedColumns,
    createOrUpdateReport,
    createOrUpdateRule,
    createProject,
    getImportedColumns,
    getProjectList,
)
from nemo_library.utils.migmanutils import (
    getNEMOStepsFrompAMigrationStatusFile,
    getProjectName,
    load_database,
    upload_dataframe,
)
from nemo_library.utils.utils import (
    get_display_name,
    get_internal_name,
    log_error,
)

config_var = ContextVar("config")
local_project_directory_var = ContextVar("local_project_path")
projects_var = ContextVar("projects")
multi_projects_var = ContextVar("multi_projects")
database_var = ContextVar("database")

__all__ = ["MigManLoadData"]


def MigManLoadData(
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
            (multi_projects[project] if project in multi_projects else None)
            if multi_projects
            else None
        )
        if multi_projects_list:
            for addon in multi_projects_list:
                for postfix in postfixes:
                    _load_data(project, addon, postfix)
        else:
            for postfix in postfixes:
                _load_data(project, None, postfix)


def _load_data(
    project: str,
    addon: str,
    postfix: str,
) -> None:

    # check for file first
    project_name = getProjectName(project, addon, postfix)
    file_name = os.path.join(
        local_project_directory_var.get(),
        "srcdata",
        f"{project_name}.csv",
    )

    if os.path.exists(file_name):
        logging.info(
            f"File '{file_name}' for '{project}', addon '{addon}', postfix '{postfix}' found"
        )

        # does project exist? if not, create it
        new_project = False
        if (
            not project_name
            in getProjectList(config_var.get())["displayName"].to_list()
        ):
            new_project = True
            logging.info(f"Project not found in NEMO. Create it...")
            createProject(
                config=config_var.get(),
                projectname=project_name,
                description=f"Data Model for Mig Man table '{project}'",
            )

        # check whether file is newer than uploaded data
        time_stamp_file = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        if not new_project:
            df = LoadReport(
                config=config_var.get(),
                projectname=project_name,
                report_name="static information",
            )
            if df["TIMESTAMP_FILE"].iloc[0] == time_stamp_file:
                logging.info(
                    f"file and data in NEMO has the same time stamp ('{time_stamp_file}'). Ignore this file"
                )
                return

        # read the file now and check the fields that are filled in that file
        datadf = pd.read_csv(
            file_name,
            sep=";",
            dtype=str,
        )

        # drop all columns that are totally empty
        columns_to_drop = datadf.columns[datadf.isna().all()]
        datadf_cleaned = datadf.drop(columns=columns_to_drop)
        if not columns_to_drop.empty:
            logging.info(
                f"totally empty columns removed. Here is the list {json.dumps(columns_to_drop.to_list(),indent=2)}"
            )

        dbdf = database_var.get()
        dbdf = dbdf[(dbdf["project_name"] == project) & (dbdf["postfix"] == postfix)]
        columns_migman = dbdf["import_name"].to_list()
        columns_nemo = getImportedColumns(config_var.get(), project_name)
        columns_nemo_import_names = (
            [] if columns_nemo.empty else columns_nemo["importName"].to_list()
        )

        new_columns = []
        for col in datadf_cleaned.columns:
            if not col in columns_migman:
                log_error(
                    f"file {file_name} contains column '{col}' that is not defined in MigMan Template"
                )

            # column already defined in nemo? if not, create it
            if not col in columns_nemo_import_names:
                logging.info(
                    f"column '{col}' not found in project {project_name}. Create it."
                )

                coldb = dbdf.iloc[columns_migman.index(col)]
                description = "\n".join(
                    [f"{key}: {value}" for key, value in coldb.items()]
                )
                new_columns.append(
                    {
                        "displayName": coldb["display_name"],
                        "importName": coldb["import_name"],
                        "internalName": coldb["internal_name"],
                        "description": description,
                        "dataType": "string",
                        "focusOrder": f"{columns_migman.index(col):03}",
                    }
                )
        if new_columns:
            createImportedColumns(
                config=config_var.get(),
                projectname=project_name,
                columns=new_columns,
            )

        # now we have created all columns in NEMO. Upload data
        datadf_cleaned["timestamp_file"] = time_stamp_file
        upload_dataframe(
            config=config_var.get(), project_name=project_name, df=datadf_cleaned
        )
        _update_static_report(project_name=project_name)

        # if there are new columns, update all reports
        if new_columns:
            _update_deficiency_mining(
                project_name=project_name,
                columns_in_file=datadf_cleaned.columns,
                dbdf=dbdf,
            )


def _update_static_report(
    project_name: str,
) -> None:

    sql_query = """
SELECT  
    MAX(timestamp_file) AS timestamp_file
FROM 
    $schema.$table
WHERE
    not timestamp_file = 'timestamp_file'
"""
    createOrUpdateReport(
        config=config_var.get(),
        projectname=project_name,
        displayName="static information",
        querySyntax=sql_query,
        internalName="static_information",
        description="return static information",
    )


def _update_deficiency_mining(
    project_name: str,
    columns_in_file: list[str],
    dbdf: pd.DataFrame,
) -> None:

    logging.info(
        f"Update deficiency mining reports and rules for project {project_name}"
    )

    # create column specific fragments
    frags_checked = []
    frags_msg = []
    for idx, (display_name, internal_name, data_type, format) in enumerate(
        zip(
            dbdf["display_name"],
            dbdf["internal_name"],
            dbdf["Data Type"],
            dbdf["Format"],
        )
    ):

        if display_name in columns_in_file:
            frag_check = []
            frag_msg = []

            # data type specific checks
            match data_type.lower():
                case "character":
                    # Parse format to get maximum length
                    match = re.search(r"x\((\d+)\)", format)
                    field_length = int(match.group(1)) if match else len(format)
                    frag_check.append(f"LENGTH({internal_name}) > {field_length}")
                    frag_msg.append(
                        f"{display_name} exceeds field length (max {field_length} digits)"
                    )

                case "integer" | "decimal":
                    # Parse format
                    negative_numbers = "-" in format
                    if negative_numbers:
                        format = format.replace("-", "")

                    if not negative_numbers:
                        frag_check.append(
                            f"LEFT(TRIM({internal_name}), 1) = '-' OR RIGHT(TRIM({internal_name}), 1) = '-'"
                        )
                        frag_msg.append(f"{display_name} must not be negative")

                    # decimals?
                    decimals = len(format.split(".")[1]) if "." in format else 0
                    if decimals > 0:
                        format = format[: len(format) - decimals - 1]
                        frag_check.append(
                            f"""LOCATE(TO_VARCHAR(TRIM({internal_name})), '.') > 0 AND 
                LENGTH(RIGHT(TO_VARCHAR(TRIM({internal_name})), 
                            LENGTH(TO_VARCHAR(TRIM({internal_name}))) - 
                            LOCATE(TO_VARCHAR(TRIM({internal_name})), '.'))) > {decimals}"""
                        )
                        frag_msg.append(
                            f"{display_name} has too many decimals ({decimals} allowed)"
                        )

                    match = re.search(r"z\((\d+)\)", format)
                    field_length = int(match.group(1)) if match else len(format)

                    frag_check.append(
                        f"""LENGTH(
                        LEFT(
                            REPLACE(TO_VARCHAR(TRIM({internal_name})), '-', ''), 
                            LOCATE('.', REPLACE(TO_VARCHAR(TRIM({internal_name})), '-', '')) - 1
                        )
                    ) > {field_length}"""
                    )
                    frag_msg.append(
                        f"{display_name} has too many digits before the decimal point ({field_length} allowed)"
                    )

                    frag_check.append(
                        f"NOT {internal_name} LIKE_REGEXPR('^[-]?[0-9]+(\\.[0-9]+)?[-]?$')"
                    )
                    frag_msg.append(f"{display_name} is not a valid number")

                case "date":
                    frag_check.append(
                        f"NOT {internal_name} LIKE_REGEXPR('^(\\d{{4}})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')"
                    )
                    frag_msg.append(f"{display_name} is not a valid date")

                case "logical":
                    format_for_regex = format.replace("/", "|")
                    frag_check.append(
                        f"NOT {internal_name} LIKE_REGEXPR('^({format_for_regex})$')"
                    )
                    frag_msg.append(
                        f'{display_name}: logical value does not match format "{format}"'
                    )

            # special fields

            if "mail" in internal_name:
                frag_check.append(
                    f"NOT {internal_name} LIKE_REGEXPR('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$')"
                )
                frag_msg.append(f"{display_name} is not a valid email")

            if (
                ("phone" in internal_name)
                or ("telefon" in internal_name)
                or ("fax" in internal_name)
            ):
                frag_check.append(
                    f"NOT {internal_name} LIKE_REGEXPR('^\\+?[0-9\\s\\-()]{5,15}$')"
                )
                frag_msg.append(f"{display_name} is not a valid phone number")

            # now build deficiency mining report for this column (if there are checks)
            if frag_check:

                # save checks and messages for total report
                frags_checked.extend(frag_check)
                frags_msg.extend(frag_msg)
                sorted_columns = [f'{internal_name} AS "{display_name}"'] + [
                    f'{intname} AS "{dispname}"'
                    for dispname, intname in zip(
                        dbdf["display_name"], dbdf["internal_name"]
                    )
                    if intname != internal_name and dispname in columns_in_file
                ]

                # case statements for messages and dm report
                case_statement_specific = " ||\n\t".join(
                    [
                        f"CASE\n\t\tWHEN {check}\n\t\tTHEN CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
                        for check, msg in zip(frag_check, frag_msg)
                    ]
                )

                status_conditions = " OR ".join(frag_check)

                sql_statement = f"""SELECT
    \tCASE 
    \t\tWHEN {status_conditions} THEN 'check'
        ELSE 'ok'
    END AS STATUS
    \t,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
    \t,{',\n\t'.join(sorted_columns)}
    FROM
    $schema.$table"""

                # create the report
                report_display_name = f"(DEFICIENCIES) {idx + 1:03} {display_name}"
                report_internal_name = get_internal_name(report_display_name)

                createOrUpdateReport(
                    config=config_var.get(),
                    projectname=project_name,
                    displayName=report_display_name,
                    internalName=report_internal_name,
                    querySyntax=sql_statement,
                    description=f"Deficiency Mining Report for column '{display_name}' in project '{project_name}'",
                )

                createOrUpdateRule(
                    config=config_var.get(),
                    projectname=project_name,
                    displayName=f"DM_{idx:03}: {display_name}",
                    ruleSourceInternalName=report_internal_name,
                    ruleGroup="02 Columns",
                    description=f"Deficiency Mining Rule for column '{display_name}' in project '{project_name}'",
                )

            logging.info(
                f"project: {project_name}, column: {display_name}: {len(frag_check)} frags added"
            )

    # now setup global dm report and rule

    # case statements for messages and dm report
    case_statement_specific = " ||\n\t".join(
        [
            f"CASE\n\t\tWHEN {check}\n\t\tTHEN  CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
            for check, msg in zip(frags_checked, frags_msg)
        ]
    )

    status_conditions = " OR ".join(frags_checked)

    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([intname for intname, dispname in zip(dbdf["internal_name"],dbdf["display_name"]) if dispname in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table
)
SELECT
      Status
    , DEFICIENCY_MININNG_MESSAGE
    , {',\n\t'.join(sorted_columns)}
FROM 
    CTEDefMining
"""

    # create the report
    report_display_name = f"(DEFICIENCIES) GLOBAL"
    report_internal_name = get_internal_name(report_display_name)

    createOrUpdateReport(
        config=config_var.get(),
        projectname=project_name,
        displayName=report_display_name,
        internalName=report_internal_name,
        querySyntax=sql_statement,
        description=f"Deficiency Mining Report for  project '{project_name}'",
    )

    createOrUpdateRule(
        config=config_var.get(),
        projectname=project_name,
        displayName="Global",
        ruleSourceInternalName=report_internal_name,
        ruleGroup="01 Global",
        description=f"Deficiency Mining Rule for project '{project_name}'",
    )
    
    # create report for mig man

    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([intname for intname, dispname in zip(dbdf["internal_name"],dbdf["display_name"]) if dispname in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table
)
SELECT
    {',\n\t'.join(sorted_columns)}
FROM 
    CTEDefMining
WHERE
    STATUS = 'ok'
"""

    # create the report
    report_display_name = f"(MigMan) All records with no message"
    report_internal_name = get_internal_name(report_display_name)

    createOrUpdateReport(
        config=config_var.get(),
        projectname=project_name,
        displayName=report_display_name,
        internalName=report_internal_name,
        querySyntax=sql_statement,
        description=f"MigMan export with valid data for  project '{project_name}'",
    )
    logging.info(f"Project {project_name}: {len(frags_checked)} checks implemented...")
    return len(frags_checked)
