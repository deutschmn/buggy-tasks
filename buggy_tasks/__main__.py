import sys

from streamlit.web import cli as stcli

if __name__ == "__main__":
    from buggy_tasks import app

    sys.argv = ["streamlit", "run", app.__file__]
    sys.exit(stcli.main())
