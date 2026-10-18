"""Keep a diagnostic rerun from replacing the required checker result."""

import os
import sys


def main():
    checker = os.environ.get("CHECK_OUTCOME", "")
    diagnostic = os.environ.get("DIAGNOSE_OUTCOME", "")
    if checker == "success":
        return 0

    if diagnostic == "success":
        message = (
            "The required checker failed. The diagnostic rerun passed, "
            "but it does not replace the required check."
        )
    else:
        message = "The required checker failed; see the diagnostic step for details."
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
