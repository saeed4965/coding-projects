import random

# Function to calculate the total value of a hand
def calculate_hand_value(hand):
    total_value = sum(hand)
    if 11 in hand and total_value > 21:
        hand.remove(11)
        hand.append(1)
    return total_value

# Function to display the current state of the game
def display_game(player_hand, dealer_hand, reveal_second_card):
    print(f"Your hand: {player_hand}, current total: {calculate_hand_value(player_hand)}")
    if reveal_second_card:
        print(f"Dealer's hand: {dealer_hand}, total: {calculate_hand_value(dealer_hand)}")
    else:
        print(f"Dealer's hand: {dealer_hand[0]}, ?")

# Function to check the game result
def check_game_result(player_hand, dealer_hand):
    if calculate_hand_value(player_hand) == 21:
        return "You win! You have a Blackjack!"
    elif calculate_hand_value(dealer_hand) == 21:
        return "Dealer wins with a Blackjack."
    elif calculate_hand_value(player_hand) > 21:
        return "You went bust. Dealer wins."
    elif calculate_hand_value(dealer_hand) > 21:
        return "Dealer went bust. You win!"
    elif len(player_hand) == 2 and calculate_hand_value(player_hand) == 21:
        return "You win with a Blackjack!"
    elif len(dealer_hand) == 2 and calculate_hand_value(dealer_hand) == 21:
        return "Dealer wins with a Blackjack."
    elif calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
        return "You win!"
    else:
        return "Dealer wins."

# Initialize the deck
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

# Shuffle the deck
random.shuffle(deck)

while True:
    # Initialize player and dealer hands
    player_hand = []
    dealer_hand = []

    # Deal the initial 2 cards to the player and dealer
    for _ in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    # Display the game state with the dealer's second card hidden
    display_game(player_hand, dealer_hand, False)

    # Main game loop
    while True:
        # Check if the player or dealer has won
        if calculate_hand_value(player_hand) == 21 or calculate_hand_value(dealer_hand) == 21:
            break

        # Ask the player to hit or stand
        action = input("Do you want to hit or stand? ").lower()

        if action == "hit":
            player_hand.append(deck.pop())
            display_game(player_hand, dealer_hand, False)
            if calculate_hand_value(player_hand) > 21:
                print("You busted!")
                break
        elif action == "stand":
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            break
        else:
            print("Please enter 'hit' or 'stand'.")

    # Reveal the second card of the dealer and display the final game result
    display_game(player_hand, dealer_hand, True)
    print(check_game_result(player_hand, dealer_hand))

    # Ask the player if they want to play again
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        break
