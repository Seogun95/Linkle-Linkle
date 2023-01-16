//===========================네비게이션 사이드바 버튼 클릭
$('#nav-toggle').click(function () {
    $(this).toggleClass('is-active');
    $('ul.nav').toggleClass('show');
});

//===========================네비게이션 스크롤 이벤트
$(window).scroll(function () {
    var scroll = $(window).scrollTop();

    if (scroll >= 50) {
        $('.custom-navbar').addClass('scroll');
    } else {
        $('.custom-navbar').removeClass('scroll');
    }
});

//===========================포스팅 팝업
$(document).ready(function () {
    var target = $('#postPop');
    $(document).on('click', '.nav__posting', function (e) {
        target
            .fadeIn(300, function () {
                $('#postPop__url').focus();
            })
            .addClass('reveal');
        $('body').addClass('is-postPop');
    });

    //===========================포스팅 hover시 닫기 버튼 show
    $('#cards-box .col').hover(
        function () {
            $('button', this).addClass('active');
        },
        function () {
            $('button', this).removeClass('active');
        }
    );
});

//===========================닫기 버튼클릭시 팝업 닫기
$('#close__postPop').click(function () {
    $(this).closest('#postPop').removeClass('reveal').fadeOut(200);
    $('body').removeClass('is-postPop');
});

//============================로그인 버튼 눌렀을떄(JS 추가된 부분).
$('.login-btn').click(function () {
    $('#header-img').toggleClass('none');
    $('.login-page').toggleClass('login-page-pop');
    $('.custom-navbar').toggleClass('login-nav');
    $('.container-mid').toggleClass('container-mid-max');
    $('.login-btn').toggleClass('login-btn-max');

    if ($('.login-page').hasClass('login-page-pop') === true) {
        $('.login-btn__text').text('로그인 창 닫기');
    } else {
        $('.login-btn__text').text('바로 시작하기');
    }
});
