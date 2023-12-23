Under data/, we keep separate directories for the raw/ data, intermediate processed/ data, and final cleaned/ data. (These names, by the way, are completely arbitrary, you can name them in some other way if you desire, as long as they convey the same ideas.)

You'll note that there is also a README.md associated with this directory. This is intentional: it should contain the following details:

    1) Where the data come from

    2) What scripts under the scripts/ directory transformed which files under raw/ into which files under processed/ and cleaned/

    3) Why each file under cleaned/ exists, with optional references to particular notebooks. (Optional, especially when things are still in flux.)

Here, I'm suggesting placing the data under the same project directory, but only under certain conditions. Firstly, only when you're the only person working on the project, and so there's only one authoritative source of data. Secondly, only when your data can fit on disk.

If you're working with other people, you will want to make sure that all of you agree on what the "authoritative" data source is. If it is a URL (e.g. to an s3 bucket, or to a database), then that URL should be stored and documented in the custom Python package, with a concise variable name attached to it. If it is a path on an HPC cluster and it fits on disk, there should be a script that downloads it so that you have a local version.