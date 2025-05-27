document.getElementById('checkInBtn').addEventListener('click', async () => {
    const response = await fetch('/check_in', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    const result = await response.json();
    if (result.success) {
        document.getElementById('2faModal').style.display = 'block';
    } else {
        alert(result.message);
    }
});

document.getElementById('verify2faBtn').addEventListener('click', async () => {
    const code = document.getElementById('2faCode').value;
    const response = await fetch('/verify_2fa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
    });
    
    const result = await response.json();
    alert(result.message);
    if (result.success) {
        document.getElementById('2faModal').style.display = 'none';
        location.reload();
    }
});
