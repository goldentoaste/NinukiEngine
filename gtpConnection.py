

from sys import stdin, stderr, stdout
from board import Board, BLACK, WHITE, EMPTY, opponent, t2c, t2p, p2t
from typing import List
import re
import traceback

class GtpConnection:
    
    
    def __init__(self, board:Board):
        
        self.board = board

        self.commands = {
            "quit": self.quit,
            "boardsize": self.boardsize,
            "showboard": self.showboard,
            "clear_board": self.clearBoard,
            "genmove": self.genMove,
            "play": self.playMove,
            "legal_moves": self.getLegalMoves,
            "echo":self.echo
        }
    
    def startCon(self):
        """
        Start a GTP connection. 
        This function continuously monitors standard input for commands.
        """
        line = stdin.readline()
        while line:
            self.get_cmd(line)
            line = stdin.readline()

    def get_cmd(self, command: str) -> None:
        """
        Parse command string and execute it
        """
        if len(command.strip(" \r\t")) == 0:
            return
        if command[0] == "#":
            return
        # Strip leading numbers from regression tests
        if command[0].isdigit():
            command = re.sub("^\d+", "", command).lstrip()

        elements: List[str] = command.split()
        if not elements:
            return
        command_name: str = elements[0]
        args: List[str] = elements[1:]


        if command_name in self.commands:
            try:
                self.commands[command_name](args)
            except Exception as e:
                self.debug_msg("Error executing command {}\n".format(str(e)))
                self.debug_msg("Stack Trace:\n{}\n".format(traceback.format_exc()))
                raise e
        else:
            self.debug_msg("Unknown command: {}\n".format(command_name))
            self.error("Unknown command")
            stdout.flush()
            
    def debug_msg(self, msg: str) -> None:
        """ Write msg to the debug stream """
        stderr.write(msg)
        stderr.flush()
        
    def respond(self, response: str = "") -> None:
        """ Send response to stdout """
        stdout.write("= {}\n\n".format(response))
        stdout.flush()
        
    def quit(self, *args):
        self.respond()
        exit()
        
        
    def boardsize(self, size):
        size = int(size)
        self.board = Board(size)
        
        # TODO remake player
        
        self.respond()
        
    def showboard(self, *args):
        self.respond(
            str(self.board)
        )
    
    def clearBoard(self, *args):
        self.board.reset()
        self.respond()
        
        
    def genMove(self, color:str):
        # TODO convert color to generate position
        pass
    

    def playMove(self, color:str, move:str):
        color = t2c(color.lower())
        move = t2p(move)
        self.board.playNoUndo(*move, color)
        self.respond()
    
    def getLegalMoves(self):
        empties = self.board.emptyPoints()
        self.respond(
            ", ".join([p2t(p) for p in empties])
        )
    
    def echo(self, *messages):
        # respond with whatever args are given
        msg = "".join(messages)
        self.respond(msg)