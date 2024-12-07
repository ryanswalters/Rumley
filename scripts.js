function checkPassword() {
    const password = document.getElementById('password').value;
    const encryptedPassword = '5f4dcc3b5aa765d61d8327deb882cf99'; // Example MD5 hash for 'password'

    if (md5(password) === encryptedPassword) {
        window.location.href = 'protected.html';
    } else {
        alert('Incorrect password');
    }
}

// Simple MD5 hash function (for demonstration purposes)
function md5(string) {
    return CryptoJS.MD5(string).toString();
}