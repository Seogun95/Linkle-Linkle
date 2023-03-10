$(document).ready(function () {
    categoryPosting();
});

// 카테고리 post 존재시 사라지게 하는 함수
// let get_list;
// if (!get_list) {
//     $('.category').show();
//     $('.main').hide();
// } else {
//     $('.category').hide();
//     $('.main').show();
// }

// ================================= issue
function check() {
    $.ajax({
        type: 'GET',
        url: '/categories',
        data: {},
        success: function (response) {
            let check = response;
            if (!check) {
                $('.category').show();
                $('.main').hide();
            } else {
                $('.category').hide();
                $('.main').show();
            }
        },
    });
}
// =================================

// ================================= 테스트 완료
function category() {
    let img_url = $('#categoryPop__url').val();
    let category_name = $('#categoryPop__title').val();

    $.ajax({
        type: 'POST',
        url: 'api/category',
        data: { category_name: category_name, category_img_url: img_url },
        success: function (response) {
            alert('등록 완료!');
            window.location.href = '/category';
        },
    });
}

// =================================

// ================================= 테스트 완료

function categoryPosting() {
    $.ajax({
        type: 'GET',
        url: '/api/categories',
        data: {},
        success: function (response) {
            $('.category__cards-box').empty();
            let rows = response['categories'];
            for (let i = 0; i < rows.length; i++) {
                let category_title = rows[i]['name'];
                let category_img = rows[i]['img'];
                let id = rows[i]['id'];
                let temp_html = `<div class="col cards-box" id=${id} data-aos="fade-up" data-aos-delay="200" data-aos-easing="ease-in-out" data-aos-once="false">
                <div class="cards-box__cate-container">
                    <div class="cards-box__cateTitle"><span>${category_title}</span></div>
                </div>
                <button onclick="remove_category(${id})" class="remove-btn-rebtn"></button>
                <div class="cards-box__container logo">
                    <div class="cards-box__card" style="width: 18rem">
                        <a href="/post?id=${id}">
                            <img src="${category_img}" class="cards-box__img alt="bookimage" onerror="this.src='static/img/error_img.png';" />
                        </a>
                    </div>
                </div>
            </div>`;
                $('.category__cards-box').append(temp_html);
            }
        },
    });
}
// =================================

function remove_category(id) {
    $.ajax({
        type: 'POST',
        url: '/api/cateRemove',
        data: { remove_id: id },
        success: function (response) {
            alert(response['remove']);
            window.location.href = `/category`;
        },
    });
}
