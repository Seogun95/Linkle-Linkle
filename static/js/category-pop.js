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
        url: '/category',
        data: { category_name: category_name, category_img_url: img_url },
        success: function (response) {
            alert(response);
        },
    });
}

// =================================

// ================================= 테스트 완료
function categoryPosting() {
    $.ajax({
        type: 'GET',
        url: '/categories',
        data: {},
        success: function (response) {
            let rows = response['categories'];
            for (let i = 0; i < rows.length; i++) {
                let category_title = rows[i]['name'];
                let category_img = rows[i]['image'];
                console.log(rows);
                console.log(category_title);
                let temp_html = `<div class="col cards-box" data-aos="fade-up" data-aos-delay="200" data-aos-easing="ease-in-out" data-aos-once="false">
                                    <div class="cards-box__container logo">
                                        <div class="cards-box__card" style="width: 18rem">
                                            <a href="https://www.youtube.com/watch?v=GmxPT-P331s&t=1s">
                                                <img src="${category_img}" class="cards-box__img" alt="bookimage" onerror="this.src='../static/img/error_img.png';" />

                                                <p class="cards-box__body-title text-center">${category_title}</p>
                                            </a>
                                        </div>
                                    </div>
                                </div>`;
                $('#cards-box').append(temp_html);
            }
        },
    });
}
// =================================
