import PongRender from './PongRender.js';

document.addEventListener('DOMContentLoaded', () => {
	const urlParams = new URLSearchParams(window.location.search);
	const roomId = urlParams.get('roomId');
	const side = urlParams.get('side');
	// const roomId = "{{ room_id }}";

	console.log("player init renderer resverse_mode with", side);

	if (!roomId) {
		alert('No room ID provided. Redirecting to matchmaking.');
		window.location.href = '/index.html';
		return;
	}

	const gameContainer = document.getElementById('game-container');
	const game = new PongRender(roomId, side);
});