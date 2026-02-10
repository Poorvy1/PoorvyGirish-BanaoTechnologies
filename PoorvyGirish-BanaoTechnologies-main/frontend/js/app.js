document.getElementById("signupForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const data = new FormData();
    data.append("username", document.getElementById("username").value);
    data.append("email", document.getElementById("email").value);
    data.append("password", document.getElementById("password").value);
    data.append("role", document.getElementById("role").value);

    fetch("http://127.0.0.1:8000/users/signup/", {
        method: "POST",
        body: data
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("message").innerText = data.message || data.error;
    });
});
