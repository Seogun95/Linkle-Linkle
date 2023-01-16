// 카테고리 post 존재시 사라지게 하는 함수
// $(document).ready(function () {});
// let get_list;
// if (!get_list) {
//     $('.category').show();
//     $('.main').hide();
// } else {
//     $('.category').hide();
//     $('.main').show();
// }

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

// 테스트 완료
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

// function categoryPosting() {
//     $.ajax({
//         type: 'GET',
//         url: '/categories',
//         data: {},
//         success: function (response) {
//             let rows
//         },
//     });
// }
