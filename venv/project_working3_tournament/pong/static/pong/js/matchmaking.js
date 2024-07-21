import PongRender from "./render.js";

document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/pong');
    const findMatchButton = document.getElementById('findMatch');
    const statusDiv = document.getElementById('status');
    const tournamentSizeSelect = document.getElementById('tournamentSize');
    const gameContainer = document.getElementById('game-container');

    if (findMatchButton) {
        findMatchButton.addEventListener('click', () => {
            const tournamentSize = parseInt(tournamentSizeSelect.value);
            statusDiv.textContent = `Searching for a ${tournamentSize}-player tournament...`;
            socket.send(JSON.stringify({
                type: 'requestMatch',
                tournamentSize: tournamentSize
            }));
        });
    }

    socket.onopen = function(event) {
        statusDiv.textContent = 'Connected to server. Select tournament size and click "Find Match".';
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.type === 'matchFound') {
            statusDiv.textContent = 'Match found! Starting game...';
            // Instead of navigating, we'll start the game here
            startGame(data.gameId, data.side, data.tournamentSize, socket);
        } else if (data.type === 'waitingForPlayers') {
            statusDiv.textContent = `Waiting for more players... ${data.currentPlayers}/${data.tournamentSize}`;
        }
    };

    socket.onerror = function(error) {
        statusDiv.textContent = 'Error connecting to the server. Please try again later.';
        console.error('WebSocket Error:', error);
    };

    socket.onclose = function(event) {
        statusDiv.textContent = 'Disconnected from server. Please refresh the page to reconnect.';
    };
});

function startGame(gameId, side, tournamentSize, socket) {
    // Hide matchmaking UI
    document.getElementById('matchmaking-container').style.display = 'none';
    // Show game UI
    document.getElementById('game-container').style.display = 'block';

    // Initialize the game
    new PongRender(gameId, side, socket);
}