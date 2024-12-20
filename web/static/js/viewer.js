// viewer.js
function initViewer(roomId) {
    const canvas = document.getElementById("viewCanvas");
    const ctx = canvas.getContext("2d");
    let drawing = false;

    const ws = new WebSocket(`ws://${location.host}/ws/view/${roomId}`);
    ws.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.type === "startLine") {
            ctx.beginPath();
            ctx.moveTo(msg.x, msg.y);
            ctx.lineWidth = msg.thickness;
            
            if (msg.eraser) {
                // 消しゴムモード
                ctx.globalCompositeOperation = 'destination-out';
                // 消しゴム時はstrokeStyleは黒など何でもよいが、半透明黒で問題ない
                ctx.strokeStyle = 'rgba(0,0,0,1)';
            } else {
                // 通常ペンモード
                ctx.globalCompositeOperation = 'source-over';
                ctx.strokeStyle = msg.color;
            }

            drawing = true;

        } else if (msg.type === "draw") {
            if (drawing) {
                ctx.lineTo(msg.x, msg.y);
                ctx.stroke();
            }
        } else if (msg.type === "endLine") {
            if (drawing) {
                ctx.closePath();
                drawing = false;
            }
        } else if (msg.type === "clear") {
            // クリア
            ctx.clearRect(0,0,canvas.width,canvas.height);
            // クリア後は背景を白で再塗りつぶし（もし必要なら）
            ctx.globalCompositeOperation = 'source-over';
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0,0,canvas.width,canvas.height);
        }
    };
}
