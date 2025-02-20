<script lang="ts">
	import { A, Card, Heading, P } from 'flowbite-svelte';
</script>

<main class="min-h-screen py-8">
	<!-- Hero Section -->
	<Card class="max-w-4xl mx-auto mb-16 p-12 shadow-xl dark:shadow-gray-800/30" size="lg">
		<div class="space-y-6">
			<Heading tag="h1" class="text-5xl font-extrabold dark:text-white mb-6">Praktický učitel prstové abecedy</Heading>
			<P class="text-xl text-gray-600 dark:text-gray-400">
				Diplomová práce: Program na podporu výuky prstové abecedy
			</P>
			<P class="text-lg text-gray-500 dark:text-gray-500">
				Autor: Filip Martiník
			</P>
			<A href="https://github.com/martinikf/upa" class="">Zdrojový kód na GitHubu</A>
		</div>
	</Card>

	<!-- About Section -->
	<div class="max-w-7xl mx-auto px-4 mb-16">
		<Heading tag="h2" align="center" class="text-3xl font-bold dark:text-white mb-12">O aplikaci</Heading>
		<div class="grid md:grid-cols-2 justify-items-center gap-8">
			<Card size="sm" class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800">
				<div class="p-6 space-y-4">
					<P class="text-gray-600 dark:text-gray-400">
						Tato aplikace slouží jako nástroj k podpoře učení české prstové abecedy. Nabízí různé režimy, ze kterých si můžete vybrat takový, jaký Vám bude nejvíce vyhovovat.
					</P>
				</div>
			</Card>

			<Card size="sm" class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800">
				<div class="p-6 space-y-4">
					<P class="text-gray-600 dark:text-gray-400">
						Aplikace využívá obraz vaší kamery, ale nemusíte mít strach o Vaše soukromí. Obraz kamery se zpracovává pouze v prohlížeči a není nikam odesílán.
					</P>
				</div>
			</Card>
		</div>
	</div>

	<!-- Modes Section -->
	<div class="max-w-7xl mx-auto px-4">
		<Heading tag="h2" align="center" class="text-3xl font-bold dark:text-white mb-12">Režimy</Heading>
		<div class="grid md:grid-cols-3 justify-items-center gap-8">
			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Učitel</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Systematický přístup k postupnému učení. Sledování postupu a procvičování na naučených znacích.
					</P>
				</div>
			</Card>

			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Konverzace</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Tohle stojí za to vyzkoušet! Povídejte si a přitom procvičujte jak odezírání tak znakování.
					</P>
				</div>
			</Card>

			<Card class="hover:shadow-lg transition-shadow duration-200 dark:bg-gray-800" size="xs">
				<div class="p-6 space-y-4">
					<Heading tag="h3" class="text-xl font-semibold dark:text-white">Playground</Heading>
					<P class="text-gray-600 dark:text-gray-400">
						Souhrn různých režimů na jednom místě. Zde si můžete vyzkoušet co Vás napadne.
					</P>
				</div>
			</Card>
		</div>
	</div>
</main>