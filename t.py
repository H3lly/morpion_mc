    while grids[0].gameover() == -1:
        shot = -1
        while shot < 0 or shot >= NB_CELLS:
            shot = int(input ("Quelle case allez-vous jouer ?"))
        if (grids[0].cells[shot] != EMPTY:
            grids[current_player].cells[shot] = curret_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
            other_player = current_player%2+1
        for client in connexions_clients:
            connexions_clients[client].send(bytes(client+"\n", "utf8"))
    print("game over")
    message_pour_tous("grids[0].display()\n")
    
