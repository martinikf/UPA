<script>
	import '../app.css';
	import { DarkMode, Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
	import { page } from '$app/stores';

	$: activeUrl = $page.url.pathname;
	let activeClass = 'text-orange-600 dark:text-orange-400 font-semibold border-b-2 border-orange-600 dark:border-orange-400';
	let nonActiveClass = 'text-gray-700 hover:text-orange-600 dark:text-gray-300 dark:hover:text-orange-400 transition-colors duration-200';
</script>

<header class="top-0 z-50">
	<Navbar
		fluid={true}
		class="backdrop-blur-sm border-b border-gray-200 dark:border-gray-700"
	>
		<NavBrand class="flex items-center space-x-3 rtl:space-x-reverse">
			<span class="self-center text-3xl font-bold whitespace-nowrap dark:text-white gradient-text">
				PUPA
			</span>
		</NavBrand>

		<div class="flex md:order-2 gap-2">
			<DarkMode class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" />
			<NavHamburger class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" />
		</div>

		<NavUl
			{activeUrl}
			{activeClass}
			{nonActiveClass}
			class="md:bg-transparent p-4 md:p-0 mt-4 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0"
		>
			<NavLi href="/" class="py-2 px-3 md:p-0 text-lg">Úvod</NavLi>
			<NavLi href="/sign-alphabet" class="py-2 px-3 md:p-0 text-lg">Prstová abeceda</NavLi>
			<NavLi href="/learn" class="py-2 px-3 md:p-0 text-lg">Učitel</NavLi>
			<NavLi href="/conversation" class="py-2 px-3 md:p-0 text-lg">Konverzace</NavLi>
			<NavLi href="/playground" class="py-2 px-3 md:p-0 text-lg">Playground</NavLi>
		</NavUl>
	</Navbar>
</header>

<slot class="min-h-[calc(100vh-4rem)] max-w-screen-2xl m-auto" />

<style>
  .gradient-text {
    background: linear-gradient(to bottom, #0057b7 50%, orange 50%);
    background-clip: text;
    color: transparent;
  }
</style>