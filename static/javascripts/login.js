function sendRequest(data) {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        "username": data["username"],
        "password": data["password"],
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };

    fetch("/login", requestOptions)
        .then((response) => response.json())
        .then((result) => {
            window.location.href = result["url"];
        })
        .catch((error) => console.error(error));
}

function getFormData() {
    const username = document.querySelector('[name="username"]').value;
    const password = document.querySelector('[name="password"]').value;
    return {
        username,
        password
    }
}

function submitForm() {
    const raw = getFormData()
    sendRequest(raw);
}
