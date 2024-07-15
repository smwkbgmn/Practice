from channels.generic.websocket import AsyncWebsocketConsumer
from .consumer_pong import ConsumerPong
import json

class ConsumerMatch(AsyncWebsocketConsumer):
	tournaments = {}

	async def connect(self):
		await self.accept()

	# async def disconnect(self, close_code):
	# 	# Handle disconnection logic

	async def receive(self, text_data):
		data = json.loads(text_data)
		if data['type'] == 'join_tournament':
			await self.handle_join_tournament(data['tournament_id'])
		elif data['type'] == 'start_tournament':
			await self.handle_start_tournament(data['tournament_id'])

	async def handle_join_tournament(self, tournament_id):
		if tournament_id not in self.tournaments:
			self.tournaments[tournament_id] = {'players': [], 'games': []}
		
		self.tournaments[tournament_id]['players'].append(self.channel_name)
		
		if len(self.tournaments[tournament_id]['players']) == 4:
			await self.start_semi_finals(tournament_id)

	async def start_semi_finals(self, tournament_id):
		players = self.tournaments[tournament_id]['players']
		game1 = await self.create_game(players[0], players[1])
		game2 = await self.create_game(players[2], players[3])
		
		self.tournaments[tournament_id]['games'] = [game1, game2]

	async def create_game(self, player1, player2):
		game_id = f'game_{id(player1)}_{id(player2)}'
		# Create a new PongConsumer instance for this game
		game = ConsumerPong()
		game.room_name = game_id
		await game.connect()
		await game.handle_join_room(game_id, 'left')
		await game.handle_join_room(game_id, 'right')
		return game

	async def handle_game_finished(self, game_id, winner):
		# Logic to handle when a game finishes
		# Move winners to final round
		# Start final game when both semi-finals are complete
		pass
