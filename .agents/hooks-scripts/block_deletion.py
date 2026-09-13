#!/usr/bin/env python3
import sys
import json
import re

def main():
    try:
        data = json.load(sys.stdin)
        tool_call = data.get("toolCall", {})
        args = tool_call.get("args", {})
        command = str(args.get("CommandLine", "")).lower()

        # Padrões de comandos de deleção/remoção (PowerShell, CMD, Bash, Git)
        deletion_patterns = [
            r"\brm\b",
            r"\brmdir\b",
            r"\bdel\b",
            r"\berase\b",
            r"\bunlink\b",
            r"\bremove-item\b",
            r"\bri\b",
            r"\bgit\s+rm\b",
            r"\bremove\b",
        ]

        for pattern in deletion_patterns:
            if re.search(pattern, command):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"BLOQUEADO PELO HOOK: Operação de deleção de arquivo/diretório proibida ('{command}')."
                }))
                sys.exit(0)

    except Exception:
        pass

    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()