// drawer.js
function initDrawer(roomId) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    let drawing = false;
    let ws = new WebSocket(`ws://${location.host}/ws/draw/${roomId}`);

    let currentColor = "#000000";
    let isEraser = false;
    let thickness = 5; // デフォルトの太さ

    // 背景を白で初期化
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // ペンモードへの切り替え
    function setPenMode() {
        isEraser = false;
        ctx.globalCompositeOperation = 'source-over';
        currentColor = document.getElementById("colorPicker").value;
        ctx.strokeStyle = currentColor;
        document.getElementById("eraserBtn").textContent = "消しゴム";
    }

    // 消しゴムモードへの切り替え
    function setEraserMode() {
        isEraser = true;
        ctx.globalCompositeOperation = 'destination-out';
        // 消しゴム時は色指定は必要ないが一応指定
        ctx.strokeStyle = 'rgba(0,0,0,1)';
        document.getElementById("eraserBtn").textContent = "ペンに戻す";
    }

    // 描画開始
    function startDrawing(x, y) {
        drawing = true;

        // 現在のモードに応じて設定
        if (isEraser) {
            ctx.globalCompositeOperation = 'destination-out';
            ctx.strokeStyle = 'rgba(0,0,0,1)';
        } else {
            ctx.globalCompositeOperation = 'source-over';
            ctx.strokeStyle = currentColor;
        }

        ctx.lineWidth = thickness;
        ctx.beginPath();
        ctx.moveTo(x, y);

        ws.send(JSON.stringify({
            type: "startLine",
            x,
            y,
            color: isEraser ? "#ffffff" : currentColor,
            thickness: thickness,
            eraser: isEraser
        }));
    }

    // 描画中
    function draw(x, y) {
        if (!drawing) return;
        ws.send(JSON.stringify({type:"draw", x, y}));
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    // 描画終了
    function stopDrawing() {
        if (!drawing) return;
        drawing = false;
        ws.send(JSON.stringify({type:"endLine"}));
        ctx.closePath();
    }

    // マウスイベント
    canvas.addEventListener("mousedown", e => {
        const {x, y} = getXY(e, canvas);
        startDrawing(x, y);
    });

    canvas.addEventListener("mousemove", e => {
        const {x, y} = getXY(e, canvas);
        draw(x, y);
    });

    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);

    // タッチイベント
    canvas.addEventListener("touchstart", e => {
        e.preventDefault();
        const {x, y} = getXY(e.touches[0], canvas);
        startDrawing(x, y);
    });

    canvas.addEventListener("touchmove", e => {
        e.preventDefault();
        const {x, y} = getXY(e.touches[0], canvas);
        draw(x, y);
    });

    canvas.addEventListener("touchend", e => {
        e.preventDefault();
        stopDrawing();
    });

    // 画像送信
    document.getElementById("finishBtn").addEventListener("click", async () => {
        // 一旦、オフスクリーンキャンバスを作る
        const offCanvas = document.createElement('canvas');
        offCanvas.width = canvas.width;
        offCanvas.height = canvas.height;
        const offCtx = offCanvas.getContext('2d');
    
        // 背景を白で塗りつぶし
        offCtx.fillStyle = "#ffffff";
        offCtx.fillRect(0, 0, offCanvas.width, offCanvas.height);
    
        // 元のキャンバスを上から描画
        offCtx.drawImage(canvas, 0, 0);
    
        // これで透明部分は白背景となったので、JPEGで取得
        const dataUrl = offCanvas.toDataURL("image/jpeg", 0.9);
    
        const formData = new FormData();
        formData.append("game_id", roomId);
        formData.append("img_data", dataUrl);
        let resp = await fetch("/submit_image", {method:"POST", body: formData});
        let json = await resp.json();
        alert("画像送信完了: " + json.image_url);
    });

    // リセット
    document.getElementById("resetBtn").addEventListener("click", () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ws.send(JSON.stringify({type:"clear"}));
    });

    // カラーピッカー
    const colorPicker = document.getElementById("colorPicker");
    colorPicker.addEventListener("change", () => {
        setPenMode();
    });

    // 消しゴムボタン
    const eraserBtn = document.getElementById("eraserBtn");
    eraserBtn.addEventListener("click", () => {
        if (isEraser) {
            setPenMode();
        } else {
            setEraserMode();
        }
    });

    // ペン太さスライダー
    const thicknessSlider = document.getElementById("thicknessSlider");
    thicknessSlider.addEventListener("input", () => {
        thickness = parseInt(thicknessSlider.value, 10);
        // ペンの太さ変更後、もしペンモードならstrokeStyleを更新（不要だが保険）
        if (!isEraser) {
            ctx.strokeStyle = currentColor;
        }
    });

    // 初期はペンモード
    setPenMode();
}

function getXY(e, canvas) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}
