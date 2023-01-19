$(document).ready(function () {
    urlPosting();
});

// ================================= 테스트 완료
function posting() {
    let post_url = $('#postPop__url').val();
    let post_title = $('#postPop__title').val();
    let post_desc = $('#postPop__titlecomments').val();
    let url_href = window.location.href;
    let url = new URL(url_href);
    let a = url.searchParams.get('id');

    $.ajax({
        type: 'POST',
        url: '/api/posting',
        data: { post_url: post_url, post_title: post_title, post_desc: post_desc, post_category: a },
        success: function (response) {
            alert('성공하였습니다.');
            window.location.href = `/post?id=${a}`;
        },
    });
}

// =================================

function urlPosting() {
    let url_href = window.location.href;
    let url = new URL(url_href);
    let a = url.searchParams.get('id');
    $.ajax({
        type: 'GET',
        url: `/api/posts?category_id=${a}`,
        data: {},
        success: function (response) {
            console.log(response)
            let rows = response['posts'];
            let like = response['like_list'];
            for (let i = 0; i < rows.length; i++) {
                let url = rows[i]['link_url'];
                let img = rows[i]['image'];
                let category_title = rows[i]['name'];
                let title = rows[i]['title'];
                let comments = rows[i]['desc'];
                let user_nickname = rows[i]['author'];
                let id = rows[i]['id'];

                let temp_html = `

                <div class="col cards-box" data-aos="fade-up" data-aos-delay="200" data-aos-easing="ease-in-out" data-aos-once="false">
                <div class="cards-box__container logo">
                    <div class="card-box__like-comment-container">
                      <button onclick='remove_post(${id})' class='remove-btn-rebtn pos'></button>
                      <span style='color: white'>${like_num}</span>
                        <button onclick='like_post(${id})' class="btn like"></button>
                    </div>
                    <div class="cards-box__card" style="width: 18rem">
                        <a href="${url}">
                            <img src="${img}" class="cards-box__img" alt="bookimage" />

                            <p class="cards-box__body-title" id="${category_title}">${title}</p>
                        </a>
                        <p class="cards-box__body-comment">${comments}</p>
                        <p class="cards-box__body-user">by. ${user_nickname}</p>
                    </div>
                </div>
            </div>
               `;
                $('.post__cards-box').append(temp_html);
            }
        },
    });
}

function like_post(id) {
    let url_href = window.location.href;
    let url = new URL(url_href);
    let a = url.searchParams.get('id');
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: { post_id: id },
        success: function (response) {
            alert('좋아요.');
            window.location.href = `/post?id=${a}`;
        },
    });
}

function remove_post(id) {
    let url_href = window.location.href;
    let url = new URL(url_href);
    let a = url.searchParams.get('id');
    $.ajax({
        type: 'POST',
        url: '/api/remove',
        data: { remove_id: id },
        success: function (response) {
            alert('삭제되었습니다.');
            window.location.href = `/post?id=${a}`;
        },
    });
}
