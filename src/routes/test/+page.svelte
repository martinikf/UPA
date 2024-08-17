<script lang="ts">

	import Model from '$lib/components/models/Model.svelte';
	import { T, Canvas } from '@threlte/core'
	import { OrbitControls} from '@threlte/extras'


</script>
<div class="animation_canvas">
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

	<Model />
</Canvas>

</div>

<style>
    :global(body) {
        margin: 0;
    }

    .animation_canvas{
        width: 400px;
        height: 500px;
        position: relative;
        background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
    }

</style>



