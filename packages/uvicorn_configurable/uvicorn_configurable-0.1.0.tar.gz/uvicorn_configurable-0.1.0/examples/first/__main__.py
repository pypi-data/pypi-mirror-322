"""Call the main function, which runs a configured uvicorn process.
To run this example: from the project root, call:
'poetry run python ./examples/first -c ./examples/first/config.toml'
"""

import config  # pylint: disable=unused-import  # isort: skip

import sys

from main import main

sys.exit(main())
