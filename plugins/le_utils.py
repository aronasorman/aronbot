from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import tempfile
import sh
import os
import io

PYPI_USERNAME = os.environ["PYPI_USERNAME"]
PYPI_PASSWORD = os.environ["PYPI_PASSWORD"]


class Le_utils(BotPlugin):
    """
    Commands for automating LE utils operations
    """

    @botcmd
    def leutils_push(self, message, args):
        """
        A command to push the latest LE utils master to PyPI.
        """
        yield "Gotcha! Cloning the latest LE utils repo..."
        
        repo = "https://github.com/learningequality/le-utils.git"
        
        with tempfile.TemporaryDirectory(prefix="le-utils-") as d:
            yield "Cloning to {}".format(d)
            
            # git clone command to temp dir
            sh.git.clone("--depth", "1", repo, d)
            
            # build the sdist first
            yield "Building the sdist!"
            sh.python("setup.py", "sdist", _cwd=d)
            # get the sdist we just created
            out = io.StringIO()
            sh.ls("dist/", _cwd=d, _out=out)
            dist = os.path.join("dist", out.getvalue().strip())

            
            # command: python setup.py sdist upload -r pypi
            out = io.StringIO()
            env = {
                "TWINE_USERNAME": PYPI_USERNAME,
                "TWINE_PASSWORD": PYPI_PASSWORD,
            }
            yield "Uploading to PyPI!"
            sh.twine(
                "upload", dist, 
                _cwd=d,
                _err_to_out=True,
                # _out=out,
                _env=env
            )

            
            yield out.getvalue()
            yield "success!"
