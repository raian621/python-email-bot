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
    const apikey = {};

    formData.forEach((value, key) => {
        apikey[key] = value;
    })

    apikey.created = (new Date()).toISOString()

    await fetch('/api-keys',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(apikey)
    });

    populateKeyTable();
    toggleCreateAPIKeyModal();
}

async function removeAPIKeys() {
    const table = document.getElementById("api-key-table");

    const toBeDeleted = [];

    table.children.forEach((child) => {
        if (child.children[0].checked) {
            toBeDeleted.push(child.children[1].textContent)
        }
    })

    await fetch('/api-keys',{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(toBeDeleted)
    });

    populateKeyTable();
}