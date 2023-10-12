from .ajera import Ajera

AJERA = Ajera()
AJERA.start_session()


def project_data(
    *,
    by_status: list[str] = None,  # example: ["Preliminary", "Hold"],
    by_company: list[int] = None,  # example:[1],
    by_name_like: str = None,  # example: "Description",
    by_description_like: str = None,  # example: "Project Description",
    by_description_equals: str = None,  # example: "Project Description",
    by_id_like: str = None,  # example: "20772",
    by_project_type: list = None,  # example: [1, null],
    by_sync_to_crm: list[bool] = None,  # example: [true],
    by_earliest_modified_date: str = None,  # example: "2023-03-11",
    by_latest_modified_date: str = None,  # example: "2023-03-11",
):
    project_keys = list(
        p.key
        for p in AJERA.list_projects(
            by_status=by_status,
            by_company=by_company,
            by_name_like=by_name_like,
            by_description_like=by_description_like,
            by_description_equals=by_description_equals,
            by_id_like=by_id_like,
            by_project_type=by_project_type,
            by_sync_to_crm=by_sync_to_crm,
            by_earliest_modified_date=by_earliest_modified_date,
            by_latest_modified_date=by_latest_modified_date,
        ).content.projects
    )
    projects = AJERA.get_projects(requested=project_keys).content.projects

    return projects
