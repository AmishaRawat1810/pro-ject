import Phaser from 'phaser';

const gameState = {};

function preload() {
  this.load.image('codey', 'https://content.codecademy.com/courses/learn-phaser/codey.png');
  this.load.image('bg', "../assets/flappyBirdBg.png");
  this.load.image('pillar', "../assets/cavePillar.png"); 
  
  // Load the new ground asset
  this.load.image('ground', "../assets/ground.png");
}

function create() {
  const w = this.scale.gameSize.width;
  const h = this.scale.gameSize.height;

  // Active state to prevent flapping/scrolling after crashing
  gameState.active = true;

  // 1. Static Background
  gameState.bg = this.add.image(0, 0, 'bg').setOrigin(0).setDisplaySize(w, h);

  // 2. Scrolling Ground with Physics
  // We use a tileSprite for the scrolling visual effect, and add a static physics body to it
  gameState.ground = this.add.tileSprite(0, h - 50, w, 50, 'ground').setOrigin(0);
  this.physics.add.existing(gameState.ground, true); // 'true' sets it as a static body unaffected by gravity

  // 3. Player Setup
  gameState.cody = this.physics.add.sprite(200, 200, 'codey');
  gameState.cody.setCollideWorldBounds(true); // Prevents flying off the top of the screen

  // 4. Input Handling
  const flap = () => {
    // Only allow flapping if the game hasn't ended
    if (gameState.active) {
      gameState.cody.setVelocityY(-350);
    }
  };
  this.input.keyboard.on('keydown-SPACE', flap);
  this.input.keyboard.on('keydown-UP', flap);
  this.input.on('pointerdown', flap);

  // 5. Scoring Setup & Canvas UI
  gameState.score = 0;
  gameState.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#000' });
  
  // Game Over Text (Hidden by default)
  gameState.gameOverText = this.add.text(w / 2, h / 2 - 50, 'GAME OVER', { fontSize: '64px', fill: '#000' }).setOrigin(0.5).setVisible(false);
  gameState.restartText = this.add.text(w / 2, h / 2 + 50, 'Click to Restart', { fontSize: '32px', fill: '#000' }).setOrigin(0.5).setVisible(false);

  // 6. Physics Groups
  gameState.pipes = this.physics.add.group();
  gameState.scoreZones = this.physics.add.group();

  const spawnPipes = () => {
    const gapPosition = Phaser.Math.Between(150, h - 200); // Adjusted so gaps don't spawn below the ground
    const gapSize = 150;

    const bottomPipe = gameState.pipes.create(w, gapPosition + (gapSize / 2), 'pillar').setOrigin(0, 0);
    const topPipe = gameState.pipes.create(w, gapPosition - (gapSize / 2), 'pillar').setOrigin(0, 1);
    topPipe.flipY = true;

    const scoreZone = gameState.scoreZones.create(w + 30, gapPosition, 'pillar');
    scoreZone.setVisible(false);
    scoreZone.setDisplaySize(10, gapSize);

    gameState.pipes.getChildren().forEach(pipe => {
      pipe.body.allowGravity = false;
      pipe.setVelocityX(-200);
    });
    
    gameState.scoreZones.getChildren().forEach(zone => {
      zone.body.allowGravity = false;
      zone.setVelocityX(-200);
    });
  };

  // 7. Spawn Timer
  gameState.pipeLoop = this.time.addEvent({
    delay: 1500,
    callback: spawnPipes,
    callbackScope: this,
    loop: true
  });

  // 8. Universal Crash Logic
  const hitObstacle = () => {
    if (!gameState.active) return; // Prevent multiple triggers if hitting ground and pipe simultaneously
    
    gameState.active = false;
    this.physics.pause();
    gameState.pipeLoop.destroy();
    
    // Show Canvas UI
    gameState.gameOverText.setVisible(true);
    gameState.restartText.setVisible(true);
    
    // --- React EventBus Bridge ---
    // In your Candy Crush architecture, you will remove the text rendering above and emit an event to React:
    // EventBus.emit('game-over', { finalScore: gameState.score });
    // -----------------------------

    // Restart the scene on click or spacebar
    this.input.once('pointerup', () => {
      this.scene.restart();
    });
    this.input.keyboard.once('keydown-SPACE', () => {
      this.scene.restart();
    });
  };

  // Crash triggers for both pipes and the ground
  this.physics.add.collider(gameState.cody, gameState.pipes, hitObstacle);
  this.physics.add.collider(gameState.cody, gameState.ground, hitObstacle);

  // 9. Overlap (Scoring)
  this.physics.add.overlap(gameState.cody, gameState.scoreZones, (bird, zone) => {
    if (gameState.active) {
        gameState.score += 1;
        gameState.scoreText.setText(`Score: ${gameState.score}`);
        
        // --- React EventBus Bridge ---
        // Synchronize the server/React state in your final build:
        // EventBus.emit('score-update', gameState.score);
        // -----------------------------
    }
    zone.destroy(); 
  });
}

function update() {
  // Only scroll the ground if the game is actively playing
  if (gameState.active) {
    gameState.ground.tilePositionX += 2;
  }

  // Clean up off-screen objects
  gameState.pipes.getChildren().forEach(pipe => {
    if (pipe.x < -pipe.width) {
      pipe.destroy();
    }
  });

  gameState.scoreZones.getChildren().forEach(zone => {
    if (zone.x < -zone.width) {
      zone.destroy();
    }
  });
}

const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 800 },
      debug: false 
    }
  },
  scene: { preload, create, update }
}

new Phaser.Game(config);