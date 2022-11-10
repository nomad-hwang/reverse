import subprocess


def cmd(cmd: list[str]) -> tuple[str, str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8"), err.decode("utf-8")
