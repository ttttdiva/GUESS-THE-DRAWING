// drawer.js
function initDrawer(roomId) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    let drawing = false;
    let ws = new WebSocket(`ws://${location.host}/ws/draw/${roomId}`);

    // キャンバス背景を白に塗りつぶす（透過をなくす）
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    canvas.addEventListener("mousedown", e => {
        drawing = true;
        const {x,y} = getXY(e, canvas);
        const thickness = 5;
        ws.send(JSON.stringify({type:"startLine", x, y, color:"#000000", thickness:thickness}));
        ctx.beginPath();
        ctx.moveTo(x,y);
        ctx.lineWidth = thickness;
    });

    canvas.addEventListener("mousemove", e => {
        if(!drawing) return;
        const {x,y} = getXY(e, canvas);
        ws.send(JSON.stringify({type:"draw", x, y}));
        ctx.lineTo(x,y);
        ctx.stroke();
    });

    canvas.addEventListener("mouseup", e => {
        drawing = false;
        ws.send(JSON.stringify({type:"endLine"}));
        ctx.closePath();
    });

    document.getElementById("finishBtn").addEventListener("click", async () => {
        // 背景白塗りは既にしているので、そのままJPEGでエクスポート
        const dataUrl = canvas.toDataURL("image/jpeg", 0.9); // JPEG形式, 品質90%
        const formData = new FormData();
        formData.append("game_id", roomId);
        formData.append("img_data", dataUrl);
        let resp = await fetch("/submit_image", {method:"POST", body: formData});
        let json = await resp.json();
        alert("画像送信完了: " + json.image_url);
    });

    // リセットボタン
    document.getElementById("resetBtn").addEventListener("click", () => {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        // リセット後も白背景
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ws.send(JSON.stringify({type:"clear"}));
    });
}

function getXY(e, canvas) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}
