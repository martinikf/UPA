<script>
	import { Heading, Li, List, P } from 'flowbite-svelte';
</script>

<main class="m-auto max-w-4xl mx-auto p-8">
	<Heading tag="h1" class="text-4xl font-extrabold dark:text-white mb-4">Česká prstová abeceda</Heading>
	<P class="text-lg text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
		Česká prstová abeceda je&nbsp;vizuální komunikační systém,
		který se používá k&nbsp;vyjádření písmen abecedy pomocí prstů a&nbsp;rukou.

		Je nedílnou součástí českého znakového jazyka a&nbsp;slouží k&nbsp;vyjádření slov,
		která nemají ustálený znak, jako jsou jména, cizí slova nebo odborné termíny.
	</P>

	<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-6 border-b border-gray-200 dark:border-gray-700 pb-2">Jednoruční a&nbsp;dvouruční varianty</Heading>
	<P class="text-gray-600 dark:text-gray-400 mb-6">
		V&nbsp;české prstové abecedě existují dvě hlavní varianty:
	</P>

	<List tag="ul" list="none" class="space-y-6">
		<Li class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 shadow-sm">
			<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-2">Jednoruční prstová abeceda:</Heading>
			<P class="text-gray-600 dark:text-gray-400">
				Každé písmeno je&nbsp;tvořeno specifickým postavením prstů jedné ruky.
				Tato varianta je&nbsp;méně častá a&nbsp;náročnější.
			</P>
		</Li>

		<Li class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 shadow-sm">
			<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-2">Dvouruční prstová abeceda:</Heading>
			<P class="text-gray-600 dark:text-gray-400">
				Každé písmeno je&nbsp;tvořeno kombinací postavení prstů obou rukou.
				Tato varianta je&nbsp;v&nbsp;České republice běžnější a&nbsp;rozšířenější.
			</P>
		</Li>
	</List>

	<div class="mt-12">
		<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-6 border-b border-gray-200 dark:border-gray-700 pb-2">Český znakový jazyk</Heading>
		<P class="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
			Český znakový jazyk je&nbsp;plnohodnotný jazyk s&nbsp;vlastní gramatikou a&nbsp;slovní zásobou.
			Prstová abeceda je&nbsp;jeho součástí a&nbsp;slouží k&nbsp;doplnění slov, pro která neexistuje vlastní znak.
		</P>

		<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-4">Rozdíly mezi znakovými jazyky</Heading>
		<P class="text-gray-600 dark:text-gray-400">
			Znakové jazyky se mezi různými zeměmi liší.
			Stejně tak i&nbsp;prstové abecedy se mohou v&nbsp;různých zemích lišit.
			Například americká prstová abeceda se používá v&nbsp;USA a&nbsp;je odlišná od české prstové abecedy.
			Ve většině znakových jazycích je&nbsp;využívána prstová abeceda jednoruční a&nbsp;většinou sdílí podobné znaky s&nbsp;ostatními jazyky.
		</P>
	</div>
</main>