import os
import tempfile
import tarfile

from ansible_creator.config import Config
from ansible_creator.output import Output
from ansible_creator.utils import TermFeatures
from ansible_creator.subcommands.init import Init


from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse


try:
    from ._version import version as __version__
except ImportError:
    __version__ = "source"

app = Flask(__name__)
api = Api(app)

term_features = TermFeatures(
    color=False,
    links=False,
)

output = Output(
    log_append=True,
    log_file=tempfile.mkdtemp() + "/ansible-creator.log",
    log_level="debug",
    term_features=term_features,
    verbosity=3,
    display="json",
)

creator_init_args = reqparse.RequestParser()
creator_init_args.add_argument(
    "collection",
    type=str,
    required=True,
    help="The collection parameter is required when using ansible-creator init!",
)


def _create_collection_tar(tar_path, collection_dir):
    print(tar_path)
    with tarfile.open(tar_path, "w") as tarhandler:
        # list the root of the source dir and add each entry to tar
        # this is recursive by nature
        # we just need to remove the parents from the name
        for content in os.listdir(collection_dir):
            full_path = os.path.join(collection_dir, content)
            tarhandler.add(full_path, arcname=content)


class CreatorInit(Resource):
    """Resource for ansible-creator init."""

    def get(self):
        """Handle GET requests for /init endpoint."""
        req_args = creator_init_args.parse_args()
        req_collection = req_args["collection"]
        req_tmp_dir = tempfile.mkdtemp()

        collection_init_path = req_tmp_dir + "/" + req_collection
        req_tar_path = f"{req_collection.replace('.', '_')}.tar"

        req_args.update(
            {
                "subcommand": "init",
                "init_path": collection_init_path,
                "creator_version": __version__,
                "output": output,
                "project": "collection",
            }
        )
        # scaffold collection
        Init(config=Config(**req_args)).run()

        _create_collection_tar(
            tar_path=req_tmp_dir + "/" + req_tar_path,
            collection_dir=collection_init_path,
        )

        return send_from_directory(
            directory=req_tmp_dir,
            path=req_tar_path,
            as_attachment=True,
        )


api.add_resource(CreatorInit, "/init")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
