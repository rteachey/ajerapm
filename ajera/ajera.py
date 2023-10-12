from contextlib import contextmanager
from .errors import AjeraError
from .model import (
    CreateSession,
    CreateSessionContent,
    EndSession,
    ListProjects,
    ListProjectsResponse,
    ListProjectsArgs,
    GetProjects,
    GetProjectsResponse,
    GetProjectsArgs,
)


class Ajera:
    """AJERA API interaction class"""

    _token = None

    @property
    def token(self):
        if self._token is not None:
            return self._token
        else:
            raise AjeraError("please create_session() first")

    @token.setter
    def token(self, t):
        if self._token is None:
            self._token = t
        else:
            raise AjeraError("please close_session() first")

    def start_session(self):
        """Ajera API 'CreateAPISession' function"""
        session: CreateSessionContent = CreateSession().post().content
        if self._token is None:
            self._token = session.session_token
        else:
            raise AjeraError("cannot start session; session already active")

    def close_session(self):
        EndSession(session_token=self._token).post()
        del self._token

    def list_projects(
        self,
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
        **kwargs
    ):
        """Ajera API 'ListProjects' function"""

        args = ListProjectsArgs(
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
        )
        lp_model = ListProjects(
            session_token=self._token, method_arguments=args, **kwargs
        )
        content: ListProjectsResponse = lp_model.post()

        return content

    def get_projects(self, requested: list[int] = None, **kwargs):  # example: [1, 2, 3]
        """Ajera API 'GetProjects' function"""

        args = GetProjectsArgs(requested_projects=requested)
        gp_model = GetProjects(
            session_token=self._token, method_arguments=args, **kwargs
        )
        content: GetProjectsResponse = gp_model.post()  # .content

        return content


@contextmanager
def ajera():
    ajera_inst = Ajera()
    ajera_inst.start_session()
    try:
        yield ajera_inst
    finally:
        # Code to release resource, e.g.:
        ajera_inst.close_session()
