import pytest
from ajera.public import project_data


@pytest.fixture()
def project_id_like():
    return "28222"


@pytest.fixture()
def ajera_context():
    from ajera.public import AJERA

    yield None
    AJERA.close_session()


def test_project_data(ajera_context, project_id_like):
    project_data_list = project_data(by_id_like=project_id_like)
    assert project_data_list
