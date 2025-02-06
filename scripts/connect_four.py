#l0tr1k game connect four
#version 1.0

from turtle import *
from freegames import line

# Game state variables - updated for 8x8 grid
turns = {'red': 'yellow', 'yellow': 'red'}
state = {
    'player': 'yellow',
    'rows': [0] * 8,     # Changed to 8 columns
    'board': [[None for _ in range(8)] for _ in range(8)],  # Changed to 8x8
    'game_over': False
}

def grid():
    """Draw game grid using turtle graphics"""
    bgcolor('light blue')
    # Draw vertical lines for 8 columns
    for x in range(-200, 200, 50):  # Adjusted range for 8 columns
        line(x, -200, x, 200)
    # Draw empty circles for 8x8 grid
    for x in range(-175, 200, 50):
        for y in range(-175, 200, 50):
            up()
            goto(x, y)
            dot(40, 'white')
    update()

def win_check(col, row, player):
    """Check four possible winning directions in 8x8 grid"""
    # Vertical check
    count = 0
    for r in range(8):  # Changed to check 8 rows
        if state['board'][col][r] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Horizontal check
    consecutive = 0
    for c in range(8):  # Changed to check 8 columns
        consecutive = consecutive + 1 if state['board'][c][row] == player else 0
        if consecutive >= 4:
            return True
    
    # Diagonal checks - fixed implementation
    directions = [(1,1), (1,-1), (-1,1), (-1,-1)]  # All diagonal directions
    for dx, dy in directions:
        count = 1  # Start with 1 for current piece
        # Check forward direction
        x, y = col, row
        for _ in range(3):  # Need 3 more pieces to win
            x, y = x + dx, y + dy
            if 0 <= x < 8 and 0 <= y < 8 and state['board'][x][y] == player:
                count += 1
            else:
                break
        # Check opposite direction
        x, y = col - dx, row - dy
        while 0 <= x < 8 and 0 <= y < 8 and state['board'][x][y] == player:
            count += 1
            x, y = x - dx, y - dy
        if count >= 4:
            return True
    
    return False

def tap(x, y):
    """Handle mouse click input"""
    if state['game_over']:
        return
    
    player = state['player']
    col = int((x + 200) // 50)
    
    # Validate column for 8x8 grid
    if col < 0 or col > 7 or state['rows'][col] >= 8:  # Changed bounds to 7 and 8
        return
    
    # Place disc
    row = state['rows'][col]
    x_pos = col * 50 - 175
    y_pos = row * 50 - 175
    up()
    goto(x_pos, y_pos)
    dot(40, player)
    
    # Update game state
    state['board'][col][row] = player
    state['rows'][col] += 1
    
    if win_check(col, row, player):
        state['game_over'] = True
        up()
        goto(-190, 0)
        color('black')
        write(f"Player {player.capitalize()} Wins!", font=('Arial', 24, 'normal'))
    else:
        state['player'] = turns[player]

# Game initialization with larger window for 8x8 grid
setup(470, 470, 370, 0)  # Increased window size
hideturtle()
tracer(False)
grid()
onscreenclick(tap)
done()