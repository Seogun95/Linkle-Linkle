function toggle_sign_up() {
    $('#sign-up-box').toggleClass('is-hidden');
    $('.logM').toggleClass('is-hidden');
}

function sign_up() {
    let psswdcheck = $('#input-password2').val();
    let passwd = $('#input-password').val();
    let id = $('#input-username').val();

    $.ajax({
        type: 'POST',
        url: '/api/register',
        data: {
            id_name: id,
            passwd_one: passwd,
            passwd_two: psswdcheck,
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.');
                console.log(response['result']);
                window.location.href = '/';
            } else {
                alert(response['msg']);
            }
        },
    });
}

function sign_in() {
    let passwd = $('#input-password').val();
    let id = $('#input-username').val();
    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: { id_give: id, pw_give: passwd },
        success: function (response) {
            console.log(response);
            if (response['result'] == 'success') {
                // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                $.cookie('mytoken', response['token']);

                alert('로그인 완료!');
                window.location.href = '/category';
            } else {
                // 로그인이 안되면 에러메시지를 띄웁니다.
                alert(response['msg']);
            }
        },
    });
}

function get_nick() {
    $.ajax({
        type: 'GET',
        url: '/api/nick',
        data: {},
        success: function (response) {
            console.log(response);
        },
    });
}
