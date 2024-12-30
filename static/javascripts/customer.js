const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");


const requestOptions = {
  method: "GET",
  headers: myHeaders,
  redirect: "follow"
};

fetch("/store-list", requestOptions)
  .then((response) => response.json())
  .then((result) => {
    const div = document.querySelector(".store-list");
    
    let html = "";
    for(let i = 0; i < result['data'].length; i += 1) {
        html += `<div class="col">`;
        html += `<a class="btn btn-warning store-btn" href="/customer/store/${result["data"][i]["id"]}">${result["data"][i]["name"]}</a>`;
        html += `</div>`;
    }
    div.innerHTML = html;
  })
  .catch((error) => console.error(error));