# cli.py

import argparse
from yggdrasil.rag import ask_yggdrasil

def main():
    parser = argparse.ArgumentParser(description="🧠 Ask Yggdrasil — memory-guided AI")
    parser.add_argument("question", type=str, help="The question to ask Yggdrasil")

    args = parser.parse_args()
    response = ask_yggdrasil(args.question)

    print("\n📜 Yggdrasil says:\n")
    print(response)

if __name__ == "__main__":
    main()
