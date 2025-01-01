const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

const requestOptions = {
  method: "GET",
  headers: myHeaders,
  redirect: "follow"
};

let url = window.location.href; // 抓網址
let index = url.lastIndexOf("/"); // 尋找網址的最後一個 "/"
fetch(`/store-list/${url.substring(index + 1, url.length)}/menu`, requestOptions) // 
  .then((response) => response.json())
  .then((result) => {
    const div = document.querySelector(".menu-list");
    let html = "";

    for (let i = 0; i < result['data'].length; i += 1) {
      html += `<div class="col">`;
      html += `<button class="btn btn-info menu-btn" data-name="${result["data"][i]["name"]}">${result["data"][i]["name"]}</button>`;
      html += `</div>`;
    }

    // 動態加入輸入框和按鈕
    html += `
      <div class="col-12 mt-3">
        <input type="text" id="destinationInput" class="form-control" placeholder="請輸入送餐地址">
      </div>
      <div class="col-12 mt-2 text-center">
        <button id="submitOrder" class="btn btn-primary" disabled>送出訂單</button>
      </div>
    `;
    div.innerHTML = html;

    // 動態菜品名稱變數
    let selectedMenuName = null;

    // 綁定菜單按鈕點擊事件
    const menuButtons = document.querySelectorAll(".menu-btn");
    menuButtons.forEach((btn) => {
      btn.addEventListener("click", function () {
        selectedMenuName = btn.getAttribute("data-name"); // 獲取菜品名稱
        alert(`已選擇菜品：${selectedMenuName}`);
        document.getElementById("submitOrder").disabled = false; // 啟用送出按鈕
      });
    });

    // 綁定送出訂單按鈕事件
    document.getElementById("submitOrder").addEventListener("click", function () {
      const destinationInput = document.getElementById("destinationInput").value; // 獲取用戶輸入值

      if (!destinationInput) {
        alert("請填寫送餐地址！");
        return; // 若未填寫則終止執行
      }

      if (!selectedMenuName) {
        alert("請選擇菜品！");
        return; // 若未選擇菜品則終止執行
      }

      const postHeaders = new Headers();
      postHeaders.append("Content-Type", "application/json");
      postHeaders.append("Cookie", "session=eyJpZCI6MSwibG9naW5JRCI6InNyal9jdXMiLCJyb2xlIjoyfQ.Z3Tn0g.VPj2MvnfqrjFQ_ZgFh4wa3pmZyo");

      const raw = JSON.stringify({
        "order": [
          {
            "destination": destinationInput, // 使用者輸入
            "name": selectedMenuName // 動態選擇的菜品名稱
          }
        ]
      });

      const postRequestOptions = {
        method: "POST",
        headers: postHeaders,
        body: raw,
        redirect: "follow"
      };

      fetch("http://localhost:5000/store-list/1/order", postRequestOptions)
        .then((response) => response.json())
        .then((result) => {
          console.log(result); // 檢查伺服器回應
          alert("訂單已送出！");

          document.getElementById("destinationInput").value = ""; // 清空輸入框
          document.getElementById("submitOrder").disabled = true; // 禁用送出按鈕
          window.location.href = "/customer";
        })
        .catch((error) => console.error("Error:", error));
    });
  })
  .catch((error) => console.error(error));
