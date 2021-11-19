import subprocess as sp


def cmd(c):
    output, err = sp.Popen(
        c,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    ).communicate()

    output = output.decode("utf-8").strip()
    err = err.decode("utf-8").strip()

    return output, err
