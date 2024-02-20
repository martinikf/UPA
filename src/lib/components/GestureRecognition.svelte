<script>
    // https://codepen.io/mediapipe-preview/details/zYamdVd
    import { GestureRecognizer, FilesetResolver, DrawingUtils } from "@mediapipe/tasks-vision";
    import { browser } from '$app/environment';

    if(browser){
        const demosSection = document.getElementById("demos");
        let gestureRecognizer;
        let runningMode = "VIDEO";
        let enableWebcamButton;
        let webcamRunning = false;
        const videoHeight = "360px";
        const videoWidth = "480px";

        // Before we can use HandLandmarker class we must wait for it to finish
        // loading. Machine Learning models can be large and take a moment to
        // get everything needed to run.
        const createGestureRecognizer = async () => {
            const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm");
            gestureRecognizer = await GestureRecognizer.createFromOptions(vision, {
                baseOptions: {
                    modelAssetPath: "models/gesture_recognizer.task",
                    delegate: "GPU"
                },
                runningMode: runningMode
            });
            demosSection.classList.remove("invisible");
        };

        createGestureRecognizer();

        /********************************************************************
        // Demo 2: Continuously grab image from webcam stream and detect it.
        ********************************************************************/

        const video = document.getElementById("webcam");
        const canvasElement = document.getElementById("output_canvas");
        const canvasCtx = canvasElement.getContext("2d");
        const gestureOutput = document.getElementById("gesture_output");

        // Check if webcam access is supported.
        function hasGetUserMedia() {
            return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
        }

        // If webcam supported, add event listener to button for when user
        // wants to activate it.
        if (hasGetUserMedia()) {
            enableWebcamButton = document.getElementById("webcamButton");
            enableWebcamButton.addEventListener("click", enableCam);
        }
        else {
            console.warn("getUserMedia() is not supported by your browser");
        }

        // Enable the live webcam view and start detection.
        function enableCam(event) {
            if (!gestureRecognizer) {
                alert("Please wait for gestureRecognizer to load");
                return;
            }
            webcamRunning = true;

            // getUsermedia parameters.
            const constraints = {
                video: true
            };
            // Activate the webcam stream.
            navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
                video.srcObject = stream;
                video.addEventListener("loadeddata", predictWebcam);
            });
        }

        let lastVideoTime = -1;
        let results = undefined;

        async function predictWebcam() {
            const webcamElement = document.getElementById("webcam");
            
            let nowInMs = Date.now();
            if (video.currentTime !== lastVideoTime) {
                lastVideoTime = video.currentTime;
                results = gestureRecognizer.recognizeForVideo(video, nowInMs);
            }
            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            const drawingUtils = new DrawingUtils(canvasCtx);
            
            canvasElement.style.height = videoHeight;
            webcamElement.style.height = videoHeight;
            canvasElement.style.width = videoWidth;
            webcamElement.style.width = videoWidth;
            
            if (results.landmarks) {
                for (const landmarks of results.landmarks) {
                    drawingUtils.drawConnectors(landmarks, GestureRecognizer.HAND_CONNECTIONS, {
                        color: "#00FF00",
                        lineWidth: 5
                    });
                    drawingUtils.drawLandmarks(landmarks, {
                        color: "#FF0000",
                        lineWidth: 2
                    });
                }
            }
            canvasCtx.restore();

            if (results.gestures.length > 0) {
                gestureOutput.style.display = "block";
                gestureOutput.style.width = videoWidth;
                
                const categoryName = results.gestures[0][0].categoryName;
                const categoryScore = parseFloat(results.gestures[0][0].score * 100).toFixed(2);
                const handedness = results.handednesses[0][0].displayName;

                gestureOutput.innerText = `GestureRecognizer: ${categoryName}\n Confidence: ${categoryScore} %\n Handedness: ${handedness}`;
            }
            else {
                gestureOutput.style.display = "none";
            }
            // Call this function again to keep predicting when the browser is ready.
            if (webcamRunning === true) {
                window.requestAnimationFrame(predictWebcam);
            }
    }
}
</script>


<section id="demos" class="invisible">

  <h2>Demo: Webcam continuous hand gesture detection</h2>

  <div id="liveView" class="videoView">
    <button id="webcamButton" class="mdc-button mdc-button--raised">
      <span class="mdc-button__ripple"></span>
      <span class="mdc-button__label">ENABLE WEBCAM</span>
    </button>

    <div class ="">
        
        <div id="webcamDiv" style="position: relative;">
            <video id="webcam" autoplay playsinline> <track kind="captions"> </video>
            <canvas class="output_canvas" id="output_canvas" width="1280" height="720" style="position: absolute; left: 0px; top: 0px;"></canvas>
        </div>
          
          <p id='gesture_output' class="output"></p>
    </div>

  </div>
</section>



<style>
   #webcamDiv{
    -webkit-transform: scaleX(-1);
    transform: scaleX(-1);

    width: 480px;
    height: 360px;
   }

</style>