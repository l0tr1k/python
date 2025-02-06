#l0tr1k game connect four
#version 1.0

from turtle import *
from freegames import line

# Game state variables
turns = {'red': 'yellow', 'yellow': 'red'}  # Player turn order
state = {
    'player': 'yellow',  # Current player
    'rows': [0] * 7,     # Number of discs in each column (7 columns total)
    'board': [[None for _ in range(6)] for _ in range(7)],  # 7x6 board
    'game_over': False   # Win state flag
}

def grid():
    """Draw game grid using turtle graphics"""
    bgcolor('light blue')
    # Draw vertical lines (columns)
    for x in range(-150, 200, 50):
        line(x, -200, x, 200)
    # Draw empty circles (slots)
    for x in range(-175, 200, 50):
        for y in range(-175, 200, 50):
            up()
            goto(x, y)
            dot(40, 'white')
    update()

def win_check(col, row, player):
    """Check four possible winning directions"""
    # Vertical check
    if state['rows'][col] >= 4:
        count = 0
        for r in range(6):
            if state['board'][col][r] == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0  # Reset count when different color found
    
    # Horizontal check
    consecutive = 0
    for c in range(7):
        consecutive = consecutive + 1 if state['board'][c][row] == player else 0
        if consecutive >= 4:
            return True
    
    # Diagonal checks
    directions = [(1,1), (1,-1)]  # Down-right, Up-right
    for dx, dy in directions:
        count = 1
        for i in range(1,4):
            x, y = col + dx*i, row + dy*i
            if 0 <= x < 7 and 0 <= y < 6:
                if state['board'][x][y] == player:
                    count +=1
                else:
                    break
        if count >=4:
            return True
    
    return False

def tap(x, y):
    """Handle mouse click input"""
    if state['game_over']:
        return  # Ignore input after game ends
    
    player = state['player']
    col = int((x + 200) // 50)  # Convert click position to column index (0-6)
    
    # Validate column
    if col < 0 or col > 6 or state['rows'][col] >= 6:
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
    
    # Check win condition
    if win_check(col, row, player):
        state['game_over'] = True
        up()
        goto(-190, 0)
        color('black')
        write(f"Player {player.capitalize()} Wins!", font=('Arial', 24, 'normal'))
    else:
        state['player'] = turns[player]

# Game initialization
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
onscreenclick(tap)
done()