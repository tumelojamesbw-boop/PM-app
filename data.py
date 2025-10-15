import pandas as pd

import pandas as pd

def load_and_merge_data():
    # Load datasets safely
    projects_df = pd.read_csv("projects.csv")

    # Parse project date columns safely
    for col in ["Start_Date", "End_Date"]:
        if col in projects_df.columns:
            projects_df[col] = pd.to_datetime(
                projects_df[col],
                errors='coerce',
                dayfirst=True
            )

    # Load tasks
    tasks_df = pd.read_csv("tasks.csv")

    # Clean and parse task date columns
    for col in ["Est_Start", "Est_End", "Act_Start", "Act_End"]:
        if col in tasks_df.columns:
            # Replace common separators and handle text values
            tasks_df[col] = (
                tasks_df[col]
                .astype(str)
                .str.replace(r'[./]', '-', regex=True)  # handles both / and .
                .str.strip()
            )
            tasks_df[col] = pd.to_datetime(
                tasks_df[col],
                errors='coerce',
                dayfirst=True
            )

    # Load other datasets
    costs_df = pd.read_csv("costs.csv")
    departments_df = pd.read_csv("Departments.csv")

    # Merge tasks with projects
    merged = tasks_df.merge(
        projects_df,
        on="Project_ID",
        how="left",
        suffixes=('', '_Project')
    )

    # Merge with departments
    if "Department_ID" in merged.columns and "Department_ID" in departments_df.columns:
        merged = merged.merge(
            departments_df,
            on="Department_ID",
            how="left"
        )

    # Merge with costs
    if "Task_ID" in merged.columns and "Task_ID" in costs_df.columns:
        merged = merged.merge(
            costs_df,
            on="Task_ID",
            how="left",
            suffixes=('', '_Cost')
        )

    return merged
