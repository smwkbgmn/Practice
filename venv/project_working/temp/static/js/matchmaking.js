document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');
    const findMatchButton = document.getElementById('findMatch');
    const statusDiv = document.getElementById('status');

    if (findMatchButton) {
        findMatchButton.addEventListener('click', () => {
            statusDiv.textContent = 'Searching for a match...';
            socket.send(JSON.stringify({type: 'requestMatch'}));
        });
    }

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'matchFound') {
            statusDiv.textContent = 'Match found! Starting game...';
            window.location.href = `/game/?roomId=${data.roomId}`;
        }
    };
});