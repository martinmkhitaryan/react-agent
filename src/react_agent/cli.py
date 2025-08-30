import argparse
import os
import sys

from .agent import ReactAgent

parser = argparse.ArgumentParser(
    description="ReactAgent - A ReAct-based AI agent for question answering",
)
# NOTE: Add args later. For example model name.


def main():
    args = parser.parse_args()

    try:
        agent = ReactAgent()
        while True:
            query = input("Question: ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print("Bye")
                break

            if query.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                continue

            agent.react(query)
            print()
    except KeyboardInterrupt:
        print('Bye')
        sys.exit(1)
    # NOTE: better exception handling


if __name__ == "__main__":
    main()
