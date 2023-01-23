const submitHandler = async(e) => {
    e.preventDefault();

    console.log(e);

    let username = document.getElementById('username-input').value;
    let password = document.getElementById('password-input').value;
    document.getElementById('username-input').value = "";
    document.getElementById('password-input').value = "";

    let res = await fetch('/login', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Authorization': `Basic ${btoa(`${username}:${password}`)}`,
            'Content-Type': 'application/json',
        },
    })
    
    console.log(res);
}