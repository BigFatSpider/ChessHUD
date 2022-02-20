import chess
import chess.pgn
import PySimpleGUI as sg
from io import StringIO

def main():
    defaulttheme = 'DarkGrey8'
    themes = ['DarkBlue3', 'DarkAmber', 'DarkBlack1', 'DarkBlue', 'DarkBlue14', 'DarkBlue2',
              'DarkBrown2', 'DarkBrown5', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen7',
              'DarkGrey1', 'DarkGrey3', 'DarkGrey5', defaulttheme, 'DarkPurple7', 'DarkTanBlue', 'DarkTeal10']
    sg.theme(defaulttheme)
    pieceset = 'cburnett'
    piecesetpath = 'images/pieces/' + pieceset + '/'
    br = piecesetpath + 'bR.png'
    wr = piecesetpath + 'wR.png'
    bb = piecesetpath + 'bB.png'
    wb = piecesetpath + 'wB.png'
    bn = piecesetpath + 'bN.png'
    wn = piecesetpath + 'wN.png'
    bq = piecesetpath + 'bQ.png'
    wq = piecesetpath + 'wQ.png'
    bk = piecesetpath + 'bK.png'
    wk = piecesetpath + 'wK.png'
    bp = piecesetpath + 'bP.png'
    wp = piecesetpath + 'wP.png'
    b = piecesetpath + 'blank.png'
    c2i = {'P': wp, 'R': wr, 'N': wn, 'B': wb, 'Q': wq, 'K': wk,
           'p': bp, 'r': br, 'n': bn, 'b': bb, 'q': bq, 'k': bk,
           '.': b}
    sqpixels = 85
    def sqsize():
        return (sqpixels, sqpixels)
    def sq(p, c, k):
        return sg.Button(image_filename=p, image_size=sqsize(), button_color=c, pad=0, key=k)
    movestack = []
    board = chess.Board()
    defaultsquaresstr = 'Light/Dark'
    squaresstrs = [defaultsquaresstr, 'Light', 'Dark']
    flipped = False
    moveinput = lambda: sg.Input(size=12, key='Moveinput', tooltip='Move, in standard algebraic notation')
    movebutton = lambda: sg.Button('Move', bind_return_key=True, tooltip='Make the move specified to the right (enter/return)')
    promoelem = lambda: sg.Combo(['q','r','n','b'], default_value='q', enable_events=True, key='Promote',
                                 tooltip='Promotion piece for click-moving on the board above')
    firstbutton = lambda: sg.Button('<<', tooltip='To starting position (up arrow)')
    leftbutton = lambda: sg.Button('<-', tooltip='Back one half-move (left arrow)')
    rightbutton = lambda: sg.Button('->', tooltip='Forward one half-move (right arrow)')
    lastbutton = lambda: sg.Button('>>', tooltip='To last half-move (down arrow)')
    flipbutton = lambda: sg.Button('Flip', tooltip='Flip the board to intimidate your opponents')
    attackbutton = lambda: sg.Button('Attack', tooltip='Toggle attack space highlighting')
    colorbutton = lambda: sg.Button('Color', tooltip='Cycle through attack space highlighting colors')
    squareselem = lambda: sg.Combo(squaresstrs, default_value=defaultsquaresstr, enable_events=True, key='Squares',
                                   tooltip='Square shading')
    themeelem = lambda: sg.Combo(themes, default_value=defaulttheme, enable_events=True, key='Theme',
                                 tooltip='Color scheme for the non-board UI')
    eventsbutton = lambda: sg.Button('Debug events', tooltip='Toggle display of unhandled UI events')
    jumpbutton = lambda: sg.Button('Jump', tooltip='Jump to half-move number specified to the right')
    jumpinput = lambda: sg.Input(size=6, key='Jumpinput', tooltip='Half-move number')
    pixbutton = lambda: sg.Button('Pix', tooltip='Update board square size as specified to the right')
    pixinput = lambda: sg.Input(size=12, key='Pixinput', tooltip='Board square size in pixels')
    pixtext = lambda: sg.Text(str(sqpixels), key='Pixtext', tooltip='Current square size in pixels')
    pgninput = lambda: sg.Input(key='PGNinput', tooltip='PGN text')
    pgnbutton = lambda: sg.Button('PGN', tooltip='Import moves from PGN text specified to the right')
    msgoutput = lambda: sg.Text('', tooltip='Messages appear here')
    colorsetting = 0
    clickmove = ''
    squarenames = set(chess.SQUARE_NAMES)
    attackcolors = [['6f', '97', 'af', 'bd', 'c8', 'd2', 'db', 'e3', 'ea', 'f0', 'f5', 'f9', 'fc', 'fd', 'fe', 'ff'],
                    ['5f', '87', '9f', 'ad', 'b8', 'c2', 'cb', 'd3', 'da', 'e0', 'e5', 'e9', 'ec', 'ed', 'ee', 'ef']]
    ls = '#' + attackcolors[0][0] + attackcolors[0][0] + attackcolors[0][0]
    ds = '#' + attackcolors[1][0] + attackcolors[1][0] + attackcolors[1][0]
    def createwindow():
        msg = msgoutput()
        lboard = [[sq(br,ls,'a8'), sq(bn,ds,'b8'), sq(bb,ls,'c8'), sq(bq,ds,'d8'), sq(bk,ls,'e8'), sq(bb,ds,'f8'), sq(bn,ls,'g8'), sq(br,ds,'h8')],
                  [sq(bp,ds,'a7'), sq(bp,ls,'b7'), sq(bp,ds,'c7'), sq(bp,ls,'d7'), sq(bp,ds,'e7'), sq(bp,ls,'f7'), sq(bp,ds,'g7'), sq(bp,ls,'h7')],
                  [sq(b,ls,'a6'), sq(b,ds,'b6'), sq(b,ls,'c6'), sq(b,ds,'d6'), sq(b,ls,'e6'), sq(b,ds,'f6'), sq(b,ls,'g6'), sq(b,ds,'h6')],
                  [sq(b,ds,'a5'), sq(b,ls,'b5'), sq(b,ds,'c5'), sq(b,ls,'d5'), sq(b,ds,'e5'), sq(b,ls,'f5'), sq(b,ds,'g5'), sq(b,ls,'h5')],
                  [sq(b,ls,'a4'), sq(b,ds,'b4'), sq(b,ls,'c4'), sq(b,ds,'d4'), sq(b,ls,'e4'), sq(b,ds,'f4'), sq(b,ls,'g4'), sq(b,ds,'h4')],
                  [sq(b,ds,'a3'), sq(b,ls,'b3'), sq(b,ds,'c3'), sq(b,ls,'d3'), sq(b,ds,'e3'), sq(b,ls,'f3'), sq(b,ds,'g3'), sq(b,ls,'h3')],
                  [sq(wp,ls,'a2'), sq(wp,ds,'b2'), sq(wp,ls,'c2'), sq(wp,ds,'d2'), sq(wp,ls,'e2'), sq(wp,ds,'f2'), sq(wp,ls,'g2'), sq(wp,ds,'h2')],
                  [sq(wr,ds,'a1'), sq(wn,ls,'b1'), sq(wb,ds,'c1'), sq(wq,ls,'d1'), sq(wk,ds,'e1'), sq(wb,ls,'f1'), sq(wn,ds,'g1'), sq(wr,ls,'h1')]]
        buttons = [movebutton(), firstbutton(), leftbutton(), rightbutton(), lastbutton(),
                   flipbutton(), attackbutton(), colorbutton(), jumpbutton(), pixbutton(), eventsbutton(), pgnbutton()]
        layout = [lboard,
                  [buttons[0], moveinput(), sg.Text('Promo:'), promoelem(), themeelem()],
                  [buttons[1], buttons[2], buttons[3], buttons[4], buttons[5], buttons[6], buttons[7], squareselem()],
                  [buttons[8], jumpinput(), buttons[9], pixinput(), pixtext(), buttons[10]],
                  [buttons[11], pgninput()],
                  [msg]]
        window = sg.Window('Chess HUD', layout, return_keyboard_events=True)
        window.finalize()
        for row in lboard:
            for butt in row:
                butt.block_focus()
        for butt in buttons:
            butt.block_focus()
        window['Moveinput'].set_focus()
        return window, lboard, msg
    window, lboard, msg = createwindow()
    attackoverlay = True
    attackspace = []
    for idx in range(64):
        attackspace.append([0, 0])
    c2team = {'P': 0, 'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0,
              'p': 1, 'r': 1, 'n': 1, 'b': 1, 'q': 1, 'k': 1,
              '.': None}
    squareshading = 0
    def updateattack(bs):
        for squ in attackspace:
            squ[0] = 0
            squ[1] = 0
        if attackoverlay:
            bidx = 0
            for idx in range(64):
                team = c2team[bs[bidx]]
                bidx += 2
                if team is None:
                    continue
                row = idx // 8
                col = idx % 8
                bbrow = 7 - row
                bbidx = bbrow * 8 + col
                bbmask = board.attacks_mask(bbidx)
                for bbidx in range(64):
                    if ((1 << bbidx) & bbmask) > 0:
                        bbrow = bbidx // 8
                        col = bbidx % 8
                        row = 7 - bbrow
                        aidx = row * 8 + col
                        attackspace[aidx][team] += 1
        def getcolor(cidx, idx_in):
            team0 = lambda: attackspace[idx][0]
            team1 = lambda: attackspace[idx][1]
            zero = lambda: 0
            colorfuncs = [[team0, team1, zero],
                          [team0, zero, team1],
                          [zero, team0, team1],
                          [team1, team0, zero],
                          [team1, zero, team0],
                          [zero, team1, team0]]
            attackcolor = colorfuncs[colorsetting][cidx]()
            # Blue is too dark
            return 2*attackcolor if cidx == 2 and attackcolor > 0 and 2*attackcolor < 15 else attackcolor
        bidx = 0
        for idx in range(64):
            acidx = (idx + (idx // 8)) % 2 if squareshading == 0 else 0 if squareshading == 1 else 1
            bgcolor = ('#' + attackcolors[acidx][getcolor(0, idx)]
                           + attackcolors[acidx][getcolor(1, idx)]
                           + attackcolors[acidx][getcolor(2, idx)])
            lidx = 63 - idx if flipped else idx
            lboard[lidx // 8][lidx % 8].update(image_filename=c2i[bs[bidx]], image_size=sqsize(), button_color=bgcolor)
            bidx += 2
    updateattack(str(board))
    def uparrow():
        try:
            while True:
                movestack.append(board.pop())
        except IndexError as e:
            msg.update('')
            updateattack(str(board))
    def leftarrow():
        try:
            movestack.append(board.pop())
            msg.update('')
            updateattack(str(board))
        except IndexError as e:
            pass
    def rightarrow():
        try:
            if len(movestack) > 0:
                board.push(movestack.pop())
                msg.update('')
                updateattack(str(board))
        except ValueError as e:
            print(e)
            msg.update(str(e))
    def downarrow():
        while len(movestack) > 0:
            board.push(movestack.pop())
        msg.update('')
        updateattack(str(board))
    showunhandled = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Move':
            try:
                elem = window['Moveinput']
                movesan = elem.get()
                if movesan != '':
                    move = board.push_san(movesan)
                    if len(movestack) > 0:
                        if move == movestack[-1]:
                            movestack.pop()
                        else:
                            movestack.clear()
                    elem.update('')
                    msg.update('')
                    updateattack(str(board))
            except ValueError as e:
                print(e)
                msg.update(str(e))
        elif event == 'Promote':
            window['Moveinput'].set_focus()
        elif event == '<<' or event.startswith('Up:'):
            uparrow()
        elif event == '<-' or event.startswith('Left:'):
            leftarrow()
        elif event == '->' or event.startswith('Right:'):
            rightarrow()
        elif event == '>>' or event.startswith('Down:'):
            downarrow()
        elif event == 'Flip':
            flipped = not flipped
            updateattack(str(board))
            msg.update('')
        elif event == 'Attack':
            attackoverlay = not attackoverlay
            updateattack(str(board))
        elif event == 'Color':
            colorsetting = (colorsetting + 1) % 6
            updateattack(str(board))
        elif event == 'Squares':
            squareshading = squaresstrs.index(window['Squares'].get())
            window['Moveinput'].set_focus()
            updateattack(str(board))
        elif event == 'Theme':
            theme = window['Theme'].get()
            squaresval = window['Squares'].get()
            promoteval = window['Promote'].get()
            window.close()
            sg.theme(theme)
            window, lboard, msg = createwindow()
            window['Theme'].update(theme)
            window['Squares'].update(squaresval)
            window['Promote'].update(promoteval)
            updateattack(str(board))
        elif event == 'Debug events':
            showunhandled = not showunhandled
            if not showunhandled:
                msg.update('')
        elif event == 'Jump':
            try:
                elem = window['Jumpinput']
                movenum = int(elem.get())
                try:
                    while True:
                        movestack.append(board.pop())
                except IndexError as e:
                    pass
                numpushes = min(movenum, len(movestack))
                for n in range(numpushes):
                    board.push(movestack.pop())
                elem.update('')
                msg.update('')
                updateattack(str(board))
            except ValueError as e:
                print(e)
                msg.update(str(e))
        elif event == 'Pix':
            try:
                elem = window['Pixinput']
                sqpixels = int(elem.get())
                elem.update('')
                if sqpixels > 120:
                    sqpixels = 120
                elif sqpixels < 20:
                    sqpixels = 20
                window['Pixtext'].update(str(sqpixels))
                msg.update('')
                updateattack(str(board))
            except ValueError as e:
                print(e)
                msg.update(str(e))
        elif event == 'PGN':
            elem = window['PGNinput']
            try:
                game = chess.pgn.read_game(StringIO(elem.get()))
                if game is not None:
                    board = game.board()
                    if board is not None:
                        for move in game.mainline_moves():
                            board.push(move)
                        movestack.clear()
                        try:
                            while True:
                                movestack.append(board.pop())
                        except IndexError as e:
                            pass
                        elem.update('')
                        msg.update('')
                        updateattack(str(board))
            except Exception as e:
                emsg = 'pgn exception: ' + str(e)
                print(emsg)
                msg.update(emsg)
        elif event in squarenames:
            squarename = chess.SQUARE_NAMES[63 - chess.SQUARE_NAMES.index(event)] if flipped else event
            if clickmove == '':
                clickmove = squarename
                msg.update(clickmove)
            elif clickmove == squarename:
                clickmove = ''
                msg.update('')
            elif clickmove in squarenames:
                if board.color_at(chess.SQUARE_NAMES.index(clickmove)) == board.turn and board.color_at(chess.SQUARE_NAMES.index(squarename)) != board.turn:
                    try:
                        dopromote = board.piece_type_at(chess.SQUARE_NAMES.index(clickmove)) == 1 and (squarename[1] == '1' or squarename[1] == '8')
                        clickmove = clickmove + (squarename + window['Promote'].get() if dopromote else squarename)
                        move = board.push_uci(clickmove)
                        clickmove = ''
                        if len(movestack) > 0:
                            if move == movestack[-1]:
                                movestack.pop()
                            else:
                                movestack.clear()
                        msg.update('')
                        updateattack(str(board))
                    except ValueError as e:
                        clickmove = ''
                        msg.update('')
                else:
                    clickmove = squarename
                    msg.update(clickmove)
        elif showunhandled:
            print(event)
            msg.update(event)
    window.close()

if __name__ == '__main__':
    main()

