#!/usr/bin/env python3
import sys
import json

def main():
    try:
        # Lê o payload exato que o Antigravity envia (conforme a doc: toolCall -> args -> CommandLine)
        data = json.load(sys.stdin)
        tool_call = data.get("toolCall", {})
        args = tool_call.get("args", {})
        command = str(args.get("CommandLine", "")).lower()

        # Palavras-chave de remoção (pega rm, git rm, rmdir, del, etc.)
        if "rm" in command or "rmdir" in command or "del" in command:
            # Retorna o JSON de negação exigido pelo Antigravity
            print(json.dumps({
                "decision": "deny",
                "reason": f"BLOQUEADO PELO HOOK: Proibido deletar arquivos ou usar comandos de remoção ('{command}')."
            }))
            sys.exit(0)

    except Exception:
        pass

    # Se não for remoção, permite a execução normalmente
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()