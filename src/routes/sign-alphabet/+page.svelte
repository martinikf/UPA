<script>
	import { Heading, Li, List, P } from 'flowbite-svelte';
</script>

<main class="m-auto max-w-4xl mx-auto p-8">
	<Heading tag="h1" class="text-4xl font-extrabold dark:text-white mb-4">Česká prstová abeceda</Heading>
	<P class="text-lg text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
		Česká prstová abeceda je vizuální komunikační systém,
		který se používá k vyjádření písmen abecedy pomocí prstů a rukou.

		Je nedílnou součástí českého znakového jazyka a slouží k vyjádření slov,
		která nemají ustálený znak, jako jsou jména, cizí slova nebo odborné termíny.
	</P>

	<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-6 border-b border-gray-200 dark:border-gray-700 pb-2">Jednoruční a dvouruční varianty</Heading>
	<P class="text-gray-600 dark:text-gray-400 mb-6">
		V české prstové abecedě existují dvě hlavní varianty:
	</P>

	<List tag="ul" list="none" class="space-y-6">
		<Li class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 shadow-sm">
			<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-2">Jednoruční prstová abeceda:</Heading>
			<P class="text-gray-600 dark:text-gray-400">
				Každé písmeno je tvořeno specifickým postavením prstů jedné ruky.
				Tato varianta je méně častá a náročnější.
			</P>
		</Li>

		<Li class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 shadow-sm">
			<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-2">Dvouruční prstová abeceda:</Heading>
			<P class="text-gray-600 dark:text-gray-400">
				Každé písmeno je tvořeno kombinací postavení prstů obou rukou.
				Tato varianta je v České republice běžnější a rozšířenější.
			</P>
		</Li>
	</List>

	<div class="mt-12">
		<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-6 border-b border-gray-200 dark:border-gray-700 pb-2">Český znakový jazyk</Heading>
		<P class="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
			Český znakový jazyk je plnohodnotný jazyk s vlastní gramatikou a slovní zásobou.
			Prstová abeceda je jeho součástí a slouží k doplnění slov, pro která neexistuje vlastní znak.
		</P>

		<Heading tag="h3" class="text-2xl font-semibold dark:text-white mb-4">Rozdíly mezi znakovými jazyky</Heading>
		<P class="text-gray-600 dark:text-gray-400">
			Znakové jazyky se mezi různými zeměmi liší.
			Stejně tak i prstové abecedy se mohou v různých zemích lišit.
			Například americká prstová abeceda se používá v USA a je odlišná od české prstové abecedy.
			Ve většině znakových jazicích je využívína prstová abeceda jednoruční a většinou sdílí podobné znaky s ostatními jazyky.
		</P>
	</div>
</main>