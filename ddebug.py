#!/usr/bin/env python3
"""
ddebug - debug container

Usage:
    ddebug.py debug <container_name_or_id> [--shell SHELL]

Examples:
    ./ddebug.py debug mybackend
"""

import argparse
import os
import shutil
import subprocess
import sys

DOCKER_IMAGE = "nicolaka/netshoot:latest"


def run(cmd, capture=False, check=True):
    if isinstance(cmd, str):
        cmd = cmd.split()
    if capture:
        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check
        )
    return subprocess.run(cmd, check=check)


def docker_exists():
    return shutil.which("docker") is not None


def check_target_exists(name):
    p = run(["docker", "inspect", name], capture=True, check=False)
    return p.returncode == 0


def check_target_running(name):
    p = run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            name
        ],
        capture=True,
        check=False
    )
    if p.returncode != 0:
        return False
    return p.stdout.decode().strip().lower() == "true"


def run_debug_container(target):
    dbg_name = f"ddebug_{target}"

    # Remove old debug container if exists
    existing = subprocess.run(
        [
            "docker",
            "ps",
            "-aq",
            "-f",
            f"name=^{dbg_name}$"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    if existing.stdout.strip():
        run(["docker", "rm", "-f", dbg_name], check=False)

    print(f"[+] Launching debug container attached to '{target}' ...")
    cmd = [
        "docker", "run", "--rm", "-it",
        "--privileged",
        f"--name={dbg_name}",
        f"--pid=container:{target}",
        f"--net=container:{target}",
        "--volumes-from", target,
        DOCKER_IMAGE,
        "sh",
        "-c",
        "apk update > /dev/null && apk add fish > /dev/null && fish"]
    os.execvp("docker", cmd)


def main():
    parser = argparse.ArgumentParser(
        prog="ddebug",
        description="ddebug - debug helper"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    dbg = sub.add_parser("debug", help="open shell attached to a container")
    dbg.add_argument("target", help="target container name or id")
    args = parser.parse_args()

    if not docker_exists():
        print("[!] docker not found in PATH")
        sys.exit(1)
    if args.cmd == "debug":
        if not check_target_exists(args.target):
            print(f"[!] Container '{args.target}' does not exist.")
            sys.exit(1)
        if not check_target_running(args.target):
            print(f"[!] Container '{args.target}' is not running.")
            sys.exit(1)
        run_debug_container(args.target)


if __name__ == "__main__":
    main()
