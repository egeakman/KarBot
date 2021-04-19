player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@Bot.command()
async def xox(ctx,p2: discord.Member):
    if p2.id==802209233734205470:
        await ctx.send("I can't play with you right now :(")
        return
    """Play XOX with someone you mention!"""
    global count
    global player1
    global player2
    global turn
    global gameOver

    if ctx.author.id == p2.id:
        await ctx.send("You are not alone, I'm by your side. I hope I will be able to play with you soon :).")
    elif gameOver:
        await ctx.send("The areas are divided into 9 areas: 1 is the upper left and 9 is the lower right, In the game, type ?place 5 to place a mark in a field, type ?finish to finish the game.")



        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = ctx.author
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("<@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("Finish this game before start a new one.")

@Bot.command(hidden=True)
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
                await ctx.send(f"{player2.mention}'s turn.")
            elif turn == player2:
                mark = ":o2:"
                await ctx.send(f"{player1.mention}'s turn'.")
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + " won!")
                elif count >= 9:
                    await ctx.send("It's a draw!")

                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Please pick a number between 1 and 9.")
        else:
            await ctx.send("It's not your turn.")
    else:
        await ctx.send("Please make a new game by typing ?xox.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@xox.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a player for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure you've done everything right. It looks like there are some problems about the player you mentioned.")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please choose where you wanna mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please pick a number between 1 and 9.")
###############################################################################
@Bot.command(hidden=True)
async def finish(ctx):
    global gameOver
    if gameOver==False:
        gameOver = True
        await ctx.send("The game is finished.")
    else:
        await ctx.send("I can't see any games currently being played.")
