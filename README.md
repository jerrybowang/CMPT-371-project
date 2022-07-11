Command to install pygame:

pip install pygame



## Token scheme

| Token name    | Format                          | Example                  | Sender | Description                                                                                              |
|:--------------|:--------------------------------|:-------------------------|:------:|:---------------------------------------------------------------------------------------------------------|
| pressed       | pressed player_number button.id | pressed 2 24             | Client | Telling sever which player pressed which button                                                          |
| player#       | player#    player_number        | player 3                 | Server | Telling client its global veritable player_number                                                        |
| player_colour | player_colour    string         | player_colour '#666666'  | Server | Telling client its global veritable  player_colour                                                       |
| player_turn   | player_turn player_number       | player_turn 2            | Server | (Brocasting) Telling client which player's turn is it right now                                          |
| remote_press  | remote_press button_id colour   | remote_press 3 '#666666' | Server | (Brocasting) Telling client other player's action, it is server's responsibility to determine the colour |
| display       | display string                  | display "a message"      | Server | Telling client the message it need to display on its message box                                         |
| end           | end                             | end                      | Server | Telling client it need to end the connection with the server                                             |

