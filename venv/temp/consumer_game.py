import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .physics import PongPhysic

class Consumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		self.room_name = None
		self.game = None
		self.side = None

	async def disconnect(self, close_code):
		if self.room_name:
			await self.channel_layer.group_discard(
				self.room_name,
				self.channel_name
				
			)
			if self.room_name in self.active_games:
				del self.active_games[self.room_name]
		
		if self.game:
			await self.game.remove_player(self.channel_name)

	async def receive(self, text_data):
		data = json.loads(text_data)
		
		if data['type'] == 'joinRoom':
			await self.handle_join_room(data['roomId'], data['side'])
		elif data['type'] == 'playerMove':
			await self.handle_player_move(data['movedY'])

	async def handle_join_room(self, room_id, side):
		print("handle_join_room", room_id)
		self.room_name = room_id
		# self.room_name = self.validate_room_id(room_id)
		self.side = side
		await self.channel_layer.group_add(self.room_name, self.channel_name)
		
		self.game = self.active_games.get(room_id)
		if self.game is None:
			self.game = PongPhysic(self.room_name, self.channel_layer)
			self.active_games[room_id] = self.game
			print(f"Creating a new game in room {room_id}...")

		await self.game.add_player(self.channel_name, side)

	async def handle_player_move(self, moved_y):
		if self.game:
			await self.game.move_paddle(self.channel_name, moved_y)

	async def game_state(self, event):
		await self.send(json.dumps(event))

	async def game_finished(self, event):
		winner_side = event['winner']
		winner = self.channel_name if winner_side == self.side else "opponent"
		
		await self.send(json.dumps({
			'type': 'gameFinish',
			'winner': winner
		}))

		# Notify the tournament consumer about the game result
		await self.channel_layer.send(
			"tournament_group",
			{
				"type": "handle_game_finished",
				"game_id": self.room_name,
				"winner": self.channel_name if winner_side == self.side else None
			}
		)

		# Clean up the game
		if self.room_name in self.active_games:
			del self.active_games[self.room_name]
		self.game = None