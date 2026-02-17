# ui/cli.py

from core.tutor import Tutor


def start_cli():
    print("=" * 50)
    print("📘 Welcome to OffTute (Offline AI Tutor)")
    print("Type 'exit' to quit.")
    print("=" * 50)

    # Initialize tutor
    tutor = Tutor(language="English", level="beginner")

    while True:
        try:
            user_input = input("\n🧑 You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("\n👋 Goodbye! Happy learning.")
                break

            if not user_input:
                print("⚠️ Please ask a question.")
                continue

            print("\n🤖 OffTute is thinking...\n")
            response = tutor.explain(user_input)
            print(f"📖 OffTute: {response}")

        except KeyboardInterrupt:
            print("\n\n👋 Session ended.")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")
