from app import app
from dotenv import load_dotenv

load_dotenv()

# Configuration with a unique thread ID
config = {
    "configurable": {
        "thread_id": "walmart_onboarding_001"
    }
}


def run_workflow():

    # Phase 1: Initial submission
    print("\n--- Seller Submitting Data ---")

    initial_input = {
        "raw_data": "",
        "image_path": "MACES/test_image2.jpeg"
    }

    for event in app.stream(initial_input, config, stream_mode="values"):
        print(f"Current State: {event.get('listing', 'Processing...')}")

    # Check for pause
    state = app.get_state(config)

    if state.next:
        print(f"\n[PAUSED] Next node: {state.next}")
        print("Reason: Validation or compliance failed.")

        # Phase 2: Human review
        print("\n--- Human Review ---")
        user_choice = input("Approve this listing? (yes/no): ")

        if user_choice.lower() == "yes":

            for event in app.stream(None, config, stream_mode="values"):
                print(f"Final Output: {event.get('listing')}")

        else:
            print("Listing rejected.")


if __name__ == "__main__":
    run_workflow()
