<script lang="ts">
    // based on: https://codepen.io/mediapipe-preview/pen/gOKBGPN
    import { HandLandmarker, FilesetResolver, GestureRecognizer,  DrawingUtils, type HandLandmarkerResult} from "@mediapipe/tasks-vision";

    import { browser } from '$app/environment';

    if(browser){

        let handLandmarker : HandLandmarker | undefined;
        let runningMode = "VIDEO";
        let enableWebcamButton: HTMLButtonElement;
        let webcamRunning: Boolean = false;
        const videoHeight = "360px";
        const videoWidth = "480px";
        let tfliteModel : any;

        const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ch']

        // Before we can use HandLandmarker class we must wait for it to finish
        // loading. Machine Learning models can be large and take a moment to
        // get everything needed to run.
        const createHandLandmarker = async () => {
            const vision = await FilesetResolver.forVisionTasks(
                "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
            );
            handLandmarker = await HandLandmarker.createFromOptions(vision, {
                baseOptions: {
                modelAssetPath: `models/hand_landmarker.task`,
                delegate: "GPU"
                },
                runningMode: runningMode,
                numHands: 1
            });
            enableCam();
        };

        async function loadGestureModel(){
            tflite.setWasmPath(
                'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.8/dist/'
            );
            tfliteModel = await tflite.loadTFLiteModel('models/keypoint_classifier.tflite');  
        }

        createHandLandmarker();

        const video = document.getElementById("webcam") as HTMLVideoElement;
        const canvasElement = document.getElementById("output_canvas") as HTMLCanvasElement;
        const canvasCtx = canvasElement.getContext("2d");

        // Check if webcam access is supported.
        const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

        // If webcam supported, add event listener to button for when user
        // wants to activate it.
        if (!hasGetUserMedia()) {
            console.warn("getUserMedia() is not supported by your browser");
        }

        // Enable the live webcam view and start detection.
        function enableCam() {
            webcamRunning = true;
            if (!handLandmarker) {
                console.log("Wait! objectDetector not loaded yet.");
                return;
            }

            // getUsermedia parameters.
            const constraints = {
                video: true
            };

            // Activate the webcam stream.
            navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
                video.srcObject = stream;
                video.addEventListener("loadeddata", predictWebcam);
            });
        }

        let lastVideoTime = -1;
        let results : HandLandmarkerResult | undefined;

        async function predictWebcam() {
            const webcamElement = document.getElementById("webcam");

            if(canvasCtx === null || handLandmarker === undefined || video === null || webcamElement === null){
                return;
            }

            let startTimeMs = performance.now();
            if (lastVideoTime !== video.currentTime) {
                lastVideoTime = video.currentTime;
                results = handLandmarker.detectForVideo(video, startTimeMs);
            }


            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

            const drawingUtils = new DrawingUtils(canvasCtx);

            if (results && results.landmarks && results.landmarks.length > 0) {
                // draw landmarks and connections
                drawLandmarks(drawingUtils, results);
                // draw bounding box
                drawBoundingBox(drawingUtils, results.landmarks[0]);

                const abosluteLandmarks = calculateLandmarksAbsolutePositions(results.landmarks[0], video.videoWidth, video.videoHeight);
                
                //Convert landmarks to relative normalized coordtinates
                const relativeLandmarks = calculateRelativeLandmarks(abosluteLandmarks);
        
                //Run ML model, get for each gesture its probability
                const probabilities = await handGestureClassifier(relativeLandmarks);

                for(let i = 0; i < probabilities.length; i++){
                    if(probabilities[i] > 0.25){
                        console.log("Gesture " + letters[i] + " has probability " + probabilities[i]);
                    }
                }                  
            }
            canvasCtx.restore();

            // Call this function again to keep predicting when the browser is ready.
            if (webcamRunning === true) {
                window.requestAnimationFrame(predictWebcam);
            }
        }
    

    function drawLandmarks(drawingUtils : DrawingUtils, results : any){
        for (const landmark of results.landmarks) {
            drawingUtils.drawConnectors(landmark, GestureRecognizer.HAND_CONNECTIONS, {
            color: "#00FF00",
            lineWidth: 5
            });
            drawingUtils.drawLandmarks(landmark, { 
                color: "#0000FF", 
                lineWidth: 2
            });
        }       
    }

    function drawBoundingBox(drawingUtils : DrawingUtils, landmarks : any) : void{
        //TODO idk how to create bounding box for param
    }

    // https://github.com/kinivi/hand-gesture-recognition-mediapipe
    function calculateLandmarksAbsolutePositions(landmarks : any, imageWidth : number, imageHeight : number) : any {
        let newLandmarks = [];

        for (const landmark of landmarks){
            let x = Math.min( Math.floor(landmark.x * imageWidth), imageWidth - 1);
            let y = Math.min( Math.floor(landmark.y * imageHeight), imageHeight - 1);
            //let z = landmark.z;
            newLandmarks.push({x: x, y: y});
        }

        return newLandmarks;
    }

    function calculateRelativeLandmarks(landmarks : any) : any{        
        const tempLandmarkList = structuredClone(landmarks);
        
        let baseX: number = 0;
        let baseY: number = 0;

        for (let index = 0; index < tempLandmarkList.length; index++) {
            const landmarkPoint = tempLandmarkList[index];

            if (index === 0) {
                baseX = landmarkPoint.x;
                baseY = landmarkPoint.y;
            }

            tempLandmarkList[index].x = tempLandmarkList[index].x - baseX;
            tempLandmarkList[index].y = tempLandmarkList[index].y - baseY;
        }

        
        // Convert to a one-dimensional list
        let flattenedLandmarkList = [];
        for (let index = 0; index < tempLandmarkList.length; index++) {
            flattenedLandmarkList.push(tempLandmarkList[index].x);
            flattenedLandmarkList.push(tempLandmarkList[index].y);
        }

        // Normalization
        const absValues = flattenedLandmarkList.map(Math.abs);
        const maxValue: number = Math.max(...absValues);

        const normalizedLandmarkList: number[] = flattenedLandmarkList.map((val) => val / maxValue);
        return normalizedLandmarkList;
    }

    async function handGestureClassifier(landmarks : any){

        if(tfliteModel === undefined){
            await loadGestureModel();
        }

        const input = tf.tensor(landmarks, [1, 42]);
        const output = tfliteModel.predict(input);

        const result = await output.dataSync();
        return result;
    }
}
</script>

<svelte:head>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-core"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-cpu"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite/dist/tf-tflite.min.js"></script>
</svelte:head>


<div id="webcamDiv">
    <video id="webcam" autoplay playsinline><track kind="captions"></video>
    <canvas class="output_canvas" id="output_canvas" width="1920" height="1080"></canvas>
</div>

<style>
    #webcamDiv{
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1);
        width: 480px;
        height: 360px;
        position: relative;
    }

    #webcam{
        width: 480px;
        height: 360px;
    }

    #output_canvas{
        width: 480px;
        height: 360px;
        position: absolute;
        left: 0px;
        top: 0px;
    }
</style>