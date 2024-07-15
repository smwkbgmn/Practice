import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .pong_physic import PongPhysic

class PongConsumer(AsyncWebsocketConsumer):
	active_games = {}
	waiting_players = []

	async def connect(self):
		await self.accept()
		self.room_name = None
		self.game = None

	async def disconnect(self, close_code):
		if self.room_name:
			await self.channel_layer.group_discard(
				self.room_name,
				self.channel_name
			)
			if self.room_name in self.active_games:
				del self.active_games[self.room_name]
		
		if self in self.waiting_players:
			self.waiting_players.remove(self)

	async def receive(self, text_data):
		data = json.loads(text_data)
		if data['type'] == 'requestMatch':
			await self.handle_request_match()
		elif data['type'] == 'joinRoom':
			await self.handle_join_room(data['roomId'], data['side'])
		elif data['type'] == 'playerMove':
			await self.handle_player_move(data['movedY'])

	async def handle_request_match(self):
		if self.waiting_players:
			opponent = self.waiting_players.pop(0)
			self.room_name = f'pong_{id(self)}'
			
			await self.channel_layer.group_add(
				self.room_name,
				self.channel_name
			)
			await self.channel_layer.group_add(
				self.room_name,
				opponent.channel_name
			)

			# await self.channel_layer.group_send(self.room_name, {
			# 	'type': 'matchFound',
			# 	'roomId': self.room_name
			# })

			# self.game = PongPhysic(self.room_name, self.channel_layer)
			# self.active_games[self.room_name] = self.game

			await self.send(json.dumps({
				'type': 'matchFound',
				'roomId': self.room_name,
				'side': 'left'
			}))
			await opponent.send(json.dumps({
				'type': 'matchFound',
				'roomId': self.room_name,
				'side': 'right'
			}))

			# await self.game.add_player(self.channel_name)
			# await self.game.add_player(opponent.channel_name)
			
		else:
			self.waiting_players.append(self)
			await self.send(json.dumps({
				'type': 'waitingForOpponent',
			}))

	async def handle_join_room(self, room_id, side):
		self.room_name = room_id
		await self.channel_layer.group_add(
			self.room_name,
			self.channel_name
		)
		
		self.game = self.active_games.get(room_id)
		if self.game is None:
			self.game = PongPhysic(self.room_name, self.channel_layer)
			self.active_games[room_id] = self.game
			print("making new game...")

		await self.game.add_player(self.channel_name, side)

	async def handle_player_move(self, moved_y):
		if self.game:
			await self.game.move_paddle(self.channel_name, moved_y)

	async def game_state(self, event):
		await self.send(json.dumps(event))