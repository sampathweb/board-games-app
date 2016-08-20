// Create a new WebSocket.
var APP = {
  wsURL: 'ws://' + window.location.host + window.location.pathname + '/ws',
  connected: false,
  myTurn: false,
  gameOn: false,
  gameId: null,

  sendMessage: function(data) {
    APP.socket.send(JSON.stringify(data));
    console.log(data);
  },

  setButtonState: function(button, value) {

    var content = button.find(".content");
    if (content) {
      // set the game matrix
      content.text(value);  // O for opponent
      button.prop("disabled", true);
    }
  },

  messageUpdate: function(message) {
    console.log(APP.gameId)
    if (APP.gameId) {
      message = "Game: " + APP.gameId + " " + message;
      console.log(message);
    }
    $("#message").text(message);
  },

  initialize: function() {

    APP.socket = new WebSocket(APP.wsURL);

    // Show a connected message when the WebSocket is opened.
    APP.socket.onopen = function(event) {
      APP.connected = true;
      APP.messageUpdate('Connected to Game Server');
    };

    // Show a disconnected message when the WebSocket is closed.
    APP.socket.onclose = function(event) {
      APP.connected = false;
      APP.messageUpdate('Disconnected from Game Server');
      APP.gameEnded();  // Game Ended - Disconnected from Server

    };

    // Handle any errors that occur.
    APP.socket.onerror = function(error) {
      APP.connected = false;
      APP.gameOn = false;
      APP.messageUpdate('Connection Error');
    };

    // Handle messages sent by the server.
    APP.socket.onmessage = function(event) {
      var payload = JSON.parse(event.data);
      var action = payload.action;
      var data = payload.data;
      APP.serverMessage(action, data);
    };
  },

  resetBoard: function() {

    $("button.btn-marker")
      .prop("disabled", false);

    $("button.btn-marker > span")
      .text("_");
  },

  gameStarted: function(gameId) {
    APP.gameOn = true;
    APP.gameId = gameId;
    APP.resetBoard();
    $("#game-submit")[0].style.backgroundColor = "red";
    $("#game-submit").val("End Game");
  },

  gameEnded: function() {
    $("#game-room").val("");
    $("#game-submit")[0].style.backgroundColor = "";
    $("#game-submit").val("New Game");
    APP.gameOn = false;
    APP.myTurn = false;
    APP.gameId = null;
  },

  abortGame: function() {
    // End Game Selected
    var data = {
      action: "abort",
      game_id: APP.gameId
    };
    APP.sendMessage(data);
  },

  newGame: function() {
    if (!APP.connected) {
      APP.initialize();
    }
    var data = {
      action: "new"
    };
    APP.sendMessage(data);
  },

  joinGame: function(gameId) {
    if (!APP.connected) {
      APP.initialize();
    }

    var data = {
      action: "join",
      game_id: gameId
    };
    APP.sendMessage(data);
  },

  opponentMove: function(data) {
    APP.myTurn = true;

    var oppMove = data.opp_move;
    var selectedItem = $("button").filter(function() {
      return this.value == oppMove;
    });
    APP.setButtonState(selectedItem, "O");
  },

  serverMessage: function(action, data) {
    switch (action) {
      case "open":
        APP.messageUpdate("Connected to Game Server")
        break;
      case "wait-pair":
        APP.gameStarted(data.game_id);
        APP.messageUpdate("Waiting for Pair to Join..");
        break;
      case "paired":
        APP.gameStarted(data.game_id);
        APP.messageUpdate("Game Started...");
        break;
      case "move":
        APP.opponentMove(data);
        APP.messageUpdate("Your Move...")
        break;
      case "opp-move":
        APP.myTurn = false;
        APP.messageUpdate("Waiting for pair to Move...")
        break;
      case "end":
        APP.gameEnded();
        if (data.result == "W") {
          APP.messageUpdate("You Won. Congrats!")
        } else if (data.result == "L") {
          APP.messageUpdate("You Lost.  Better luck next time.")
        } else if (data.result == "D") {
          APP.messageUpdate("Draw.  Good game.");
        } else if (data.result == "A") {
          APP.messageUpdate("Game Aborted.")
        } else {
          APP.messageUpdate("Game Ended.");
        }
        break;
      case "error":
        if (data.message) {
          APP.messageUpdate(data.message)
        } else {
          APP.messageUpdate("Error Occured")
        }
        break;
       default:
        APP.messageUpdate("Unknown Action: " + action);
    }
  },

  buttonSelected: function(button) {
    APP.setButtonState(button, "X");
    // send the button value to server
    var data = {
      action: "move",
      "player_move": button.val()
    };
    APP.sendMessage(data);
  }
};

$("#game-room").on("change paste keyup", function() {
  var value = $(this).val();
  if (value) {
    $("#game-submit").val("Join Game");
  } else {
    $("#game-submit").val("New Game");
  }
});

// Initialize App
APP.initialize();

$("#game-submit").click(function() {

  if (APP.gameOn) {
    // End Game Selected
    APP.abortGame();
  } else {
    // New Game / Join Game
    var gameId = $("#game-room").val();
    if (gameId) {
      APP.joinGame(gameId);
    } else {
      APP.newGame();
    }
  }
});

$("ul.row button").on("click", function(event) {
  event.preventDefault();
  if (APP.gameOn && APP.myTurn) {
    var button = $(this);
    var my_move = button.val();
    APP.buttonSelected(button);
  }
});
