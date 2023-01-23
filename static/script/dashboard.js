populateKeyTable();

async function populateKeyTable() {
    const table = document.getElementById("api-key-table");

    apikeys = await fetch('/api-keys')
        .then(res => res.json());

    while(table.children.length > 1) {
        table.removeChild(table.lastChild);
    }

    tableRows = apikeys.map(apikey => {
        const row = document.createElement("tr");

        const checkbox = document.createElement("input");
        checkbox.setAttribute('type', 'checkbox');
        checkbox.setAttribute('id', apikey.title);
        const checkField = document.createElement("td");
        checkField.append(checkbox);
        row.appendChild(checkField);
        const titleField = document.createElement("td");
        titleField.append(document.createTextNode(apikey.title))
        row.appendChild(titleField);
        const createdField = document.createElement("td");
        createdField.append(document.createTextNode(apikey.created))
        row.appendChild(createdField);
        const expiresField = document.createElement("td");
        expiresField.append(document.createTextNode(apikey.expires))
        row.appendChild(expiresField);
        const nameField = document.createElement("td");
        nameField.append(document.createTextNode(apikey.username))
        row.appendChild(nameField);

        table.appendChild(row);
    })
}

function toggleCreateAPIKeyModal() {
    const modal = document.getElementById('create-api-key-modal');
    modal.classList.toggle("hidden");
    if (!modal.classList.contains("hidden"))
        document.getElementById('title-input').focus();
}

async function handleAPIKeyCreation(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    let apikey = {};

    formData.forEach((value, key) => {
        apikey[key] = value;
    })

    apikey.created = (new Date()).toISOString()
    const { created, expires, title, username } = apikey;
    apikey = { 
        created: created,
        expires: expires,
        title: title, 
        username: username 
    };
    console.log(apikey);

    const res = await fetch('/api-keys', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // username, created, expired, title
        body: JSON.stringify(apikey)
    });

    if (res.ok) {
        const { apitoken } = await res.json()
        alert(apitoken);
    }

    populateKeyTable();
    toggleCreateAPIKeyModal();
}

async function removeAPIKeys() {
    const table = document.getElementById("api-key-table");
    const tableChildren = [...table.children];

    const toBeDeleted = [];

    tableChildren.forEach((child) => {
        console.log(child.children);
        if (child.children[0].children[0].checked) {
            toBeDeleted.push(child.children[1].textContent)
        }
    })

    await fetch('/api-keys',{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({toBeDeleted: toBeDeleted})
    });

    populateKeyTable();
}