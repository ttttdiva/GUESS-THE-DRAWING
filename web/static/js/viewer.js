// viewer.js
function initViewer(roomId) {
    const canvas = document.getElementById("viewCanvas");
    const ctx = canvas.getContext("2d");
    let drawing = false;

    let ws = new WebSocket(`ws://${location.host}/ws/view/${roomId}`);
    ws.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        if(msg.type === "startLine"){
            ctx.beginPath();
            ctx.moveTo(msg.x, msg.y);
            ctx.strokeStyle = msg.color;
            ctx.lineWidth = msg.thickness;
            drawing = true;
        } else if(msg.type === "draw"){
            if(drawing){
                ctx.lineTo(msg.x,msg.y);
                ctx.stroke();
            }
        } else if(msg.type === "endLine"){
            ctx.closePath();
            drawing = false;
        } else if(msg.type === "clear"){
            // クリア
            ctx.clearRect(0,0,canvas.width,canvas.height);
        }
    };
}
