<script lang="ts">
	import { page } from '$app/stores';
</script>

<div style="margin: auto; width: 50vw; text-align: center; margin-top: 1rem;">
	<p>
		V aplikaci došlo k následující chybě: {$page?.status} - {$page?.error?.message}.
	</p>
	<p>
		Zkuste stránku obnovit nebo přejít <a style="font-weight: bold" href="/">na hlavní stránku aplikace</a>.
	</p>
	<p>
		Pokud pořád narazíte na problém, navštivte aplikaci později a případně kontaktuje autora.
	</p>
</div>

