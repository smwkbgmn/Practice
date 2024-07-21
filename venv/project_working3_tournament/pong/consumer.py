import json
import random

from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .physics import PongPhysic

class Consumer(AsyncWebsocketConsumer):
	queue = {}
	group = {}
	match = {}

	@staticmethod
	def generate_id():
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
		return f"{timestamp}_{random_suffix}"

	### CONNECTION ###
	async def connect(self):
		await self.accept()

	async def disconnect(self):
		if self.group:
			await self.channel_layer.group_discard(
				self.group,
				self.channel_name	
			)
		await self.remove_player_from_queue()
	
	async def remove_player_from_queue(self):
		for size, players in self.queue.items():
			if self.channel_name in players:
				players.remove(self.channel_name)

	async def receive(self, text_data):
		data = json.loads(text_data)
		
		if data['type'] == 'requestMatch'	: await self.handle_request_match(data['tournamentSize'])
		elif data['type'] == 'joinRoom'		: await self.handle_join_room(data['gameId'], data['side'])
		elif data['type'] == 'playerMove'	: await self.handle_player_move(data['movedY'])
	
	### HANDLES ###
	async def handle_request_match(self, tourn_size):
		print("receive match request from", self.channel_name)

		if tourn_size not in self.queue:
			self.queue[tourn_size] = []
		
		self.queue[tourn_size].append(self.channel_name)
		
		if len(self.queue[tourn_size]) == tourn_size:
			await self.start_tournament(tourn_size)
		else:
			await self.send(json.dumps({
				'type'			: 'waitingForPlayers',
				'currentPlayers': len(self.queue[tourn_size]),
				'tournamentSize': tourn_size
			}))

	async def start_tournament(self, tourn_size):
		print("starting tournament for size", tourn_size)

		players = self.queue[tourn_size]
		group_id = self.generate_id()
		self.group[group_id] = {
			'players'		: players,
			'matches'		: [],
			'current_round'	: 0
		}
		
		# Create a group for this tournament
		self.tourn_id = f"tournament_{group_id}"
		
		# Add all players to the tournament group
		for player in players:
			await self.channel_layer.group_add(self.tourn_id, player)
		
		matches = self.create_matches(players)
		self.group[group_id]['matches'] = matches
		
		for i, match in enumerate(matches):
			print("assigning players to game_id group")
			await self.channel_layer.group_add(match['gameId'], match['player1'])
			await self.channel_layer.group_add(match['gameId'], match['player2'])

			print("sending start match event to", match['gameId'])
			await self.channel_layer.group_send(
				match['gameId'],
				# self.tourn_id,
				{
					'type'			: 'match_start',
					'gameId'		: match['gameId'],
					'player1'		: match['player1'],
					'player2'		: match['player2'],
					'tournamentSize': tourn_size
				}
			)
		
		self.queue[tourn_size] = []
	
	def create_matches(self, players):
		print("creating matches")

		random.shuffle(players)

		matches = []
		for i in range(0, len(players), 2):
			if i + 1 < len(players):
				game_id = self.generate_id()
				self.match[game_id] = PongPhysic(game_id, self.channel_layer)

				matches.append({
					'gameId'	: game_id,
					'player1'	: players[i],
					'player2'	: players[i + 1],
					'winner'	: None
				})
			else:
				matches.append({
					'player1'	: players[i],
					'player2'	: None,
					'winner'	: players[i]
				})
		return matches
	
	async def match_start(self, event):
		print("match starting..")

		if self.channel_name == event['player1']: side = 'left'
		elif self.channel_name == event['player2']: side = 'right'
		else: return  # This player is not part of this match

		self.game = self.match[event['gameId']]

		await self.send(json.dumps({
			'type': 'matchFound',
			'gameId': event['gameId'],
			'side': side,
			'tournamentSize': event['tournamentSize']
		}))

	async def handle_join_room(self, game_id, side):
		print("receive join request from", self.channel_name)

		await self.game.add_player(self.channel_name, side)

	async def handle_player_move(self, moved_y):
		await self.game.move_paddle(self.channel_name, moved_y)

	### EVENTS ###
	async def game_state(self, event):
		await self.send(json.dumps(event))

	# async def game_finished(self, event):
	# 	winner_side = event['winner']
	# 	winner = self.channel_name if winner_side == self.side else "opponent"
		
	# 	await self.send(json.dumps({
	# 		'type': 'gameFinish',
	# 		'winner': winner
	# 	}))

	# 	# Notify the tournament consumer about the game result
	# 	await self.channel_layer.send(
	# 		"tournament_group",
	# 		{
	# 			"type": "handle_game_finished",
	# 			"game_id": self.room_name,
	# 			"winner": self.channel_name if winner_side == self.side else None
	# 		}
	# 	)

	# 	# Clean up the game
	# 	if self.room_name in self.active_games:
	# 		del self.active_games[self.room_name]
	# 	self.game = None