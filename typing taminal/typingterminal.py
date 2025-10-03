import random
import time

WORD_LIST = ["apple","orange","banana","grape","lemon","keyboard","mouse","python","java","code","debug","fast","quick","speed","cloud","github","linux","mac","monitor","laptop"]
NUM_WORDS = 20
TEST_SECONDS = 30

def make_prompt():
    return " ".join(random.choice(WORD_LIST) for _ in range(NUM_WORDS))

def main():
    prompt = make_prompt()
    print("Typing test — type the following as quickly and accurately as you can:")
    print()
    print(prompt)
    print()
    input("Press Enter to start...")

    start = time.time()
    typed = ""
    try:
        typed = input()
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        return
    elapsed = time.time() - start
    elapsed = min(elapsed, TEST_SECONDS)

    # Compute words
    prompt_words = prompt.split()
    typed_words = typed.strip().split()
    correct = sum(1 for i, w in enumerate(typed_words) if i < len(prompt_words) and w == prompt_words[i])
    total_typed = len(typed_words)
    wpm = round((correct / elapsed) * 60) if elapsed > 0 else 0
    accuracy = round((correct / total_typed) * 100, 1) if total_typed > 0 else 0.0

    print(f"\nTime: {round(elapsed,1)}s  Correct: {correct}/{len(prompt_words)}")
    print(f"WPM (approx): {wpm}  Accuracy: {accuracy}%")

if __name__ == "__main__":
    main()
