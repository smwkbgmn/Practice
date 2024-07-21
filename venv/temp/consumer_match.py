# import asyncio
import json
# import re
import random
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from consumer_game import ConsumerGame

class ConsumerMatch(AsyncWebsocketConsumer):
	tournaments = {}
	waiting_players = {}
	
	async def connect(self):
		await self.accept()
		self.tournament_group = None

	async def disconnect(self, close_code):
		if self.tournament_group:
			await self.channel_layer.group_discard(
				self.tournament_group,
				self.channel_name
			)
		await self.remove_player_from_waiting()

	@staticmethod
	def generate_valid_room_id():
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
		return f"room_{timestamp}_{random_suffix}"

	async def receive(self, text_data):
		data = json.loads(text_data)
		if data['type'] == 'requestMatch':
			await self.handle_request_match(data['tournamentSize'])

	async def handle_request_match(self, tournament_size):
		if tournament_size not in self.waiting_players:
			self.waiting_players[tournament_size] = []
		
		self.waiting_players[tournament_size].append(self.channel_name)
		
		if len(self.waiting_players[tournament_size]) == tournament_size:
			await self.start_tournament(tournament_size)
		else:
			await self.send(json.dumps({
				'type': 'waitingForPlayers',
				'currentPlayers': len(self.waiting_players[tournament_size]),
				'tournamentSize': tournament_size
			}))

	async def start_tournament(self, tournament_size):
		players = self.waiting_players[tournament_size]
		tournament_id = self.generate_valid_room_id()
		self.tournaments[tournament_id] = {
			'players': players,
			'matches': [],
			'current_round': 0
		}
		
		# Create a group for this tournament
		self.tournament_group = f"tournament_{tournament_id}"
		
		# Add all players to the tournament group
		for player in players:
			await self.channel_layer.group_add(
				self.tournament_group,
				player
			)
		
		matches = self.create_matches(players)
		self.tournaments[tournament_id]['matches'] = matches
		
		for i, match in enumerate(matches):
			room_id = self.generate_valid_room_id()
			await self.channel_layer.group_send(
				self.tournament_group,
				{
					'type': 'match_start',
					'roomId': room_id,
					'player1': match['player1'],
					'player2': match['player2'],
					'tournamentSize': tournament_size
				}
			)
		
		self.waiting_players[tournament_size] = []
	
	def create_matches(self, players):
		random.shuffle(players)
		matches = []
		for i in range(0, len(players), 2):
			if i + 1 < len(players):
				matches.append({
					'game': ConsumerGame(),
					'player1': players[i],
					'player2': players[i + 1],
					'winner': None
				})
			else:
				matches.append({
					'player1': players[i],
					'player2': None,
					'winner': players[i]
				})
		return matches

	async def match_start(self, event):
		if self.channel_name == event['player1']:
			side = 'left'
		elif self.channel_name == event['player2']:
			side = 'right'
		else:
			return  # This player is not part of this match

		await self.send(json.dumps({
			'type': 'matchFound',
			'gameId': event['gameId'],
			'side': side,
			'tournamentSize': event['tournamentSize']
		}))

	async def remove_player_from_waiting(self):
		for size, players in self.waiting_players.items():
			if self.channel_name in players:
				players.remove(self.channel_name)

	async def remove_player_from_tournaments(self):
		for tournament_id, tournament in self.tournaments.items():
			if self.channel_name in tournament['players']:
				tournament['players'].remove(self.channel_name)
				if len(tournament['players']) == 0:
					del self.tournaments[tournament_id]
				else:
					for match in tournament['matches']:
						if match['player1'] == self.channel_name:
							match['winner'] = match['player2']
						elif match['player2'] == self.channel_name:
							match['winner'] = match['player1']
					await self.advance_tournament(tournament_id)

	# async def advance_tournament(self, tournament_id):
	# 	# Implementation for advancing the tournament
	# 	pass

