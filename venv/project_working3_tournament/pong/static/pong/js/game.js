import PongRender from './render.js';

document.addEventListener('DOMContentLoaded', () => {
	const urlParams = new URLSearchParams(window.location.search);
	const gameId = urlParams.get('gameId');
	const side = urlParams.get('side');

	if (!gameId) {
		alert('No room ID provided. Redirecting to matchmaking.');
		window.location.href = '/index.html';
		return;
	}

	const gameContainer = document.getElementById('game-container');
	const game = new PongRender(gameId, side);
});