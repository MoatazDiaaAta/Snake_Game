
import random
import curses

# Initialize the curses library to create the screen
screen = curses.initscr()

# Hide the mouse cursor
curses.curs_set(0)

# Get max screen height and width
screen_height, screen_width = screen.getmaxyx()

# Create a new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# Allow window to receive input from the keyboard
window.keypad(1)

# Set the delay for updating the screen
window.timeout(100)

# Set the initial position of the snake's head
snk_x = screen_width // 4
snk_y = screen_height // 2

# Define the initial position of the snake's body
snake = [
    [snk_y, snk_x],  # Head
    [snk_y, snk_x - 1],  # Body
    [snk_y, snk_x - 2]   # Tail
]

# Create the food in the middle of the window
food = [screen_height // 2, screen_width // 2]

# Add the food using the DIAMOND character
window.addch(food[0], food[1], curses.ACS_DIAMOND)

# Set the initial movement direction to right
key = curses.KEY_RIGHT

# Game loop
while True:
    # Get the next key pressed by the user
    next_key = window.getch()
    # If no key is pressed, keep the current direction
    key = key if next_key == -1 else next_key

    # Check if the snake collides with the wall or itself
    if (snake[0][0] in [0, screen_height] or
        snake[0][1] in [0, screen_width] or
        snake[0] in snake[1:]):
        curses.endwin()
        quit()

    # Determine the new position of the snake's head
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN and key != curses.KEY_UP:
        new_head[0] += 1
    if key == curses.KEY_UP and key != curses.KEY_DOWN:
        new_head[0] -= 1
    if key == curses.KEY_RIGHT and key != curses.KEY_LEFT:
        new_head[1] += 1
    if key == curses.KEY_LEFT and key != curses.KEY_RIGHT:
        new_head[1] -= 1

    # Insert the new head at the front of the snake list
    snake.insert(0, new_head)

    # Check if the snake ate the food
    if snake[0] == food:
        food = None  # Remove the food
        # Generate new food at a random location
        while food is None:
            new_food = [
                random.randint(1, screen_height - 2),
                random.randint(1, screen_width - 2)
            ]
            food = new_food if new_food not in snake else None
        window.addch(food[0], food[1], curses.ACS_DIAMOND)
    else:
        # Remove the last segment of the snake's body
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    # Update the snake's position on the screen
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
