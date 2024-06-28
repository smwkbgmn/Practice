import * as THREE from 'three';

import Stats from 'three/addons/libs/stats.module.js';

let SCREEN_WIDTH = window.innerWidth;
let SCREEN_HEIGHT = window.innerHeight;
let aspect = SCREEN_WIDTH / SCREEN_HEIGHT;

let container, stats;
let camera, scene, renderer, mesh;
let cameraRig, activeCamera, activeHelper;
let cameraPerspective;
let cameraPerspectiveHelper;
const frustumSize = 600;

init();

function init() {

	container = document.createElement( 'div' );
	document.body.appendChild( container );

	scene = new THREE.Scene();

	//

	camera = new THREE.PerspectiveCamera( 50, 0.5 * aspect, 1, 10000 );
	camera.position.z = 2500;

	cameraPerspective = new THREE.PerspectiveCamera( 50, 0.5 * aspect, 150, 1000 );

	cameraPerspectiveHelper = new THREE.CameraHelper( cameraPerspective );
	scene.add( cameraPerspectiveHelper );

	activeCamera = cameraPerspective;
	activeHelper = cameraPerspectiveHelper;


	// counteract different front orientation of cameras vs rig

	// cameraOrtho.rotation.y = Math.PI;
	cameraPerspective.rotation.y = Math.PI;

	cameraRig = new THREE.Group();

	cameraRig.add( cameraPerspective );
	// cameraRig.add( cameraOrtho );

	scene.add( cameraRig );

	//

	mesh = new THREE.Mesh(
		new THREE.SphereGeometry( 100, 16, 8 ),
		new THREE.MeshBasicMaterial( { color: 0xffffff, wireframe: true } )
	);
	scene.add( mesh );

	const mesh2 = new THREE.Mesh(
		new THREE.SphereGeometry( 50, 16, 8 ),
		new THREE.MeshBasicMaterial( { color: 0x00ff00, wireframe: true } )
	);
	mesh2.position.y = 150;
	mesh.add( mesh2 );

	const mesh3 = new THREE.Mesh(
		new THREE.SphereGeometry( 5, 16, 8 ),
		new THREE.MeshBasicMaterial( { color: 0x0000ff, wireframe: true } )
	);
	mesh3.position.z = 150;
	cameraRig.add( mesh3 );

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );
	renderer.setAnimationLoop( animate );
	container.appendChild( renderer.domElement );

	renderer.setScissorTest( true );

	//

	stats = new Stats();
	container.appendChild( stats.dom );

	//

	window.addEventListener( 'resize', onWindowResize );
}

//

function onWindowResize() {

	SCREEN_WIDTH = window.innerWidth;
	SCREEN_HEIGHT = window.innerHeight;
	aspect = SCREEN_WIDTH / SCREEN_HEIGHT;

	renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );

	camera.aspect = 0.5 * aspect;
	camera.updateProjectionMatrix();

	cameraPerspective.aspect = 0.5 * aspect;
	cameraPerspective.updateProjectionMatrix();

}

//

function animate() {

	render();
	stats.update();

}


function render() {

	const r = Date.now() * 0.0005;

	mesh.position.x = 700 * Math.cos( r );
	mesh.position.z = 700 * Math.sin( r );
	mesh.position.y = 700 * Math.sin( r );

	mesh.children[ 0 ].position.x = 70 * Math.cos( 2 * r );
	mesh.children[ 0 ].position.z = 70 * Math.sin( r );

	cameraPerspective.fov = 35 + 30 * Math.sin( 0.5 * r );
	cameraPerspective.far = mesh.position.length();
	cameraPerspective.updateProjectionMatrix();

	cameraPerspectiveHelper.update();
	cameraPerspectiveHelper.visible = true;

	cameraRig.lookAt( mesh.position );

	//

	activeHelper.visible = false;

	renderer.setClearColor( 0x000000, 1 );
	renderer.setScissor( 0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT );
	renderer.setViewport( 0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT );
	renderer.render( scene, activeCamera );

	//

	activeHelper.visible = true;

	renderer.setClearColor( 0x111111, 1 );
	renderer.setScissor( SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT );
	renderer.setViewport( SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT );
	renderer.render( scene, camera );

}