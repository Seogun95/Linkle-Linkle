function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!');
    window.location.href = '/login';
}
