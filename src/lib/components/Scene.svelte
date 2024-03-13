<!-- Scene -->
<script lang="ts">

  import { T, Canvas } from '@threlte/core'
  import { OrbitControls } from '@threlte/extras'

  import Model from './AnimatedModel.svelte'

  export let model : Model;
  export let showLetter = true;

  let letterDisplay = "";

</script>

<Canvas>
  <T.PerspectiveCamera
    makeDefault
    position={[0, 0, 0.8]}
    fov={60}
  >
    <OrbitControls
      autoRotate={false}
      enableZoom={true}
      enableDamping={false}
    />
  </T.PerspectiveCamera>

  <T.DirectionalLight
    intensity={0.8}
    position.x={1}
    position.y={1}
  />

  <T.AmbientLight intensity={1} />

  <Model bind:this={model} bind:letterDisplay={letterDisplay}  />

</Canvas>

{#if showLetter && model}
  <div class="text" id="text">{letterDisplay}</div>
{/if}

<style>
  .text{
    position: absolute;
    top: 5%;
    left: 80%;
    font-size: 48px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
  }
</style>
