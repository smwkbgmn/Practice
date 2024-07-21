import asyncio
# import json
import random
import pymunk

class PongPhysic:
	def __init__(self, room_id, channel_layer):
		self.room_id = room_id
		self.channel_layer = channel_layer
		self.players = {"left": None, "right": None}
		
		self.ball_speed_default = 3
		self.ball_speed_increment = 0.5
		self.ball_time_scale = 1
		self.paddle_random_bounce_scale = 0.3

		self.setup()

	def setup(self):
		self.space = pymunk.Space()
		self.space.gravity = (0, 0)

		ball_body = pymunk.Body(1, 1)
		ball_body.position = 0, 0
		self.ball = pymunk.Circle(ball_body, 0.1)
		self.ball.elasticity = 1

		paddle_mass = 1000 
		paddle_moment = pymunk.moment_for_box(paddle_mass, (0.2, 1))

		self.paddle_left_body = pymunk.Body(paddle_mass, paddle_moment, body_type=pymunk.Body.KINEMATIC)
		self.paddle_left_body.position = -4.5, 0
		self.paddle_left = pymunk.Poly.create_box(self.paddle_left_body, (0.2, 1))
		self.paddle_left.elasticity = 1
		self.paddle_left.collision_type = 2

		self.paddle_right_body = pymunk.Body(paddle_mass, paddle_moment, body_type=pymunk.Body.KINEMATIC)
		self.paddle_right_body.position = 4.5, 0
		self.paddle_right = pymunk.Poly.create_box(self.paddle_right_body, (0.2, 1))
		self.paddle_right.elasticity = 1
		self.paddle_right.collision_type = 3

		self.wall_top = pymunk.Segment(self.space.static_body, (-4, -5), (4, -5), 0.05)
		self.wall_bottom = pymunk.Segment(self.space.static_body, (-4, 5), (4, 5), 0.05)
		self.wall_top.elasticity = self.wall_bottom.elasticity = 1

		self.space.add(ball_body, self.ball,
			self.paddle_left_body, self.paddle_left,
			self.paddle_right_body, self.paddle_right,
			self.wall_top, self.wall_bottom)
		self.space.add_collision_handler(0, 0).post_solve = self.handle_collision

	def handle_collision(self, arbiter, space, data):
		if self.ball in (arbiter.shapes[0], arbiter.shapes[1]):
			speed = self.ball.body.velocity.length

			if self.paddle_left in (arbiter.shapes[0], arbiter.shapes[1]) or \
				self.paddle_right in (arbiter.shapes[0], arbiter.shapes[1]):
				print("hit the paddle")

				direction = self.ball.body.velocity.normalized()
				mod = 1 + ((random.random() - 0.5) * self.paddle_random_bounce_scale)
				direction = (direction[0], direction[1] * mod)

				self.update_ball_velocity(direction, speed)
			
			self.ball.body.velocity = self.ball.body.velocity.normalized() * (speed + self.ball_speed_increment)

	def update_ball_velocity(self, direction, speed):
		velocity = (direction[0] * speed, direction[1] * speed)
		self.ball.body.velocity = velocity

	async def update_game_state(self):
		if abs(self.ball.body.position.x) > 7 or abs(self.ball.body.position.y) > 7:
			self.reset_ball()

		game_state = {
			"type": "game_state",
			"players": self.players,
			"ball_position": {"x": self.ball.body.position.x, "y": self.ball.body.position.y},
			"left_paddle_position_y": self.paddle_left_body.position.y,
			"right_paddle_position_y": self.paddle_right_body.position.y
		}

		await self.channel_layer.group_send(self.room_id, game_state)
	
	def reset_ball(self):
		self.ball.body.position = 0, 0
		direction = (
			1 if random.random() > 0.5 else -1,
			(random.random() - 0.5) * 2
		)
		self.update_ball_velocity(direction, self.ball_speed_default)

	async def move_paddle(self, player, moved_y):
		paddle_body = self.paddle_left_body if player == self.players["left"] else self.paddle_right_body
		paddle_body.position = (paddle_body.position.x, moved_y)

	async def add_player(self, channel_name, side):
		self.players[side] = channel_name
		
		if self.players['left'] and self.players['right']:
			await self.start_game()

	async def start_game(self):
		self.reset_ball()
		asyncio.create_task(self.schedule())
		print("game has created!")

	async def schedule(self):
		while True:
			self.space.step(1/60)
			await self.update_game_state()
			await asyncio.sleep(1/60)

