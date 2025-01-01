const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");


const requestOptions = {
  method: "GET",
  headers: myHeaders,
  redirect: "follow"
};
let url = window.location.href; // 抓網址
let index = url.lastIndexOf("/"); // 尋找網址的最後一個 "/"
fetch(`/order-list/${url.substring(index+1,url.length)}/order`, requestOptions) // 
.then((response) => response.json())
.then((result) => {
  const div = document.querySelector(".order-list");
  let html = "";
    
    for(let i = 0; i < result['data'].length; i += 1) {
        html += `<div class="col">`;
        html += `<a class="btn btn-info menu-btn" href="/delivery/order/${result["data"][i]["id"]}">${result["data"][i]["name"]}</a>`;
        html += `</div>`;
    }
    div.innerHTML = html;
  })
  .catch((error) => console.error(error));