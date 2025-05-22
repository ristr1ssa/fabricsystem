function showTab(tabId) {
    
    document.querySelectorAll('.container').forEach(el => el.classList.add('hidden'));
    document.getElementById(tabId).classList.remove('hidden');
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    event.target.classList.add('active');
    
    if (tabId=="active-users") {
        get_users_table()
    }else if (tabId=="new-orders") {
        get_orders();  
    }else if (tabId=='active-order-list'){
        get_active_orders()
    };
        
        
        // active-order-list - список активных заказов
}

function toggleForm() {
    let modal = document.getElementById('order-modal');
    modal.classList.toggle('show');
}

function toggleUserForm() {
    let modal = document.getElementById('user-modal');
    modal.classList.toggle('show');
}

function addOrder() {
    let name = document.getElementById('name').value;
    let article = document.getElementById('article').value;
    let price = document.getElementById('price').value;

    if (!name || !article || !price) return alert("Заполните все поля");

    let orderItem = document.createElement('tr');
    orderItem.innerHTML = `<td>${article}</td><td>${name}</td><td>${price} руб.</td><td><button onclick="moveToActive(this)">+</button></td>`;
    document.getElementById('order-list').appendChild(orderItem);
    
    addOrderToDb(name, article, price)
    toggleForm();
}

function moveToActive(article) {
    let row = document.getElementById(article).cloneNode(true)
    row.lastElementChild.remove()

    row.innerHTML += '<td>В процессе</td>';
    row.innerHTML += `<td><button onclick="addOrderToActiveDb(${article}, "DEL")">DEL</button></td>`;
    document.getElementById('active-order-list').appendChild(row);

    addOrderToActiveDb(article, 'ADD')
    showSuccessMessage();
}

function showSuccessMessage() {
    let message = document.getElementById('success-message');
    message.classList.add('show');

    setTimeout(() => {
        message.classList.remove('show');
    }, 2000);
}

function addUser() {
    let userLogin = document.getElementById('userLogin').value;
    let userPass = document.getElementById('userPass').value;


    let select = document.querySelector('select')
    let userRole = select.value;

    if (!userLogin || !userRole || !userPass) return alert("Заполните все поля");

    let orderItem = document.createElement('tr');
    orderItem.innerHTML = `<td>1</td><td>${userLogin}</td><td>${userRole}</td><td><button class="del-btn" onclick="delUserFromDb(${data[i]["id"]})">DEL</button></td>`;
    document.getElementById('active-user-list').appendChild(orderItem);

    addUserToDb(userLogin, userPass, userRole)
    toggleUserForm();
}



function get_users_table() {
    document.getElementById('active-user-list').innerHTML = "";

    fetch('/get-active-users')  // URL бэкенда
    .then(response => response.json())  // Преобразуем ответ в JSON
    .then(data => {
        for (let i = 0; i <= data.length - 1; i++) {
            
            let orderItem = document.createElement('tr')
            orderItem.setAttribute('id', data[i]["id"] );
            
            orderItem.innerHTML = `<td>${data[i]["id"]}</td><td>${data[i]['username']}</td><td>${data[i]['role']}</td><button class="del-btn" onclick="delUserFromDb(${data[i]["id"]})">DEL</button>`;

            document.getElementById('active-user-list').appendChild(orderItem);
        }})  // Работаем с данными
    .catch(error => console.error('Ошибка:', error));
}

function get_orders() {
    document.getElementById('order-list').innerHTML = "";

    fetch('/get-orders')  // URL бэкенда
    .then(response => response.json())  // Преобразуем ответ в JSON
    .then(data => {
        for (let i = 0; i <= data.length - 1; i++) {
            
            let orderItem = document.createElement('tr')
            orderItem.setAttribute('id', data[i]["article"] );
            
            orderItem.innerHTML = `<td>${data[i]["article"]}</td><td>${data[i]['name']}</td><td>${data[i]['price']}</td><button class="add-active-btn" onclick="moveToActive(${data[i]["article"]})">ADD</button>`;
            
            document.getElementById('order-list').appendChild(orderItem);
        }})  // Работаем с данными
    .catch(error => console.error('Ошибка:', error));
}

function get_active_orders() {
    document.getElementById('active-order-list').innerHTML = "";

    fetch('/get-active-users')  // URL бэкенда
    .then(response => response.json())  // Преобразуем ответ в JSON
    .then(data => {
        for (let i = 0; i <= data.length - 1; i++) {
            
            let orderItem = document.createElement('tr')
            orderItem.setAttribute('id', data[i]["id"] );
            
            // orderItem.innerHTML = `<td>${data[i]["id"]}</td><td>${data[i]['username']}</td><td>${data[i]['role']}</td><button class="add-active-btn" onclick="delUserFromDb(${data[i]["id"]})">DEL</button>`;
            
            document.getElementById('active-user-list').appendChild(orderItem);
        }})  // Работаем с данными
    .catch(error => console.error('Ошибка:', error));
}


function addUserToDb(userLogin, userPass, userRole){
    fetch(`/register?user=${userLogin}&pass=${userPass}&role=${userRole}`)
    .then(response => response.json())
}

function delUserFromDb (uid){
    fetch(`/del-user?uid=${uid}`)
    .then(response => {
        if (response.ok){
            orderItem = document.getElementById(uid)
            document.getElementById('active-user-list').removeChild(orderItem);
        };
    })
};

function addOrderToDb(name, article, price){
    fetch(`/add-order?name=${name}&article=${article}&price=${price}`)
    .then(response => response.json())
};

function addOrderToActiveDb(article, action){
    fetch(`/active-orders?action=${action}&article=${article}`)
    .then(response => response.json())
}; 


window.addEventListener('load', () => {
    get_orders();
  });