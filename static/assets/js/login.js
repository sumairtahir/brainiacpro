const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signInContainer = document.getElementById('sign-in-container');
const signUpContainer = document.getElementById('sign-up-container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
	signUpContainer.classList.remove("d-none");
	signInContainer.classList.add("d-none");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
	signInContainer.classList.remove("d-none");
	signUpContainer.classList.add("d-none");
});