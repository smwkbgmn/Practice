export default class PongRender {	
	constructor(gameId, side, socket) {
		this.join(gameId, side, socket);
		this.setUp();
		this.animate();
	}
	
	setUp() {
		this.paddleMoveDistance = 0.7;

		this.setupThreeJS();
		this.setupObject();
		this.setupInputs();
	}

	/*** WEBSOCKET ***/
	join(gameId, side, socket) {
		this.socket = socket;

		this.socket.send(JSON.stringify({
            type: 'joinRoom',
            gameId: gameId,
            side: side
        }));
        
        this.gameId = gameId; 
        this.setupSocketListeners();
        console.log("Joined room:", gameId);

        this.reverse = side == "left" ? false : true;
        console.log("Starting multiplayer as player", side);
	}

	setupSocketListeners() {
		console.log("Setting up socket listeners");
		
		this.socket.onmessage = (event) => {
			const data = JSON.parse(event.data);

			if (data.type === 'game_state') this.updateGameObjects(data);
			else if (data.type === 'gameFinish') this.stop();
		};
		
		this.socket.onclose = () => { console.log("WebSocket disconnected"); };
		this.socket.onerror = (error) => { console.log("WebSocket error:", error); };
	}
	
	updateGameObjects(lastState) {
		if (!this.reverse) {
			this.ball.position.set(
				lastState.ball_position.x,
				lastState.ball_position.y,
				0
			);
			this.paddleRight.position.set(
				this.paddleRight.position.x,
				lastState.right_paddle_position_y,
				0
			);
		} else {
			this.ball.position.set(
				-lastState.ball_position.x,
				lastState.ball_position.y,
				0
			);
			this.paddleRight.position.set(
				this.paddleRight.position.x,
				lastState.left_paddle_position_y,
				0
			);
		}
	}

	/*** SETUP ***/
	setupThreeJS() {
		this.gameScene = new THREE.Scene();
		this.gameScene.background = new THREE.Color(0x2c3e50);

		const aspect = window.innerWidth / window.innerHeight;
		const frustumSize = 10;
		this.gameCamera = new THREE.OrthographicCamera(frustumSize * aspect / -2, frustumSize * aspect / 2, frustumSize / 2, frustumSize / -2, 0.1, 1000);
		this.gameCamera.position.z = 5;

		this.gameRenderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
		this.gameRenderer.setClearColor(0x000000, 0);
		this.gameRenderer.setSize(window.innerWidth, window.innerHeight);
		this.gameRenderer.domElement.style.position = 'absolute';
		this.gameRenderer.domElement.style.top = '0px';

		document.body.appendChild(this.gameRenderer.domElement);
	}

	setupObject() {
		this.ball = this.createBall();

		this.paddleLeft = this.createPaddle(-4.5, 0);
		this.paddleRight = this.createPaddle(4.5, 0);

		this.wallTop = this.createWall(0, -5, 8, 0.1);
		this.wallBottom = this.createWall(0, 5, 8, 0.1);
	}

	setupInputs() {
		document.addEventListener('keydown', (event) => {
			switch (event.key) {
				case 'w'	: this.movePaddle(this.paddleLeft, this.paddleMoveDistance); break;
				case 's'	: this.movePaddle(this.paddleLeft, -this.paddleMoveDistance); break;
			}
		});
	}

	/*** OBJECT ***/
	createBall() {
		const ballGeometry = new THREE.CircleGeometry(0.1, 32);
		const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
		const ballMesh = new THREE.Mesh(ballGeometry, ballMaterial);
		ballMesh.position.set(0, 0, 0);

		this.gameScene.add(ballMesh);

		return ballMesh;
	}

	createPaddle(x, y) {
		const paddleGeometry = new THREE.PlaneGeometry(0.2, 1);
		const paddleMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
		const paddleMesh = new THREE.Mesh(paddleGeometry, paddleMaterial);
		paddleMesh.position.set(x, y, 0);

		this.gameScene.add(paddleMesh);

		return paddleMesh;
	}

	movePaddle(paddle, distance) {
		const newY = paddle.position.y + distance;
		if (newY > -4.5 && newY < 4.5) {
			paddle.position.set(paddle.position.x, newY, 0);
		}

		this.socket.send(JSON.stringify({
			type: 'playerMove',
			gameId: this.gameId,
			movedY: paddle.position.y
		}));
	}

	createWall(x, y, width, height) {
		const wallGeometry = new THREE.PlaneGeometry(width, height);
		const wallMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
		const wallMesh = new THREE.Mesh(wallGeometry, wallMaterial);
		wallMesh.position.set(x, y, 0);

		this.gameScene.add(wallMesh);

		return wallMesh;
	}

	/*** SHOOT ***/
	animate() {
		this.animationFrameId = requestAnimationFrame(this.animate.bind(this));
		this.gameRenderer.render(this.gameScene, this.gameCamera);
	}

	stop() { cancelAnimationFrame(this.animationFrameId); }
	resume() { this.animate(); }
	cleanUp() {
		this.stopGame();

		if (this.gameRenderer && this.gameRenderer.domElement)
			document.body.removeChild(this.gameRenderer.domElement);
		document.removeEventListener('keydown', this.handleKeyDown);

		while(this.gameScene.children.length > 0){ 
			this.gameScene.remove(this.gameScene.children[0]); 
		}
	}

	addEventWindowResize() { window.addEventListener('resize', this.handleWindowResize); }
	handleWindowResize() {
		var width = window.innerWidth,
			height = window.innerHeight;

		Render.setSize(render, width, height);
		Render.lookAt(render, Composite.allBodies(engine.world), {
			x: 50,
			y: 50
		});
	}
}
