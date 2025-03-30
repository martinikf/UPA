<script lang="ts">
	import { A, Card, Heading, P } from 'flowbite-svelte';
</script>

<main class="py-8">
	<!-- Hero Section -->
	<Card class="max-w-4xl mx-auto mb-16 p-12 shadow-xl dark:shadow-gray-800/30" size="lg">
		<div class="space-y-6">
			<Heading tag="h1" class="text-5xl font-extrabold dark:text-white mb-6">Praktický učitel prstové abecedy</Heading>
			<P class="text-xl text-gray-600 dark:text-gray-400">
				Diplomová práce: Program na&nbsp;podporu výuky prstové abecedy
			</P>
			<P class="text-lg text-gray-500 dark:text-gray-500">
				Autor: Filip Martiník
			</P>
			<P>
				<A href="/text.pdf" class="">Text diplomové práce</A>, ve&nbsp;kterém se lze dočíst jak celá webová aplikace funguje a podrobněji zjistit, jaké všechny funkcionality aplikace nabízí.
				Zdrojový kód aplikace se nachází veřejně <A href="https://github.com/martinikf/upa"> na&nbsp;GitHubu</A>.
			</P>
		</div>
	</Card>

	<!-- About Section -->
	<div class="max-w-7xl mx-auto px-4 mb-16">
		<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-12 text-center">O aplikaci</Heading>
		<div class="grid md:grid-cols-2 justify-items-center gap-8">
			<Card size="sm" class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800">
				<div class="p-6 space-y-4">
					<P class="text-gray-600 dark:text-gray-400">
						Tato aplikace slouží jako nástroj k&nbsp;podpoře učení české prstové abecedy. Nabízí různé režimy, ze&nbsp;kterých si&nbsp;můžete vybrat takový, jaký Vám bude nejvíce vyhovovat.
					</P>
				</div>
			</Card>

			<Card size="sm" class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800">
				<div class="p-6 space-y-4">
					<P class="text-gray-600 dark:text-gray-400">
						Aplikace využívá obraz vaší kamery, ale nemusíte mít strach o&nbsp;Vaše soukromí. Obraz kamery se&nbsp;zpracovává pouze v&nbsp;prohlížeči a&nbsp;není nikam odesílán.
					</P>
				</div>
			</Card>
		</div>
	</div>

	<!-- Modes Section -->
	<div class="max-w-7xl mx-auto px-4">
		<Heading tag="h2" class="text-3xl font-bold dark:text-white mb-12 text-center">Režimy</Heading>
		<div class="grid md:grid-cols-3 justify-items-center gap-8">
			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Učitel</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Systematický přístup k&nbsp;postupnému učení. Sledování postupu a&nbsp;procvičování na&nbsp;naučených znacích.
					</P>
				</div>
			</Card>

			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Konverzace</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Tohle stojí za&nbsp;to&nbsp;vyzkoušet! Povídejte si&nbsp;a&nbsp;přitom procvičujte odezírání i&nbsp;znakování.
					</P>
				</div>
			</Card>

			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Playground</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Souhrn různých režimů na&nbsp;jednom místě. Zde si&nbsp;můžete vyzkoušet co&nbsp;Vás napadne.
					</P>
				</div>
			</Card>
		</div>
	</div>
</main>