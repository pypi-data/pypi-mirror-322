from contextvars import ContextVar
import json
import logging
import os
import re
import tempfile
from nemo_library.features.config import Config
from nemo_library.features.fileingestion import ReUploadFile
from nemo_library.features.focus import focusCoupleAttributes
from nemo_library.features.projects import (
    LoadReport,
    createImportedColumns,
    createOrUpdateReport,
    getImportedColumns,
    getProjectList,
)
from nemo_library.utils.utils import (
    get_display_name,
    get_import_name,
    get_internal_name,
)

__all__ = ["MigManApplyMapping"]

config_var = ContextVar("config")


def MigManApplyMapping(
    config: Config,
) -> None:

    # store parameters als global objects to avoid passing them to each and every funtion
    config_var.set(config)

    # get all projects
    projectList = getProjectList(config=config)["displayName"].to_list()

    # It might happen, that the user does not run our library will all mapping fields given that exists.
    # In any case, we have to check for ALL mappings defined to create the right reports. So here we ignore
    # the mapping fields that have been given - we collect all the mappings by ourselves
    mappingprojects = [
        x[len("Mapping ") :] for x in projectList if x.startswith("Mapping ")
    ]
    mappingfieldsall = {}
    for project in mappingprojects:
        importedcolumns = getImportedColumns(
            config=config, projectname=f"Mapping {project}"
        )["displayName"].to_list()
        mappingfieldsprj = [
            x[len("source ") :] for x in importedcolumns if x.startswith("source ")
        ]
        mappingfieldsall[project] = mappingfieldsprj

    if not mappingfieldsall:
        logging.info("no mapping fields found.")
        return

    logging.info(
        f"Mapping fields found. Here is the list: {json.dumps(mappingfieldsall,indent=2)}"
    )

    # scan all the other projects now whether they contain these fields or not
    dataprojects = [
        x
        for x in projectList
        if not x.startswith("Mapping")
        and not x in ["Business Processes", "Master Data"]
    ]

    for project in dataprojects:
        importedcolumns = getImportedColumns(config=config, projectname=project)[
            "displayName"
        ].to_list()

        columnstobemapped = {}
        # check for columns in this project that are mapped
        for key, values in mappingfieldsall.items():

            matched_originals = []

            # Flag to ensure ALL values in `values` must have a match
            all_match = True  # Start with the assumption that all values will match

            # Iterate over each value to check for matches in `importedcolumns`
            for val in values:
                match_found = False  # Track if the current value has a match

                for entry in importedcolumns:
                    # Check if the entry matches the pattern (value followed by a 3-digit number in parentheses)
                    if re.match(rf"^{re.escape(val)} \(\d{{3}}\)$", entry):
                        matched_originals.append(entry)  # Save the matching entry
                        match_found = True  # Mark that a match was found
                        break  # Exit the loop as we only need the first match for this value

                if not match_found:  # If no match was found for the current value
                    all_match = (
                        False  # Set the flag to False as not all values can match
                    )
                    break  # Exit the outer loop since we already know not all values match

            if all_match:  # Only proceed if ALL values in `values` matched
                columnstobemapped[key] = [
                    (src, tgt) for src, tgt in zip(values, matched_originals)
                ]

        # if there are mapped columns in this project, we are going to add mapped fields for that project now
        if columnstobemapped:

            logging.info(
                f"columns to be mapped found in project '{project}'. Here is the list: {json.dumps(columnstobemapped,indent=2)}"
            )

            # create columns for "original values" if they do not exist already
            new_columns = []
            for col in columnstobemapped:
                maplist = columnstobemapped[col]
                mapcol = f"Original_{maplist[0][1]}"
                if not mapcol in importedcolumns:
                    new_columns.append(
                        {
                            "displayName": get_display_name(mapcol),
                            "importName": get_import_name(mapcol),
                            "internalName": get_internal_name(mapcol),
                            "description": f"Original value of {maplist[0][1]}",
                            "dataType": "string",
                        }
                    )
            if new_columns:
                logging.info(f"Create Original-Columns...{json.dumps(new_columns)}")
                createImportedColumns(
                    config=config_var.get(),
                    projectname=project,
                    columns=new_columns,
                )

            sqlQuery = _SQL_Query_in_data_table(
                project=project,
                columnstobemapped=columnstobemapped,
            )

            createOrUpdateReport(
                config=config,
                projectname=project,
                displayName="(MAPPING) map data",
                querySyntax=sqlQuery,
                internalName="MAPPING_map_data",
                description="Map data",
            )
            df = LoadReport(
                config=config,
                projectname=project,
                report_name="(MAPPING) map data",
            )

            # Write to a temporary file and upload
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "tempfile.csv")

                df.to_csv(
                    temp_file_path,
                    index=False,
                    sep=";",
                    na_rep="",
                    encoding="UTF-8",
                )
                logging.info(
                    f"dummy file {temp_file_path} written for project '{project}'. Uploading data to NEMO now..."
                )

                ReUploadFile(
                    config=config,
                    projectname=project,
                    filename=temp_file_path,
                    update_project_settings=False,
                    version=3,
                    datasource_ids=[{"key": "datasource_id", "value": project}],
                )
                logging.info(f"upload to project {project} completed")

            # couple attributes
            importedcolumns = getImportedColumns(config=config, projectname=project)[
                "displayName"
            ].to_list()
            pairs = []
            for col in importedcolumns:
                original_col = f"Original_{col}"
                if original_col in importedcolumns:
                    pairs.append((col, original_col))

            for col, original_col in pairs:
                logging.info(f"Couple pairs: {col} & {original_col}")
                focusCoupleAttributes(
                    config=config,
                    projectname=project,
                    attributenames=[col, original_col],
                    previous_attribute=col
                )


def _SQL_Query_in_data_table(
    project: str,
    columnstobemapped: dict[str, list[str]],
) -> str:

    # we start with the easy one: select all columns that are defined
    importedcolumnsdf = getImportedColumns(config=config_var.get(), projectname=project)

    # filter original-values, they will be re-created again
    importedcolumnsdf = importedcolumnsdf[
        ~importedcolumnsdf["displayName"].str.startswith("Original_")
    ]

    # add new column with display names without numbers
    importedcolumnsdf["strippedDisplayName"] = importedcolumnsdf[
        "displayName"
    ].str.replace(r" \(\d{3}\)$", "", regex=True)
    datafrags = [
        f'data.{row["internalName"]} AS "{"Original_" if row["strippedDisplayName"] in columnstobemapped.keys() else""}{row["displayName"]}"'
        for idx, row in importedcolumnsdf.iterrows()
    ]

    # now add all mapped values
    datafrags.extend(
        f'COALESCE(Mapping_{get_internal_name(key)}.TARGET_{get_internal_name(key)},data.{get_internal_name(tgt)}) AS "{tgt}"'
        for key, value in columnstobemapped.items()
        for src, tgt in value
        if src == key
    )

    # and now, we join the mapping tables
    joins = []
    for key, value in columnstobemapped.items():
        selects = [
            f"MAPPING_{get_internal_name(key)}.SOURCE_{get_internal_name(src)} = data.{get_internal_name(tgt)}"
            for src, tgt in value
        ]
        joins.append(
            f"""LEFT JOIN
    $schema.PROJECT_MAPPING_{get_internal_name(key)} MAPPING_{get_internal_name(key)}
    ON {"\n\tAND ".join(selects)}"""
        )

    # and finally build the query
    query = f"""
SELECT
    {"\n\t,".join(datafrags)}
FROM
    $schema.$table data
{"\n".join(joins)}
"""
    return query
