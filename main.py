from agents import CoordinatorAgent


def main() -> None:
    print("=" * 60)
    print("AGENTIC AI RESEARCH ASSISTANT")
    print("=" * 60)

    topic = input("Enter your research topic: ").strip()

    if not topic:
        print("Error: topic cannot be empty.")
        return

    coordinator = CoordinatorAgent()

    try:
        result = coordinator.run(topic)
        print("\n" + result)
    except Exception as error:
        print("\nSomething went wrong.")
        print(f"Error details: {error}")


if __name__ == "__main__":
    main()