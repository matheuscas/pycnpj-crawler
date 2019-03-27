import os
from requests_html import HTMLSession
from requests_file import FileAdapter

session = HTMLSession()
session.mount('file://', FileAdapter())


def _get(mock_file_name):
    path = os.path.sep.join(
        (
            os.path.dirname(os.path.abspath(__file__)),
            f"mocks/{mock_file_name}"
        )
    )
    url = 'file://{}'.format(path)
    return session.get(url)


def get_response(state):
    return _get(f"{state}_mock.html")
