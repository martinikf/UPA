<header>
	<div class="headerContent">
		<h1 class="logo">UPA</h1>
		<nav>
			<ul>
				<li><a href="/">Hlavní stránka</a></li>
				<li><a href="/sign-alphabet">Prstová abeceda</a></li>
				<li><a href="/playground">Playground</a></li>
				<li><a href="/translator">Překladač z texu</a></li>
			</ul>
		</nav>
		<span><a class="githubLink" href="https://github.com/martinikf/UPA">GitHub</a></span>
	</div>
</header>

<slot></slot>

<style>
	:global(body) {
		background-color: #444444;
		color: #e6e6e6;
	}

	header{
		background-color: #2e2e2e;
		padding: 20px;
	}

	.headerContent{
		max-width: 1600px;
		margin: auto;
		display: flex;
		justify-content: space-between;
	}

	header h1{
		display: inline;
		padding: 0;
		margin: 0 3rem 0 0;
		font-size: 1rem;
		color: #cccccc;
	}

	nav ul{
		list-style: none;
		margin: 0;
		padding: 0;
	}

	nav ul li{
		display: inline;
		margin-right: 1.2rem;
	}

	nav ul li a{
		color: #cccccc;
		text-decoration: none;
	}

	nav ul li a:hover {
		color: #cccccc;
		text-decoration: underline;
	}

	.githubLink{
		text-decoration: none;
		color: dimgrey;
	}

	.githubLink:hover{
		text-decoration: underline;
	}

	@media (max-width: 768px) {
		.logo{
			display: none;
		}

		header{
			padding: 15px 5px;
		}

		.githubLink{
			display: none;
		}

		nav ul li{
			margin-right: .5rem;
		}
	}

</style>