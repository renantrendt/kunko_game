const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

function preload() {
    // Não precisamos carregar imagens
}

function create() {
    // Desenhar o corpo do pato
    this.quack = this.add.rectangle(400, 300, 100, 50, 0xffff00); // Corpo amarelo

    // Desenhar a cabeça do pato
    this.head = this.add.circle(400, 270, 25, 0xffff00); // Cabeça amarela

    // Desenhar os olhos do pato
    this.eyeLeft = this.add.circle(390, 265, 5, 0x000000); // Olho esquerdo
    this.eyeRight = this.add.circle(410, 265, 5, 0x000000); // Olho direito

    // Desenhar o bico do pato
    this.beak = this.add.triangle({
        x: 400,
        y: 280,
        points: [0, 0, -15, 10, 15, 10],
        fillColor: 0xffa500, // Laranja
        angle: 0
    });
}

function update() {
    // Não precisamos de lógica de movimento por enquanto
}
