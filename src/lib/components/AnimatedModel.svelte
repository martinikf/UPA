<!-- Human model with animations -->
<script lang="ts">
  import { T } from '@threlte/core'
  import {  GLTF, useGltf, useGltfAnimations, Text } from '@threlte/extras'

  const actionOffset = "ActionLetter";
  const gltf = useGltf('models/ModelTextures.glb', {
    useDraco: true
  })

  const { actions, mixer } = useGltfAnimations(gltf)

  export let isPaused : boolean = false;
  export let letterDisplay : string = "-"; //Letter in string for display purposes

  let text = "";  //Text to be animated
  let currentChar = ''; 
  let previousChar = '';

  let speed = 1;
  let delayOnNewWord = 0;
  let delayOnNewLetter = 0;
  let transitionSpeed = 0;
  changeSpeed(speed); 

  let currentActionKey = 'ActionRest' //Default action = rest

  const dict: { [key: string]: string } = {
    "Á": "Ad",
    "É": "Ed",
    "Í": "Id",
    "Ó": "Od",
    "Ú": "Ud",
    "Ů": "Ud", // Missing animation for "Ů" so use "Ú" instead
    "Ý": "Yd",
    "Č": "Cc",
    "Ď" : "Dc",
    "Ě": "Ec",
    "Ň": "Nc",
    "Ř": "Rc",
    "Š": "Sc",
    "Ť": "Tc",
    "Ž": "Zc"
  }

  $: $actions[currentActionKey]?.play() //Play rest action as default

  function normalizeActionKey(letter : string, double : boolean) : string{
    let charToReturn : string = letter;
    if (letter in dict){
      return dict[letter]; //Dont return doubled special letter -> no animations for them
    }

    if(double){
      return charToReturn + charToReturn
    }

    return charToReturn;
  }

  function transitionTo (nextActionKey: string, duration = 1){
    console.log("transitionTo", nextActionKey)
    const currentAction = $actions[currentActionKey]
    const nextAction = $actions[nextActionKey]

    if(nextAction != null && nextActionKey.includes("Letter")){
      nextAction.setLoop(2200, 1); // 2200 - LoopOnce
      nextAction.clampWhenFinished = true;
      nextAction.reset();
    }
    
    if (!nextAction || currentAction === nextAction) {
      return;
    }

    // Function inspired by: https://github.com/mrdoob/three.js/blob/master/examples/webgl_animation_skinning_blending.html
    nextAction.enabled = true
    if (currentAction) {
      currentAction.crossFadeTo(nextAction, duration, true)
    }
    
    currentActionKey = nextActionKey
  }

  mixer.addEventListener("finished", () => {
    if(currentActionKey.includes("Letter")){
        setTimeout(() => {
          playAnimationRec()
        }, delayOnNewLetter);
    }
  })

  function playAnimationRec(){  
    if(text.length == 0) {
      //End of animation
      letterDisplay = "-";
      transitionTo("ActionRest", 1)
      return;
    }

    if(currentChar.toLowerCase() != currentChar.toUpperCase()){
      previousChar = currentChar; //Change previous char only if the current previous is letter
    }

    currentChar = text.charAt(0);

    //Special case for letter "CH"
    if(currentChar == 'C' && text.length > 1 && text.charAt(1) == "H")
    {
      currentChar = "Ch";
      text = text.substring(1);
    }

    text = text.substring(1);

    if(currentChar.toLowerCase() != currentChar.toUpperCase()){
      // if char is letter
      letterDisplay = currentChar;
      transitionTo(actionOffset + normalizeActionKey(currentChar, currentChar === previousChar), transitionSpeed);
    }
    else{
        //delay on new word
        return setTimeout(() => {
          playAnimationRec()
        }, delayOnNewWord);
      }

  }

  export function playAnimationForText(textArg : string){
    text = textArg.toUpperCase();
    currentChar = '';
    previousChar = '';

    playAnimationRec();
  }

  // sets delay based on speed
  export function changeSpeed(newSpeed : number){
    speed = newSpeed;
    console.log("Speed changed to: ", speed);

    mixer.timeScale = speed; 
    delayOnNewLetter = 300 / speed;
    delayOnNewWord = 1000 / speed;
    transitionSpeed = Math.min(1, Math.pow(speed, -1))
    
    console.log("mixer.timeScale: ", mixer.timeScale);
    console.log("Delay on new letter: ", delayOnNewLetter);
    console.log("Delay on new word: ", delayOnNewWord);
    console.log("Transition speed: ", transitionSpeed);
  }

  export function resetAnimation(){
    transitionTo('ActionRest', 0.5);
    currentChar = '';
    previousChar = '';
    text = '';
    letterDisplay = '-';
  }

  export function pauseAnimation(){
    mixer.timeScale = 0;
    isPaused = true;
  }

  export function resumeAnimation(){
    mixer.timeScale = speed;
    isPaused = false;
  }

  export function pauseResumeAnimation(){
      if(isPaused){
        resumeAnimation();
      }
      else{
        pauseAnimation();
      }
  }
</script>

<svelte:options accessors/>

{#if $gltf}
  <T is={$gltf.scene} 
  position = {[0, -1.5, 0]}
  />
{/if}

{#if !$gltf}
  <Text text="Načítání"
    position = {[-0.2, 0, 0]}
  />
{/if}