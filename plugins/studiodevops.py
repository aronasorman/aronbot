from errbot import BotPlugin, botcmd, arg_botcmd, webhook

import subprocess


class Studiodevops(BotPlugin):
    """
    Deploy and manage Kolibri Studio
    """

    @arg_botcmd("name", type=str)
    @arg_botcmd("--favorite-number", type=int, unpack_args=False)
    def hello(self, message, args):
        """
        A command which says hello to someone.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            return "Hello {name}".format(name=args.name)
        else:
            return "Hello {name}, I hear your favorite number is {number}".format(
                name=args.name, number=args.favorite_number
            )

    @arg_botcmd("--num-threads", type=int, unpack_args=False)
    def studio_benchmark(self, message, args):
        """
        Do a quick benchmark of the main Studio app using wrk,
        and return the results.
        """
        yield "Running benchmarks on studio.learningequality.org"
        num_threads = str(args.num_threads or 10)
        cmd = [
            "wrk",
            "-t",
            num_threads,
            "-c",
            "400",
            "--latency",
            "https://studio.learningequality.org",
        ]
        out = subprocess.check_output(
            cmd, universal_newlines=True  # make the output prettier by adding this
        )

        yield str(out)

    @arg_botcmd("name", type=str)
    @arg_botcmd("branch", type=str)
    @arg_botcmd(
        "--fork",
        type=str,
        unpack_args=False,
        help="Choose which fork of learningequality/studio to use, e.g. aronasorman/content-curation",
    )
    def studio_makeinstance(self, message, args):
        # requirements: helm, gcloud, authenticated gcloud
        pass
