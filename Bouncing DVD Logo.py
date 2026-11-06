
import sys
import time
import random

# Animation settings
DURATION = 30          # Animation duration in seconds
PAUSE_AMOUNT = 0.08    # Animation speed

# Border dimensions
LEFT = 2
TOP = 2
BOX_WIDTH = 70
BOX_HEIGHT = 18

# DVD logo (large 7-line design)
DVD_LOGO = [
    "#####   #   #  #####",
    "#   #   #   #  #   #",
    "#   #   #   #  #   #",
    "#   #   #   #  #   #",
    "#   #    # #   #   #",
    "#   #    # #   #   #",
    "#####     #    #####"
]

LOGO_WIDTH = len(DVD_LOGO[0])
LOGO_HEIGHT = len(DVD_LOGO)

# Colours
COLORS = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
    '\033[97m'   # White
]

RESET = '\033[0m'
BOLD = '\033[1m'


# Move terminal cursor
def goto(x, y):
    print(f'\033[{y + 1};{x + 1}H', end='')


# Clear terminal
def clear_screen():
    print('\033[2J\033[H', end='')


# Draw rectangular border
def draw_border():

    right = LEFT + BOX_WIDTH + 1
    bottom = TOP + BOX_HEIGHT + 1

    # Top border
    goto(LEFT - 1, TOP - 1)
    print('+' + '-' * BOX_WIDTH + '+', end='')

    # Bottom border
    goto(LEFT - 1, bottom)
    print('+' + '-' * BOX_WIDTH + '+', end='')

    # Side borders
    for y in range(TOP, bottom):
        goto(LEFT - 1, y)
        print('|', end='')

        goto(right, y)
        print('|', end='')


# Draw DVD logo
def draw_logo(x, y, color):

    for i, line in enumerate(DVD_LOGO):
        goto(x, y + i)
        print(BOLD + color + line + RESET, end='')


# Erase previous DVD logo
def erase_logo(x, y):

    for i in range(LOGO_HEIGHT):
        goto(x, y + i)
        print(' ' * LOGO_WIDTH, end='')


def main():

    clear_screen()

    draw_border()

    # Logo movement limits
    MIN_X = LEFT
    MAX_X = LEFT + BOX_WIDTH - LOGO_WIDTH

    MIN_Y = TOP
    MAX_Y = TOP + BOX_HEIGHT - LOGO_HEIGHT

    # Starting position
    x = (MIN_X + MAX_X) // 2
    y = (MIN_Y + MAX_Y) // 2

    # Initial movement direction
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])

    color = random.choice(COLORS)

    corner_bounces = 0
    wall_bounces = 0

    start_time = time.monotonic()

    # Hide cursor
    print('\033[?25l', end='')

    try:

        while time.monotonic() - start_time < DURATION:

            # Erase previous position
            erase_logo(x, y)

            # Calculate next position
            new_x = x + dx
            new_y = y + dy

            hit_x = False
            hit_y = False

            # Check left and right walls
            if new_x <= MIN_X:
                new_x = MIN_X
                dx = 1
                hit_x = True

            elif new_x >= MAX_X:
                new_x = MAX_X
                dx = -1
                hit_x = True

            # Check top and bottom walls
            if new_y <= MIN_Y:
                new_y = MIN_Y
                dy = 1
                hit_y = True

            elif new_y >= MAX_Y:
                new_y = MAX_Y
                dy = -1
                hit_y = True

            # Count wall bounces
            if hit_x or hit_y:

                wall_bounces += 1

                # Change colour
                color = random.choice(COLORS)

            # Count corner bounces
            if hit_x and hit_y:
                corner_bounces += 1

            # Update position
            x = new_x
            y = new_y

            # Draw logo
            draw_logo(x, y, color)

            # Display information OUTSIDE the border
            elapsed = time.monotonic() - start_time
            remaining = max(0, DURATION - int(elapsed))

            goto(LEFT, TOP + BOX_HEIGHT + 3)

            print(
                f'Wall bounces: {wall_bounces}  '
                f'Corner bounces: {corner_bounces}  '
                f'Time left: {remaining:02d}s',
                end=''
            )

            sys.stdout.flush()

            time.sleep(PAUSE_AMOUNT)

    except KeyboardInterrupt:
        pass

    finally:

        # Restore terminal
        print(RESET + '\033[?25h')

        goto(LEFT, TOP + BOX_HEIGHT + 5)

        print('DVD Animation Finished!')
        print('Total wall bounces:', wall_bounces)
        print('Total corner bounces:', corner_bounces)


if __name__ == '__main__':
    main()
