const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');
const PIXEL_SIZE = 1; // Each pixel represents 1mm

let isDrawing = false;
let allStrokes = [];
let currentStroke = [];


canvas.addEventListener('mousedown', (event) => {
    isDrawing = true;
    currentStroke = [];
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / PIXEL_SIZE);
    const y = Math.floor((event.clientY - rect.top) / PIXEL_SIZE);
    currentStroke.push({ x, y });
});

canvas.addEventListener('mousemove', (event) => {
    if (!isDrawing) return;
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / PIXEL_SIZE);
    const y = Math.floor((event.clientY - rect.top) / PIXEL_SIZE);
    if (!currentStroke.some(point => point.x === x && point.y === y)) {
        currentStroke.push({ x, y });
    }
    
    drawStroke(currentStroke);
});

canvas.addEventListener('mouseup', () => {
    isDrawing = false;
    if (currentStroke.length > 0) {
        allStrokes.push(currentStroke); // Call the function to send the stroke to the server
    }
});

function drawStroke(stroke) {
    if (stroke.length < 2) return;
    context.strokeStyle = '#000';
    context.lineWidth = PIXEL_SIZE;
    context.lineJoin = 'round';
    context.lineCap = 'round';

    context.beginPath();
    context.moveTo(stroke[0].x * PIXEL_SIZE, stroke[0].y * PIXEL_SIZE);
    
    for (let i = 1; i < stroke.length; i++) {
        context.lineTo(stroke[i].x * PIXEL_SIZE, stroke[i].y * PIXEL_SIZE);
    }
    
    context.stroke();
    context.closePath();
}

function sendStrokeToServer() {
        fetch('/print_strokes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(allStrokes),
        })
            .then((response) => {
                if (!response.ok) {
                    console.error('Failed to send stroke to server');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

function clearStroke() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    allStrokes.length = 0

    fetch('/clear_strokes', {
            method: 'POST'
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to clear stroke');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

clearStroke()


const startButton2 = document.getElementById('startButton2');
startButton2.addEventListener('click', sendStrokeToServer);

const clearButton = document.getElementById('trash-icon');
clearButton.addEventListener('click', clearStroke)