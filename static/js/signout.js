function logout() {
    $.removeCookie('mytoken');
    alert('๋ก๊ทธ์์!');
    window.location.href = '/';
}
