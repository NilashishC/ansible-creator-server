import os
import tarfile
import tempfile

from ansible_creator.config import Config
from ansible_creator.output import Output
from ansible_creator.subcommands.init import Init
from ansible_creator.utils import TermFeatures
from flask import send_from_directory
from flask_restful import Resource, reqparse

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "source"

term_features = TermFeatures(
    color=False,
    links=False,
)

output = Output(
    log_append=True,
    log_file="ansible-creator.log",
    log_level="debug",
    term_features=term_features,
    verbosity=3,
    display="json",
)

creator_init_args = reqparse.RequestParser()

creator_init_args.add_argument("collection", type=str, location="args")
creator_init_args.add_argument("scm_org", type=str, location="args")
creator_init_args.add_argument("scm_project", type=str, location="args")
creator_init_args.add_argument(
    "project", default="collection", type=str, location="args"
)


def _create_content_tar(tar_path, req_init_path):
    with tarfile.open(tar_path, "w") as tarhandler:
        # list the root of the source dir and add each entry to tar
        # this is recursive by nature
        # we just need to remove the parents from the name
        for content in os.listdir(req_init_path):
            full_path = os.path.join(req_init_path, content)
            tarhandler.add(full_path, arcname=content)


class CreatorInit(Resource):
    """Resource for ansible-creator init."""

    def get(self):
        """Handle GET requests for /init endpoint."""
        req_args = creator_init_args.parse_args()

        # create a temp dir for every request
        # shared by scaffolded content and final tar
        with tempfile.TemporaryDirectory() as req_tmp_dir:
            # generate a workdir name
            req_project = req_args["project"]
            if req_project == "collection":
                req_workdir = req_args["collection"]
            else:
                req_workdir = f"{req_args['scm_org']}-{req_args['scm_project']}"

            # build init path where the requested content would be scaffolded
            init_path = req_tmp_dir + "/" + req_workdir

            req_args.update(
                {
                    "subcommand": "init",
                    "init_path": init_path,
                    "creator_version": __version__,
                    "output": output,
                    "project": req_project,
                }
            )

            # scaffold content
            Init(config=Config(**req_args)).run()

            _create_content_tar(
                tar_path=f"{req_tmp_dir}/{req_workdir}.tar",
                req_init_path=init_path,
            )

            return send_from_directory(
                directory=req_tmp_dir,
                path=f"{req_workdir}.tar",
                as_attachment=True,
            )
